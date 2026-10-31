# trace 追因（trace）— Skill Card

- **Type**: Claude Code Skill / Agent Skill
- **Name**: trace
- **Version**: 0.1.0
- **License**: MIT
- **Homepage**: https://github.com/IYABAO/skills
- **Triggers**: `trace` + 主题/方向
- **Requirements**: 无外部依赖（纯提示词技能）

> 本 skill 属于 **IYABAO Skills 插件市场**（共 11 个 learning/productivity skills），作者主页看全套：https://github.com/IYABAO/skills

## 一句话介绍

根因追溯。给定 bug/事故/异常指标，沿因果链逐层倒推，每步要求证据，区分根因/触发条件/症状。

## 核心能力

- **沿因果链倒推，不接受"感觉是 X"**
- 每一步要求证据（日志/指标/配置）
- 区分根因、触发条件、表面症状
- 输出止血/根治/防复发三层建议

## 何时使用

- 线上出 bug 找不到真因
- 复盘事故要写 RCA

## 何时不要使用

- 只想快速止血（不追根因）
- 纯语法报错

## 包内容

```
skills/learning/trace/
├── SKILL.md       # 技能说明（含 frontmatter metadata）
└── skill-card.md  # 本卡片
```

## 安全说明

纯提示词技能。
