# spar 对练（spar）— Skill Card

- **Type**: Claude Code Skill / Agent Skill
- **Name**: spar
- **Version**: 0.1.0
- **License**: MIT
- **Homepage**: https://github.com/IYABAO/skills
- **Triggers**: `spar` + 主题/方向
- **Requirements**: 无外部依赖（纯提示词技能）

> 本 skill 属于 **IYABAO Skills 插件市场**（共 11 个 learning/productivity skills），作者主页看全套：https://github.com/IYABAO/skills

## 一句话介绍

模拟技术面试对练。给定方向出一道题，连环追问直到你答不下去，最后给评分卡。不喂答案。

## 核心能力

- **出一道技术题（Go 并发/系统设计/数据库）**
- 连环追问你的答案，不接受模糊回答
- 答不上来的点记下来当回去补的作业
- 最后评分卡：哪类题强、哪类弱

## 何时使用

- 准备技术面试、想找人 mock 一下
- 想知道自己哪个知识点会被问穿

## 何时不要使用

- 想直接要答案/想复习知识点（用 drill）
- 非技术岗面试

## 包内容

```
skills/learning/spar/
├── SKILL.md       # 技能说明（含 frontmatter metadata）
└── skill-card.md  # 本卡片
```

## 安全说明

纯提示词技能，无脚本、无网络请求。
