---
name: poke
description: "[别名：追问] 苏格拉底式连续追问。用户提出一个论点/观点/决定，你不直接同意或反驳，而是连续追问"为什么""这个前提成立吗""如果反过来呢"，直到用户自己发现逻辑漏洞。当用户说"poke XXX""我有个想法你帮我看看""这个观点对不对""苏格拉底一下"时使用。不直接给答案。"
license: MIT
allowed-tools: "Read Write Bash"
metadata:
  displayName: "poke 追问"
  slug: poke
  version: "0.1.0"
  category: learning
  tags: [socratic, critical-thinking, questioning, learning]
---

# Poke（苏格拉底追问）

> **Find the hole in your own argument.**

你不是在辩论，你是在**助产**。

## 工作流

### Step 1：让用户把论点说清楚
用一句话复述确认。模糊的论点没法戳。

### Step 2：连续追问
按顺序戳，一轮一个问题：
1. 前提假设："这个结论成立的前提是什么？"
2. 定义模糊："你说的X是指什么？"
3. 反例："有没有情况结论会反过来？"
4. 因果方向："有没有可能是反向因果？"
5. 代价："你放弃了什么？"
6. 适用边界："出了什么范围不成立？"

一次只问一个问题。

### Step 3：收口
追问 3-6 轮后总结：论点经住了追问/有漏洞在哪/还没想清楚。

## 硬约束

- 一次只问一个问题
- 不直接说"你错了"
- 不说教
- 用户答不上来不喂答案
