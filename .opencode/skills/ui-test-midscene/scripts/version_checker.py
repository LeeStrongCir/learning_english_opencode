#!/usr/bin/env python3
"""
UI Test Midscene Skill 版本检查与更新脚本

用法:
  python3 version_checker.py              # 检查更新并执行更新
  python3 version_checker.py --check-only # 仅检查，不更新
  python3 version_checker.py --version    # 显示当前版本
"""

import os
import sys
import json
import argparse
from datetime import datetime

SKILL_NAME = "ui-test-midscene"
CURRENT_VERSION = "0.1.0"
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_JSON_PATH = os.path.join(os.path.dirname(SKILL_DIR), "skill.json")


def get_current_version():
    """从 skill.json 读取当前版本"""
    if os.path.exists(SKILL_JSON_PATH):
        with open(SKILL_JSON_PATH, "r") as f:
            data = json.load(f)
            return data.get("version", CURRENT_VERSION)
    return CURRENT_VERSION


def check_update():
    """检查是否有可用更新"""
    # 当前版本
    version = get_current_version()
    print(f"📦 {SKILL_NAME} 当前版本: {version}")

    # TODO: 实现远程版本检查逻辑
    # 目前仅做本地版本显示
    print("✅ 版本检查完成（远程检查功能待实现）")
    return False


def update():
    """执行更新"""
    print(f"🔄 更新 {SKILL_NAME}...")

    # 确保目录结构完整
    refs_dir = os.path.join(os.path.dirname(SKILL_DIR), "references")
    scripts_dir = os.path.dirname(SKILL_DIR)

    required_files = [
        os.path.join(os.path.dirname(SKILL_DIR), "SKILL.md"),
        os.path.join(refs_dir, "midscene-api-reference.md"),
        os.path.join(refs_dir, "model-config-guide.md"),
        os.path.join(refs_dir, "test-patterns.md"),
    ]

    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print(f"⚠️  缺少文件: {missing}")
        return False

    print("✅ 所有文件完整")
    return True


def main():
    parser = argparse.ArgumentParser(description=f"{SKILL_NAME} 版本管理")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="仅检查版本，不执行更新",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="显示当前版本",
    )
    args = parser.parse_args()

    if args.version:
        print(get_current_version())
        return 0

    if args.check_only:
        has_update = check_update()
        return 1 if has_update else 0

    # 默认行为：检查并更新
    has_update = check_update()
    if has_update:
        update()

    return 0


if __name__ == "__main__":
    sys.exit(main())
