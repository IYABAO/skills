# IYABAO Skills

Learning & thinking skills for AI agents. Install one plugin, get a set of composable skills.

## Install

### Claude Code

```bash
/plugin marketplace add IYABAO/skills
/plugin install iyabao-skills@iyabao-skills
```

### skills.sh CLI

```bash
npx skills add IYABAO/skills
```

## Included skills

| Skill | What it does |
|---|---|
| **drill** | Given a word/concept/domain, produce an expert-level learning roadmap: 5-7 dimensions, L1/L2/L3 depth, shortest path, scenario-based self-tests, resource map with links, common pitfalls, expert vs amateur dividing line. |
| **liken** | Given things you love (books/movies/music/apps/coffee/cities), extract taste dimensions and find cross-domain recommendations with "why it's like that". |
| **knowpitch** | Decompose any knowledge domain into a football team (formation), with ELI5 player cards, coach's tactics board, and a rendered SVG formation diagram. Triggers: kp11/kpt/kpitch. |
| **spar** | Mock technical interview. Given a direction (Go concurrency / system design / databases), ask one question, follow up relentlessly, then give a scorecard. No answers fed during the drill. |
| **poke** | Socratic questioning. Given your own argument/decision, ask one follow-up at a time until you find the logical hole yourself. No preaching, no answers handed over. |
| **trace** | Root cause analysis. Given a bug/incident/alert, walk the causal chain backward layer by layer, requiring evidence at each step. Distinguishes root cause from trigger from symptom. |
| **vet** | Information review. Given an article/paper/tech proposal/blog post, produce a vetting report: evidence quality, logic gaps, hidden assumptions, strongest counter-argument, author conflicts of interest. |
| **memo** | File memory & context persistence. Auto-creates MEMO.md in project root (current state / done / next / waiting on user / key decisions), updates at decision points, auto-commits to git. Never lose context between sessions or agents. |

## Development

```bash
# Run validation (also runs on every PR via GitHub Actions)
python scripts/validate.py

# Run LLM evals (requires OPENAI_API_KEY, manual trigger)
OPENAI_API_KEY=sk-... python scripts/run-evals.py
```

### Adding a new skill

1. Create `skills/<category>/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`).
2. Add the path to `skills` array in `.claude-plugin/plugin.json`.
3. Run `python scripts/validate.py` — it must pass.
4. Open a PR. CI must be green before merge.

## License

MIT
