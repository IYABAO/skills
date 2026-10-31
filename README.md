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
| **pulse** | 30-second progress report. Reads project files (AGENTS.md/active/daily) or conversation context, outputs a fixed 5-section status: doing / done today / next / waiting on you / one-line summary. |
| **panel** | Multi-role plan review. Before you commit, stress-test your plan from 3-4 angles: user view, devil's advocate, tech realist, future view. Each role must find a real problem; final output separates must-fix from nice-to-know. |
| **baton** | Project handoff. When you're done or switching agents, scan the project and write a complete HANDOVER.md: what it is, how to run it, current state, TODO, key decisions, pitfalls. Next person starts without reading chat history. |

## Quick examples

**drill** — "drill 向量数据库"
→ 输出：5-7 个维度（索引原理/查询性能/一致性/运维/成本），每个维度 L1/L2/L3，20 小时速成路径，自测题，资源链接，新手坑。

**liken** — "我喜欢《百年孤独》和 Node.js 的事件循环"
→ 品味维度：魔幻现实感/异步链式/非线性叙事。跨域推荐：博尔赫斯《小径分岔的花园》、RxJS、《云图》。

**knowpitch** — "kp11 机器学习"
→ 输出 4-2-3-1 阵型：主教练=从数据到泛化，GK=线性代数，CB=概率论，CDM=梯度下降，CAM=偏差方差权衡，CF=泛化误差，SVG 阵型图。

**spar** — "spar Go 并发"
→ 出题："goroutine 和线程的区别？" 答完追问："那 GMP 模型里 M 阻塞了怎么办？" 再追问："channel 关闭后还能收吗？" 最后评分卡。

**poke** — "我觉得微服务一定比单体好"
→ "你说的'一定'，在什么规模下不成立？" 答完再问："那两个服务频繁调用怎么办？" 直到你自己发现边界。

**trace** — "trace：订单接口昨天凌晨慢了 5 秒又自己好了"
→ 先问现象，沿因果链倒推：慢查询？GC？连接池？DNS？每层要证据，区分根因/触发条件/症状，最后给止血+根治+防复发。

**vet** — "vet 这篇文章说 Redis 单线程是因为网络 IO 瓶颈"
→ 审查：证据来源？是否混淆了 Redis 6.0 前/后？逻辑跳步？反方论点？可信度评级：中。

**memo** — "记一下：我们决定用 Postgres 因为 JSONB"
→ 自动更新 MEMO.md 的"关键决策"段，追加不覆盖，git commit。

**pulse** — "pulse 一下"
→ 输出 5 段 ≤12 行：正在做 X、今天完成 Y、接下来 Z、等你做 W、一句话主线。

**panel** — "panel：我要 Go 重写整个 Python 后端"
→ 用户视角/魔鬼代言人/技术现实派/未来视角各挑一个真问题，最后分必须改/可讨论/可忽略。

**baton** — "baton"
→ 扫项目生成 HANDOVER.md：怎么跑、做到哪、关键决策、坑、接手第一件事，git commit。

## Development

```bash
# Run validation (also runs on every PR via GitHub Actions)
python scripts/validate.py

# Run LLM evals (requires OPENAI_API_KEY; runs automatically on push/PR)
OPENAI_API_KEY=sk-... python scripts/run-evals.py
```

### Adding a new skill

1. Create `skills/<category>/<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`).
2. Add the path to `skills` array in `.claude-plugin/plugin.json`.
3. Run `python scripts/validate.py` — it must pass.
4. Open a PR. CI must be green before merge.

## License

MIT
