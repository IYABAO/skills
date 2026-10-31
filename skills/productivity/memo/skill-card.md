# memo 备忘（memo）— Skill Card

- **Type**: Claude Code Skill / Agent Skill
- **Name**: memo
- **Version**: 0.1.0
- **License**: MIT
- **Homepage**: https://github.com/IYABAO/skills
- **Triggers**: `memo` + 主题/方向
- **Requirements**: 无外部依赖（纯提示词技能）

> 本 skill 属于 **IYABAO Skills 插件市场**（共 11 个 learning/productivity skills），作者主页看全套：https://github.com/IYABAO/skills

## 一句话介绍

文件记忆 + 上下文持久化。在项目根自动建 MEMO.md（当前状态/已完成/下一步/等用户/关键决策），关键节点更新并 git commit，换会话/换 agent 不丢上下文。

## 核心能力

- **首次用自动在项目根建 MEMO.md**
- 5 段固定结构：状态/已完成/下一步/等用户/决策
- 关键节点追加更新，不覆盖历史
- git 仓库自动 commit，不是 git 提示 init

## 何时使用

- 长项目要跨会话/跨 agent 接力
- 怕聊到后面忘了前面做到哪

## 何时不要使用

- 一次性短任务（没必要建档）
- 个人日记

## 包内容

```
skills/productivity/memo/
├── SKILL.md       # 技能说明（含 frontmatter metadata）
└── skill-card.md  # 本卡片
```

## 安全说明

只写项目根 MEMO.md，不访问其他路径。
