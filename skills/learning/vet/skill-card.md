# vet 审源（vet）— Skill Card

- **Type**: Claude Code Skill / Agent Skill
- **Name**: vet
- **Version**: 0.1.0
- **License**: MIT
- **Homepage**: https://github.com/IYABAO/skills
- **Triggers**: `vet` + 主题/方向
- **Requirements**: 无外部依赖（纯提示词技能）

> 本 skill 属于 **IYABAO Skills 插件市场**（共 11 个 learning/productivity skills），作者主页看全套：https://github.com/IYABAO/skills

## 一句话介绍

信息审查。像 vetting 候选人一样审一篇文章/论文/技术方案，出审查报告：证据、逻辑、隐藏前提、反方论点、利益冲突。

## 核心能力

- **证据是否充分、来源可不可靠**
- 逻辑有没有跳步、隐藏前提是什么
- 反方最强论点是什么
- 作者有没有利益冲突
- 给可信度评级

## 何时使用

- 看到一篇文章/论文想判断靠不靠谱
- 采纳技术方案前自审

## 何时不要使用

- 已经确认可靠的内容
- 纯新闻摘要

## 包内容

```
skills/learning/vet/
├── SKILL.md       # 技能说明（含 frontmatter metadata）
└── skill-card.md  # 本卡片
```

## 安全说明

纯提示词技能。
