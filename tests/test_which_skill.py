#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contract tests for scripts/which_skill.py.

The router is user-facing: one natural-language task should return the
skill a user should invoke, plus the words that matched. These tests pin
one representative query per skill so adding a new skill without a route
fails CI instead of silently degrading the command.
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "which_skill.py"


def run_cli(*args):
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=str(ROOT),
        text=True,
        encoding="utf-8",
        capture_output=True,
        env=env,
    )


class WhichSkillTest(unittest.TestCase):
    def test_all_eleven_skills_have_a_routing_sample(self):
        cases = {
            "drill": "我想系统学习向量数据库，从零到专家，给我一条学习路线",
            "knowpitch": "kp11 机器学习，用足球阵型讲透",
            "liken": "我喜欢《百年孤独》和手冲咖啡，帮我找类似的",
            "spar": "spar Go 并发，模拟面试",
            "poke": "我有个观点：微服务一定比单体好，帮我看看逻辑漏洞",
            "trace": "线上订单接口昨天慢 5 秒，帮我查根因",
            "vet": "帮我审一下这篇论文，证据靠谱吗",
            "memo": "记一下进度，写个备忘，别丢上下文",
            "pulse": "pulse 一下，报进度",
            "panel": "panel 多角色评审这个方案",
            "baton": "项目要交接，写 HANDOVER.md",
        }
        for expected, query in cases.items():
            with self.subTest(skill=expected, query=query):
                result = run_cli("--json", query)
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                actual = payload["recommendations"][0]["name"]
                self.assertEqual(actual, expected, payload)

    def test_json_output_contract(self):
        result = run_cli("--json", "线上订单接口昨天慢 5 秒，帮我查根因")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["query"], "线上订单接口昨天慢 5 秒，帮我查根因")
        top = payload["recommendations"][0]
        self.assertEqual(top["name"], "trace")
        self.assertGreater(top["score"], 0)
        self.assertTrue(top["matched"])
        self.assertIn("trace", top["usage"])
        self.assertIn("path", top)
        self.assertIn("description", top)

    def test_unknown_task_returns_exit_2_and_no_match(self):
        result = run_cli("--json", "今天晚饭吃什么")
        self.assertEqual(result.returncode, 2, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["recommendations"], [])
        self.assertIn("没有明确匹配", payload["message"])

    def test_list_contains_all_plugin_skills_once(self):
        result = run_cli("--list", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        names = [item["name"] for item in payload["skills"]]
        self.assertEqual(len(names), 11)
        self.assertEqual(len(set(names)), 11)
        for required in ["drill", "knowpitch", "liken", "spar", "poke", "trace",
                         "vet", "memo", "pulse", "panel", "baton"]:
            self.assertIn(required, names)

    def test_plugin_and_marketplace_names_are_consistent(self):
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["name"], market["name"])
        self.assertEqual(market["plugins"][0]["name"], plugin["name"])
        self.assertEqual(len(plugin["skills"]), 11)


if __name__ == "__main__":
    unittest.main(verbosity=2)
