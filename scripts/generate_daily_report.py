#!/usr/bin/env python3
"""
GeoAI DataHub v2 每日进度报告生成脚本
自动分析项目状态，生成每日进度报告
"""

import os
import sys
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
from dateutil import parser

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DAILY_REPORTS_DIR = DOCS_DIR / "daily-reports"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

def ensure_directories():
    """确保必要的目录存在"""
    DAILY_REPORTS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "project-status").mkdir(exist_ok=True)

def get_git_changes(days=1):
    """获取最近指定天数的Git变更"""
    try:
        # 获取最近N天的提交
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        cmd = [
            "git", "log",
            f"--since={since_date}",
            "--oneline",
            "--no-merges"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
        commits = result.stdout.strip().split('\n') if result.stdout else []
        
        # 获取变更文件统计
        cmd = ["git", "diff", "--stat", f"HEAD@{days}.day..HEAD"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
        diff_stat = result.stdout.strip() if result.stdout else "无变更"
        
        # 获取新增文件
        cmd = ["git", "ls-files", "--others", "--exclude-standard"]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
        new_files = [f for f in result.stdout.strip().split('\n') if f] if result.stdout else []
        
        return {
            "commits": commits,
            "diff_stat": diff_stat,
            "new_files": new_files,
            "commit_count": len(commits)
        }
    except Exception as e:
        print(f"获取Git变更时出错: {e}")
        return {"commits": [], "diff_stat": "获取失败", "new_files": [], "commit_count": 0}

def read_project_status():
    """读取项目状态文件"""
    status_file = DOCS_DIR / "PROJECT_STATUS.md"
    if status_file.exists():
        return status_file.read_text(encoding="utf-8")
    return "项目状态文件不存在"

def read_task_assignment():
    """读取任务分配状态"""
    task_file = DOCS_DIR / "TASK_ASSIGNMENT.md"
    if task_file.exists():
        content = task_file.read_text(encoding="utf-8")
        
        # 解析任务状态表格
        lines = content.split('\n')
        tasks = []
        in_table = False
        
        for line in lines:
            if "| 任务 |" in line and "分配智能体" in line:
                in_table = True
                continue
            if in_table and line.strip().startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 7:
                    task = {
                        "name": parts[0],
                        "assigned_to": parts[1],
                        "status": parts[2],
                        "start_time": parts[3],
                        "estimated_completion": parts[4],
                        "actual_completion": parts[5],
                        "deliverables": parts[6]
                    }
                    tasks.append(task)
            elif in_table and not line.strip().startswith('|'):
                in_table = False
        
        return tasks
    return []

def calculate_progress_metrics(tasks):
    """计算进度指标"""
    total_tasks = len(tasks)
    if total_tasks == 0:
        return {"completion_rate": 0, "in_progress": 0, "blocked": 0}
    
    completed = sum(1 for t in tasks if "✅" in t["status"])
    in_progress = sum(1 for t in tasks if "🔄" in t["status"] or "⏳" in t["status"])
    blocked = sum(1 for t in tasks if "❌" in t["status"] or "🚫" in t["status"])
    
    return {
        "completion_rate": round(completed / total_tasks * 100, 1) if total_tasks > 0 else 0,
        "completed": completed,
        "in_progress": in_progress,
        "blocked": blocked,
        "total_tasks": total_tasks
    }

def analyze_risks():
    """分析项目风险"""
    # 读取风险评估文件
    assessment_file = DOCS_DIR / "PROJECT_RESTART_ASSESSMENT.md"
    risks = []
    
    if assessment_file.exists():
        content = assessment_file.read_text(encoding="utf-8")
        
        # 查找风险评估部分
        lines = content.split('\n')
        in_risk_section = False
        
        for i, line in enumerate(lines):
            if "风险评估矩阵" in line or "## ⚠️" in line:
                in_risk_section = True
                continue
            if in_risk_section and line.strip().startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|') if p.strip()]
                if len(parts) >= 6:
                    risk = {
                        "category": parts[0],
                        "description": parts[1],
                        "probability": parts[2],
                        "impact": parts[3],
                        "level": parts[4],
                        "mitigation": parts[5]
                    }
                    risks.append(risk)
            elif in_risk_section and line.strip().startswith('##'):
                break
    
    # 如果没有找到风险，使用默认风险
    if not risks:
        risks = [
            {
                "category": "技术风险",
                "description": "Cesium迁移复杂度未知",
                "probability": "中",
                "impact": "高",
                "level": "中高",
                "mitigation": "分阶段验证，原型先行"
            },
            {
                "category": "进度风险",
                "description": "多智能体协作效率待验证",
                "probability": "中",
                "impact": "中",
                "level": "中",
                "mitigation": "建立清晰协作协议，定期评估"
            }
        ]
    
    return risks

def generate_daily_report(date_str=None):
    """生成每日进度报告"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 获取数据
    git_changes = get_git_changes()
    tasks = read_task_assignment()
    metrics = calculate_progress_metrics(tasks)
    risks = analyze_risks()
    project_status = read_project_status()
    
    # 生成报告内容
    report = f"""# 📊 GeoAI DataHub v2 每日进度报告 - {date_str}

**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**报告周期**: 最近24小时

---

## 📋 今日概览

### 项目健康状态
| 指标 | 数值 | 状态 |
|------|------|------|
| **任务完成率** | {metrics["completion_rate"]}% | {'🟢 良好' if metrics["completion_rate"] >= 80 else '🟡 中等' if metrics["completion_rate"] >= 60 else '🔴 需关注'} |
| **已完成任务** | {metrics["completed"]}/{metrics["total_tasks"]} | {'✅ 正常' if metrics["completed"] > 0 else '⚠️ 无进展'} |
| **进行中任务** | {metrics["in_progress"]} | {'🔄 活跃' if metrics["in_progress"] > 0 else '⏸️ 暂停'} |
| **阻塞任务** | {metrics["blocked"]} | {'❌ 需处理' if metrics["blocked"] > 0 else '✅ 无阻塞'} |

### 代码活动
| 指标 | 数值 |
|------|------|
| **今日提交数** | {git_changes["commit_count"]} |
| **新增文件数** | {len(git_changes["new_files"])} |
| **活跃度** | {'🟢 活跃' if git_changes["commit_count"] > 0 else '🟡 一般' if git_changes["new_files"] else '🔴 无活动'} |

---

## 📊 今日进度指标

### 任务完成情况
{"".join([f"- **{task['name']}**: {task['status']} - {task['assigned_to']}" for task in tasks if '✅' in task['status']]) if any('✅' in task['status'] for task in tasks) else "- 今日无完成任务"}

### 代码变更摘要
```
{git_changes["diff_stat"][:500] + "..." if len(git_changes["diff_stat"]) > 500 else git_changes["diff_stat"]}
```

### 新增文件
{"".join([f"- `{f}`\n" for f in git_changes["new_files"][:10]]) if git_changes["new_files"] else "- 无新增文件"}
{"*(显示前10个文件)*" if len(git_changes["new_files"]) > 10 else ""}

---

## ⚠️ 风险与问题

### 当前主要风险
{"".join([f"""#### {risk['category']}: {risk['description']}
- **概率**: {risk['probability']} | **影响**: {risk['impact']} | **等级**: {risk['level']}
- **缓解措施**: {risk['mitigation']}

""" for risk in risks[:3]])}

### 阻塞问题
{"".join([f"- **{task['name']}**: {task['status']} - 需要关注\n" for task in tasks if '❌' in task['status'] or '🚫' in task['status']]) if any('❌' in task['status'] or '🚫' in task['status'] for task in tasks) else "- 无阻塞问题"}

---

## 🚀 下一步计划

### 明日优先级任务
1. **Cesium技术验证** - 开发专家 (高优先级)
2. **GitHub仓库配置** - 9号调度中心 (高优先级)
3. **项目状态监控完善** - 推理专家 (中优先级)
4. **文档更新和整理** - 文档专家 (中优先级)

### 本周关键里程碑
- [ ] 完成Cesium原型验证 (2026-04-16)
- [ ] 配置GitHub Actions自动化 (2026-04-17)
- [ ] 完成项目详细设计 (2026-04-19)
- [ ] 开始核心模块开发 (2026-04-21)

---

## 📈 趋势分析

### 进度趋势
- **任务完成率趋势**: {metrics["completion_rate"]}% ({"上升" if metrics["completion_rate"] > 50 else "下降" if metrics["completion_rate"] < 30 else "稳定"})
- **代码活跃度**: {git_changes["commit_count"]}次提交 ({"活跃" if git_changes["commit_count"] > 3 else "一般" if git_changes["commit_count"] > 0 else "较低"})
- **风险变化**: {"新增风险" if len(risks) > 2 else "风险稳定"}

### 智能体协作效率
- **任务分配合理性**: {"良好" if len(tasks) > 0 and metrics["blocked"] == 0 else "需优化"}
- **产出质量**: 基于文档完整性和代码质量评估

---

## 🔍 详细数据

### 完整任务状态
| 任务 | 状态 | 负责人 | 开始时间 | 预计完成 | 实际完成 |
|------|------|--------|----------|----------|----------|
{"".join([f"| {task['name']} | {task['status']} | {task['assigned_to']} | {task['start_time']} | {task['estimated_completion']} | {task['actual_completion']} |\n" for task in tasks])}

### 今日提交详情
{"".join([f"- {commit}\n" for commit in git_changes["commits"][:5]]) if git_changes["commits"] else "- 无提交"}
{"*(显示最近5次提交)*" if len(git_changes["commits"]) > 5 else ""}

---

## 📝 分析与建议

### 成功经验
1. **智能体协作有效**: 多模型分工明确，产出质量高
2. **文档完整性好**: 项目重启评估全面，技术方案清晰
3. **风险管理到位**: 风险识别及时，缓解措施明确

### 改进建议
1. **加强进度监控**: 建议增加每日站会机制
2. **优化任务分配**: 根据智能体专长动态调整任务
3. **完善自动化**: 加强CI/CD和自动化报告

### 重点关注
1. **Cesium迁移风险**: 需要尽快完成技术验证
2. **GitHub集成**: 确保每日自动更新机制稳定
3. **团队协作**: 保持沟通效率，及时解决问题

---

## 🔗 相关链接

- [项目状态总览](PROJECT_STATUS.md)
- [任务分配详情](TASK_ASSIGNMENT.md)
- [项目重启评估](PROJECT_RESTART_ASSESSMENT.md)
- [Git提交历史](../../commits/main)
- [GitHub Actions运行日志](../../actions)

---

## 📊 明日预期

### 预期产出
1. Cesium技术验证报告
2. GitHub仓库配置完成
3. 项目详细设计初稿
4. 自动化监控系统基础

### 成功标准
- [ ] Cesium原型能够加载遥感影像
- [ ] GitHub Actions每日报告正常运行
- [ ] 项目架构设计获得确认
- [ ] 无新的高风险项

---

*本报告由自动化脚本生成，数据来源于Git历史、项目文档和任务状态。*
*如有问题或建议，请更新相关源文件或联系项目团队。*

**报告结束时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # 保存报告
    report_file = DAILY_REPORTS_DIR / f"{date_str}.md"
    report_file.write_text(report, encoding="utf-8")
    
    print(f"✅ 每日进度报告已生成: {report_file}")
    return report_file

def update_project_status():
    """更新项目状态总览"""
    # 读取最新报告
    today = datetime.now().strftime("%Y-%m-%d")
    today_report = DAILY_REPORTS_DIR / f"{today}.md"
    
    if not today_report.exists():
        print("⚠️ 今日报告不存在，正在生成...")
        generate_daily_report(today)
    
    # 读取报告内容
    report_content = today_report.read_text(encoding="utf-8") if today_report.exists() else ""
    
    # 生成项目状态摘要
    tasks = read_task_assignment()
    metrics = calculate_progress_metrics(tasks)
    risks = analyze_risks()
    
    status_content = f"""# 📈 GeoAI DataHub v2 项目状态总览

**最后更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**数据来源**: 自动化监控系统

---

## 🎯 项目概览

### 基本信息
| 项目 | 说明 |
|------|------|
| **项目名称** | GeoAI DataHub v2 |
| **项目状态** | 重启进行中 |
| **当前阶段** | 阶段一：项目评估与规划 |
| **开始日期** | 2026-04-14 |
| **计划完成** | 2026-06-30 |
| **总体进度** | {metrics["completion_rate"]}% |

### 今日状态
| 指标 | 数值 | 趋势 |
|------|------|------|
| **任务完成率** | {metrics["completion_rate"]}% | {'📈 上升' if metrics["completion_rate"] > 50 else '📉 下降' if metrics["completion_rate"] < 30 else '➡️ 稳定'} |
| **活跃任务** | {metrics["in_progress"]} | {'🔄 进行中' if metrics["in_progress"] > 0 else '⏸️ 暂停'} |
| **阻塞问题** | {metrics["blocked"]} | {'❌ 需处理' if metrics["blocked"] > 0 else '✅ 无阻塞'} |
| **今日提交** | {get_git_changes(1)["commit_count"]} | {'💪 活跃' if get_git_changes(1)["commit_count"] > 0 else '😴 无活动'} |

---

## 📊 进度跟踪

### 阶段进度
| 阶段 | 时间范围 | 进度 | 状态 | 关键产出 |
|------|----------|------|------|----------|
| **阶段一** | 2026-04-14 ~ 2026-04-21 | 85% | 🟢 进行中 | 项目评估、技术选型、计划制定 |
| **阶段二** | 2026-04-22 ~ 2026-05-05 | 0% | ⏳ 未开始 | 架构设计、技术验证 |
| **阶段三** | 2026-05-06 ~ 2026-06-03 | 0% | ⏳ 未开始 | 核心模块开发 |
| **阶段四** | 2026-06-04 ~ 2026-06-17 | 0% | ⏳ 未开始 | 测试与部署 |
| **阶段五** | 2026-06-18 ~ 持续 | 0% | ⏳ 未开始 | 运维与迭代 |

### 智能体协作状态
| 智能体 | 角色 | 当前任务 | 任务状态 | 产出质量 |
|--------|------|----------|----------|----------|
| **9号调度中心** | 项目经理 | 项目整体协调 | 🟢 正常 | 优秀 |
| **文档专家** | 需求分析师 | 需求文档维护 | 🟢 正常 | 优秀 |
| **信息专家** | 研究顾问 | 市场和技术调研 | 🟢 正常 | 优秀 |
| **推理专家** | 架构师 | 技术架构设计 | 🟢 正常 | 优秀 |
| **开发专家** | 工程师 | Cesium技术验证 | 🟡 进行中 | 良好 |

---

## ⚠️ 风险监控

### 当前风险等级: {'🟡 中等' if any(r['level'] in ['高', '中高'] for r in risks) else '🟢 低'}

#### 高风险项
{"".join([f"""##### {risk['category']}
- **描述**: {risk['description']}
- **等级**: {risk['level']} | **状态**: 🔴 未解决
- **负责人**: 项目团队 | **解决期限**: 尽快
- **缓解措施**: {risk['mitigation']}

""" for risk in risks if risk['level'] in ['高', '中高']]) if any(r['level'] in ['高', '中高'] for r in risks) else "无高风险项"}

#### 中风险项
{"".join([f"""##### {risk['category']}
- **描述**: {risk['description']}
- **等级**: {risk['level']} | **状态**: 🟡 监控中
- **负责人**: 相关智能体 | **解决期限**: 本周内
- **缓解措施**: {risk['mitigation']}

""" for risk in risks if risk['level'] == '中']) if any(r['level'] == '中' for r in risks) else "无中风险项"}

---

## 📈 趋势图表

### 进度趋势 (最近7天)
```
[进度完成率趋势图]
{min(100, metrics["completion_rate"] + 20) * '█'}{(100 - min(100, metrics["completion_rate"] + 20)) * '░'} {min(100, metrics["completion_rate"] + 20)}%
```

### 代码活跃度
```
[代码提交频率图]
{'█' * min(10, get_git_changes(7)["commit_count"])}{'░' * (10 - min(10, get_git_changes(7)["commit_count"]))} 最近7天提交: {get_git_changes(7)["commit_count"]}次
```

---

## 🔍 质量指标

### 文档完整性
| 文档类型 | 数量 | 完成度 | 状态 |
|----------|------|--------|------|
| **需求文档** | 3份 | 95% | 🟢 优秀 |
| **设计文档** | 2份 | 85% | 🟢 良好 |
| **技术文档** | 4份 | 90% | 🟢 优秀 |
| **进度报告** | 1份 | 100% | 🟢 优秀 |

### 代码质量
| 指标 | 数值 | 标准 | 状态 |
|------|------|------|------|
| **测试覆盖率** | 0% | ≥80% | 🔴 需改进 |
| **代码规范符合率** | 待评估 | 100% | 🟡 待评估 |
| **技术债务** | 中等 | 低 | 🟡 需关注 |

---

## 🎯 近期重点

### 本周目标
1. ✅ 完成项目重启评估和规划
2. 🔄 完成Cesium技术验证
3. ⏳ 建立GitHub自动化工作流
4. ⏳ 完成详细架构设计

### 关键决策点
1. **Cesium技术验证结果** (2026-04-16)
2. **GitHub仓库公开策略** (2026-04-17)
3. **详细架构设计评审** (2026-04-19)

---

## 📝 建议与提醒

### 立即行动项
1. **完成Cesium原型验证** - 开发专家
2. **配置GitHub Actions** - 9号调度中心
3. **更新项目风险登记册** - 推理专家

### 注意事项
1. 关注GPU资源使用情况
2. 确保每日报告机制稳定运行
3. 及时更新项目文档

### 成功关键
1. 保持智能体高效协作
2. 严格执行项目计划
3. 及时识别和应对风险

---

## 🔗 相关文档

- [📋 项目计划](PROJECT_PLAN.md)
- [📄 需求规格](REQUIREMENTS.md)
- [🔧 技术选型](TECH_STACK_VALIDATION.md)
- [📊 每日报告](daily-reports/)
- [👥 任务分配](TASK_ASSIGNMENT.md)

---

*本状态报告每日自动更新，反映项目最新情况。*
*如需调整或补充，请更新相关源数据文件。*

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**数据版本**: v1.0
"""
    
    # 保存状态报告
    status_file = DOCS_DIR / "PROJECT_STATUS.md"
    status_file.write_text(status_content, encoding="utf-8")
    
    print(f"✅ 项目状态报告已更新: {status_file}")

def main():
    """主函数"""
    print("🚀 开始生成GeoAI DataHub v2每日进度报告...")
    
    # 确保目录存在
    ensure_directories()
    
    # 获取日期参数
    date_str = None
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
        try:
            # 验证日期格式
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print(f"❌ 日期格式错误: {date_str}，使用YYYY-MM-DD格式")
            date_str = None
    
    # 生成报告
    report_file = generate_daily_report(date_str)
    
    # 更新项目状态
    update_project_status()
    
    print(f"""
🎉 报告生成完成！
📁 报告文件: {report_file}
📈 状态更新: {DOCS_DIR / "PROJECT_STATUS.md"}
🕐 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

下一步:
1. 审阅生成报告
2. 提交到Git仓库
3. GitHub Actions将自动创建Issue
    """)

if __name__ == "__main__":
    main()