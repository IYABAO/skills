#!/usr/bin/env python3
"""
run-evals.py — LLM-based skill output evaluation.

For each eval case:
  1. Build a prompt with the SKILL.md content prepended
  2. Call LLM to generate output
  3. Call LLM Judge to check each assertion (PASS/FAIL)
  4. Report pass rate

Usage:
  # Run all evals (requires OPENAI_API_KEY)
  OPENAI_API_KEY=sk-... python scripts/run-evals.py

  # Run only one skill
  OPENAI_API_KEY=sk-... python scripts/run-evals.py --skill drill

  # Dry run (list cases, don't call LLM)
  python scripts/run-evals.py --dry-run

Environment:
  OPENAI_API_KEY   — required for actual LLM calls
  OPENAI_BASE_URL   — optional, default https://api.openai.com/v1
  EVAL_MODEL        — optional, default gpt-4o-mini (generator)
  JUDGE_MODEL       — optional, default gpt-4o-mini (judge)
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS_DIR = ROOT / "evals"
SKILLS_DIR = ROOT / "skills"


def load_skill_md(skill_name: str) -> str:
    """Load SKILL.md content for a skill."""
    for category_dir in SKILLS_DIR.iterdir():
        skill_path = category_dir / skill_name / "SKILL.md"
        if skill_path.exists():
            return skill_path.read_text(encoding="utf-8")
    print(f"ERROR: SKILL.md not found for {skill_name}", file=sys.stderr)
    sys.exit(1)


def load_eval_cases(skill_name: str) -> dict:
    f = EVALS_DIR / f"{skill_name}.evals.json"
    if not f.exists():
        print(f"ERROR: {f} not found", file=sys.stderr)
        sys.exit(1)
    return json.loads(f.read_text(encoding="utf-8"))


def call_llm(messages: list, model: str) -> str:
    """Call OpenAI-compatible chat API."""
    import urllib.request

    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    body = json.dumps({"model": model, "messages": messages, "temperature": 0.3}).encode()
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]


def run_case(skill_name: str, skill_md: str, case: dict, model: str, judge_model: str) -> dict:
    """Run one eval case: generate output, then judge assertions."""
    # Step 1: Generate output with skill context
    gen_prompt = f"{skill_md}\n\n---\n\nNow respond to this user request following the skill above:\n\n{case['prompt']}"
    output = call_llm(
        [{"role": "user", "content": gen_prompt}],
        model,
    )

    # Step 2: Judge each assertion — ask for JSON output, parse it
    assertions_text = "\n".join(f"{i+1}. {a}" for i, a in enumerate(case["assertions"]))
    judge_prompt = f"""You are a strict evaluator. Below is the output of an AI skill. Check each assertion.

SKILL: {skill_name}
USER REQUEST: {case['prompt']}
OUTPUT:
---
{output}
---

ASSERTIONS:
{assertions_text}

Return ONLY a JSON array, no other text. Each element:
{{"id": <assertion number>, "pass": true/false, "reason": "<one sentence>"}}
"""
    judge_result = call_llm(
        [{"role": "user", "content": judge_prompt}],
        judge_model,
    )

    # Parse JSON from judge output (handle code fences)
    passed = 0
    total = len(case["assertions"])
    detail_lines = []
    try:
        # Strip code fences if present
        cleaned = judge_result.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        results = json.loads(cleaned)
        for r in results:
            aid = r.get("id", "?")
            ok = r.get("pass", False)
            reason = r.get("reason", "")
            if ok:
                passed += 1
            detail_lines.append(f"  ASSERTION {aid}: {'PASS' if ok else 'FAIL'} — {reason}")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        detail_lines.append(f"  WARN: judge output not parseable: {e}")
        detail_lines.append(f"  Raw: {judge_result[:200]}")

    return {
        "id": case["id"],
        "name": case["name"],
        "prompt": case["prompt"],
        "passed": passed,
        "total": total,
        "output_length": len(output),
        "judge_detail": "\n".join(detail_lines),
    }


def discover_skills():
    """Discover skills by scanning evals/ directory for *.evals.json files."""
    skills = []
    for f in sorted(EVALS_DIR.glob("*.evals.json")):
        skills.append(f.stem.replace(".evals", ""))
    return skills


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", help="Run only this skill")
    parser.add_argument("--dry-run", action="store_true", help="List cases without calling LLM")
    args = parser.parse_args()

    all_skills = discover_skills()
    if args.skill:
        skills = [args.skill]
    else:
        skills = all_skills
    model = os.environ.get("EVAL_MODEL", "gpt-4o-mini")
    judge_model = os.environ.get("JUDGE_MODEL", "gpt-4o-mini")

    all_results = {}

    for skill_name in skills:
        eval_config = load_eval_cases(skill_name)
        cases = eval_config.get("evals", [])

        if args.dry_run:
            print(f"\n=== {skill_name} ({len(cases)} cases) ===")
            for c in cases:
                print(f"  {c['id']}: {c['name']} — {len(c['assertions'])} assertions")
            continue

        skill_md = load_skill_md(skill_name)
        print(f"\n=== Running {skill_name} evals ({len(cases)} cases) ===")

        results = []
        for case in cases:
            print(f"  Running {case['id']}: {case['name']}...")
            r = run_case(skill_name, skill_md, case, model, judge_model)
            results.append(r)
            print(f"    → {r['passed']}/{r['total']} assertions passed")

        all_results[skill_name] = results

    if not args.dry_run:
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        total_pass = 0
        total_assert = 0
        for skill, results in all_results.items():
            s_pass = sum(r["passed"] for r in results)
            s_total = sum(r["total"] for r in results)
            total_pass += s_pass
            total_assert += s_total
            pct = s_pass / s_total * 100 if s_total else 0
            print(f"  {skill}: {s_pass}/{s_total} ({pct:.0f}%)")
        overall = total_pass / total_assert * 100 if total_assert else 0
        print(f"  OVERALL: {total_pass}/{total_assert} ({overall:.0f}%)")

        # Exit non-zero if any assertion fails (for CI)
        if total_pass < total_assert:
            sys.exit(1)


if __name__ == "__main__":
    main()
