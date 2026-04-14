#!/bin/bash
# 运行每日进度报告生成脚本

cd "$(dirname "$0")/.."
python3 scripts/generate_daily_report.py "$@"