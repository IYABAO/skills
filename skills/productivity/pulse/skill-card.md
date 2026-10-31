# pulse 报进度（pulse）— Skill Card

- **Type**: Claude Code Skill / Agent Skill
- **Name**: pulse
- **Version**: 0.1.0
- **License**: MIT
- **Homepage**: https://github.com/IYABAO/skills
- **Triggers**: `pulse` + 主题/方向
- **Requirements**: 无外部依赖（纯提示词技能）

> 本 skill 属于 **IYABAO Skills 插件市场**（共 11 个 learning/productivity skills），作者主页看全套：https://github.com/IYABAO/skills

## 一句话介绍

30 秒工作进度报告。有项目目录自动读 AGENTS.md/active/日报，没有就从对话上下文总结，5 段固定输出。

## 核心能力

- **自动找进度文件（AGENTS.md/active.md/日报）**
- 5 段：正在做/今天完成/接下来/等你/一句话
- 找不到文件就明说，不编进度
- ≤12 行，30 秒读完

## 何时使用

- 聊久了不知道整体进度
- standup/周报要快速报状态

## 何时不要使用

- 要详细分析（另起任务）
- 晚上 22 点后还想接新活

## 包内容

```
skills/productivity/pulse/
├── SKILL.md       # 技能说明（含 frontmatter metadata）
└── skill-card.md  # 本卡片
```

## 安全说明

只读项目文件，不写档。
