#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pick the right skill for a task.

The plugin ships 11 overlapping-looking skills. This command turns a natural
language task into a deterministic first choice, the words that matched, and a
copy-paste invocation. It is offline and dependency-free.

Usage:
  python scripts/which_skill.py "线上订单接口慢 5 秒，帮我查根因"
  python scripts/which_skill.py --json "我喜欢《百年孤独》和手冲咖啡"
  python scripts/which_skill.py --list
  python scripts/which_skill.py --list --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_JSON = ROOT / ".claude-plugin" / "plugin.json"


def _stdout_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def _frontmatter(text: str) -> str:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return match.group(1) if match else ""


def _field(frontmatter: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}\s*:\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def load_skills() -> list[dict]:
    plugin = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    skills = []
    for order, rel in enumerate(plugin.get("skills", [])):
        skill_dir = ROOT / rel
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        name = _field(fm, "name") or skill_dir.name
        parts = Path(rel).parts
        category = parts[1] if len(parts) >= 3 else ""
        skills.append({
            "name": name,
            "display_name": _field(fm, "displayName") or name,
            "description": _field(fm, "description"),
            "category": category,
            "path": rel,
            "order": order,
        })
    return skills


# One rule per skill. Aliases are the explicit trigger words from SKILL.md.
# Patterns carry the weight; a generic word like "推荐" must not outrank a
# specific phrase like "模拟面试".
ROUTE_RULES: list[dict] = [
    {
        "name": "drill",
        "aliases": ["drill", "钻取", "深挖", "吃透"],
        "patterns": [
            (r"学习(路线|路径|地图)", 10, "学习路线"),
            (r"(从零|入门|新手).*(学|掌握|专家)", 8, "从零到专家"),
            (r"(专家|精通).*(路径|路线)", 8, "专家路径"),
            (r"(怎么|如何|从哪)(学|入门)", 6, "怎么学"),
            (r"(系统|深入)(学习|掌握)", 6, "系统学习"),
            (r"(权威)?(资源|书单|教程|课程)", 6, "学习资源"),
        ],
    },
    {
        "name": "knowpitch",
        "aliases": ["knowpitch", "kp11", "kpt", "kps", "kpitch", "阵型", "球员卡"],
        "patterns": [
            (r"足球|球队|阵型|战术板|主教练|门将|球员", 8, "足球阵型"),
            (r"讲透|大白话|eli5|比喻", 8, "讲透"),
            (r"知识.*(拆解|拆成)|拆成.*球队", 6, "知识拆解"),
        ],
    },
    {
        "name": "liken",
        "aliases": ["liken", "知音"],
        "patterns": [
            (r"喜欢.*(书|电影|音乐|app|咖啡|城市|东西|作品)", 8, "喜欢的东西"),
            (r"(类似|相似|同类|跨域)", 8, "找同类"),
            (r"(品味|口味|气质)", 6, "品味画像"),
            (r"推荐.*(书|电影|音乐|咖啡|城市)", 6, "跨域推荐"),
        ],
    },
    {
        "name": "spar",
        "aliases": ["spar", "对练"],
        "patterns": [
            (r"(模拟|技术|面试).*(面试|对练|练)|考我|评分卡", 10, "模拟面试"),
            (r"(追问|连环追问).*(回答|答)", 6, "连环追问"),
        ],
    },
    {
        "name": "poke",
        "aliases": ["poke", "苏格拉底"],
        "patterns": [
            (r"(观点|论点|想法).*(看看|对不对|有问题|成立)", 8, "观点检验"),
            (r"逻辑漏洞|前提.*成立|反过来", 8, "逻辑漏洞"),
            (r"追问|反驳", 4, "追问"),
        ],
    },
    {
        "name": "trace",
        "aliases": ["trace", "追因"],
        "patterns": [
            (r"根因|根因分析", 10, "根因"),
            (r"bug|报错|故障|事故|异常", 8, "故障现象"),
            (r"线上.*(慢|挂|错|失败)|排查|为什么.*(慢|错|失败|挂)", 6, "线上排查"),
        ],
    },
    {
        "name": "vet",
        "aliases": ["vet", "审源"],
        "patterns": [
            (r"审查|审一下|审一审", 8, "审查"),
            (r"(论文|文章|方案|观点).*(靠谱|证据|逻辑|质量)", 8, "证据审查"),
            (r"证据.*(充分|质量)|逻辑.*(跳步|漏洞)|利益冲突|反方", 6, "证据与逻辑"),
        ],
    },
    {
        "name": "memo",
        "aliases": ["memo", "备忘"],
        "patterns": [
            (r"备忘|记忆|存档", 8, "记忆"),
            (r"上下文|别丢|恢复.*(进度|上下文)", 8, "上下文"),
            (r"进度.*(记录|存档)|MEMO\.md", 6, "进度存档"),
        ],
    },
    {
        "name": "pulse",
        "aliases": ["pulse", "报进度"],
        "patterns": [
            (r"报进度|工作状态|standup", 10, "报进度"),
            (r"现在.*(干什么|做什么)|今天.*(做了|完成)|接下来.*(计划|干嘛)", 8, "进度汇报"),
            (r"聊到哪|进度怎么样", 6, "进度"),
        ],
    },
    {
        "name": "panel",
        "aliases": ["panel", "评审"],
        "patterns": [
            (r"多角色|不同.*角度|魔鬼代言人|技术现实派", 10, "多角色"),
            (r"(方案|计划|设计).*(评审|审查)|评审.*(方案|计划|设计)", 8, "方案评审"),
            (r"可行性.*(审查|评估)|风险.*(角度|评估)|挑问题", 6, "风险评审"),
        ],
    },
    {
        "name": "baton",
        "aliases": ["baton", "交接"],
        "patterns": [
            (r"交接|handover|接手|换人", 10, "交接"),
            (r"项目.*(交出去|交接)|新人.*(上手|接手)|HANDOVER\.md", 8, "项目交接"),
            (r"写.*交接文档|下一个人.*上手", 6, "交接文档"),
        ],
    },
]


