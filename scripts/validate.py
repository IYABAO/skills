#!/usr/bin/env python3
"""Validate all skills in this repo. Run with: python scripts/validate.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_JSON = ROOT / ".claude-plugin" / "marketplace.json"

errors = []
warnings = []


def check(condition, msg):
    if not condition:
        errors.append(msg)


def warn(msg):
    warnings.append(msg)


# 1. JSON manifests valid
for f in [PLUGIN_JSON, MARKETPLACE_JSON]:
    check(f.exists(), f"Missing {f.relative_to(ROOT)}")
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{f.name}: invalid JSON: {e}")
            continue
        if f == PLUGIN_JSON:
            check("skills" in data, "plugin.json missing 'skills' array")
            check("name" in data, "plugin.json missing 'name'")
            check("version" in data, "plugin.json missing 'version'")

# 2. Each declared skill exists and has valid SKILL.md
plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
skill_dirs = plugin.get("skills", [])
check(len(skill_dirs) > 0, "No skills declared in plugin.json")

for rel in skill_dirs:
    skill_path = ROOT / rel
    check(skill_path.is_dir(), f"Skill dir not found: {rel}")
    if not skill_path.is_dir():
        continue

    skill_md = skill_path / "SKILL.md"
    check(skill_md.exists(), f"{rel}: SKILL.md missing")
    if not skill_md.exists():
        continue

    text = skill_md.read_text(encoding="utf-8")

    # Frontmatter must start with ---
    check(text.startswith("---\n"), f"{rel}: SKILL.md must start with YAML frontmatter (---)")
    if not text.startswith("---\n"):
        continue

    # Extract frontmatter block
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    check(m is not None, f"{rel}: frontmatter not closed with ---")
    if not m:
        continue

    fm = m.group(1)

    # Parse simple key: value (no nested YAML needed for validation)
    def fm_field(key):
        mm = re.search(rf"^{re.escape(key)}\s*:\s*(.+)$", fm, re.MULTILINE)
        return mm.group(1).strip().strip('"').strip("'") if mm else None

    name = fm_field("name")
    description = fm_field("description")

    check(name, f"{rel}: frontmatter missing 'name'")
    check(description, f"{rel}: frontmatter missing 'description'")

    if name:
        check(re.match(r"^[a-z0-9-]+$", name),
              f"{rel}: name '{name}' must be hyphen-case (lowercase letters, digits, hyphens)")
        dir_name = skill_path.name
        check(name == dir_name,
              f"{rel}: frontmatter name '{name}' does not match directory name '{dir_name}'")

    if description:
        check(len(description) <= 1024,
              f"{rel}: description too long ({len(description)} chars, max 1024)")
        check("<" not in description and ">" not in description,
              f"{rel}: description must not contain angle brackets")

    # SKILL.md body should not be empty after frontmatter
    body = text[m.end():].strip()
    check(len(body) > 100, f"{rel}: SKILL.md body too short ({len(body)} chars)")


# 3. Report
if warnings:
    print("⚠ Warnings:")
    for w in warnings:
        print(f"  - {w}")

if errors:
    print(f"✗ Validation FAILED with {len(errors)} error(s):")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)
else:
    print(f"✓ All {len(skill_dirs)} skill(s) valid.")
    sys.exit(0)
