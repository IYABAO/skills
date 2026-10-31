# baton 交接（baton）— Skill Card

- **Type**: Claude Code Skill / Agent Skill
- **Name**: baton
- **Version**: 0.1.0
- **License**: MIT
- **Homepage**: https://github.com/IYABAO/skills
- **Triggers**: `baton` + 主题/方向
- **Requirements**: 无外部依赖（纯提示词技能）

> 本 skill 属于 **IYABAO Skills 插件市场**（共 11 个 learning/productivity skills），作者主页看全套：https://github.com/IYABAO/skills

## 一句话介绍

项目完整交接。扫项目目录生成 HANDOVER.md：项目是什么、怎么跑、做到哪、TODO、关键决策、坑，下个人不看聊天记录也能接手。

## 核心能力

- **自动扫项目目录结构**
- 汇总：项目定位/启动方式/当前状态/TODO/决策/坑
- 输出 HANDOVER.md 到项目根
- git 仓库自动 commit

## 何时使用

- 项目要交出去/换人接手
- 结束一个长期项目要存档

## 何时不要使用

- 项目刚开始还没东西交
- 日常进度报告（用 pulse）

## 包内容

```
skills/productivity/baton/
├── SKILL.md       # 技能说明（含 frontmatter metadata）
└── skill-card.md  # 本卡片
```

## 安全说明

只读项目文件生成交接文档，不删除任何东西。