def _find_rule(name: str) -> dict | None:
    for rule in ROUTE_RULES:
        if rule["name"] == name:
            return rule
    return None


def score_skills(query: str, skills: list[dict]) -> list[dict]:
    query_l = query.lower()
    results = []
    for skill in skills:
        rule = _find_rule(skill["name"])
        if not rule:
            continue
        score = 0
        matched: list[str] = []

        for alias in rule["aliases"]:
            if alias.lower() in query_l:
                score += 25
                matched.append(alias)

        for pattern, weight, label in rule["patterns"]:
            if re.search(pattern, query, re.IGNORECASE | re.DOTALL):
                score += weight
                if label not in matched:
                    matched.append(label)

        if score > 0:
            results.append({
                "name": skill["name"],
                "display_name": skill["display_name"],
                "score": score,
                "matched": matched,
                "usage": f"{skill['name']} {query}",
                "path": skill["path"],
                "description": skill["description"],
                "order": skill["order"],
            })

    results.sort(key=lambda item: (-item["score"], item["order"]))
    for item in results:
        item.pop("order", None)
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="根据任务描述选择最合适的 skill（离线关键词路由）")
    parser.add_argument("query", nargs="?", help="自然语言任务描述")
    parser.add_argument("--json", action="store_true", help="输出 JSON，便于脚本消费")
    parser.add_argument("--list", action="store_true", help="列出全部 skill")
    args = parser.parse_args(argv)

    _stdout_utf8()
    skills = load_skills()
    if not skills:
        print("没有从 .claude-plugin/plugin.json 读到任何 skill", file=sys.stderr)
        return 1

    if args.list:
        payload = {"skills": [
            {k: skill[k] for k in ("name", "display_name", "category", "path")}
            for skill in skills
        ]}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            for skill in skills:
                print(f"{skill['name']:<12} {skill['display_name']:<16} {skill['path']}")
        return 0

    if not args.query or not args.query.strip():
        parser.print_usage()
        print("请提供任务描述，例如：python scripts/which_skill.py \"线上订单接口慢 5 秒\"")
        return 1

    query = args.query.strip()
    recommendations = score_skills(query, skills)[:3]
    payload = {
        "query": query,
        "recommendations": recommendations,
        "message": "没有明确匹配的 skill，请补充任务类型或先用 --list 查看全部 skill" if not recommendations else "ok",
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"查询：{query}")
        if not recommendations:
            print(payload["message"])
        else:
            top = recommendations[0]
            print(f"首选：{top['display_name']} ({top['name']})  分数 {top['score']}")
            print(f"命中：{'、'.join(top['matched'])}")
            print(f"调用：{top['usage']}")
            if len(recommendations) > 1:
                others = "，".join(
                    f"{item['name']}({item['score']})" for item in recommendations[1:]
                )
                print(f"备选：{others}")

    return 0 if recommendations else 2


if __name__ == "__main__":
    raise SystemExit(main())
