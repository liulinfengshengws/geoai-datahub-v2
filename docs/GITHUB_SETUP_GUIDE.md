# GitHub仓库配置指南

## 🚀 快速开始

### 1. 创建GitHub仓库
1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `geoai-datahub-v2`
   - **Description**: `GeoAI DataHub v2 - 遥感/GIS AI运营解决方案`
   - **Visibility**: Public (推荐) 或 Private
   - **Initialize with**: 不要初始化 (我们已经有了本地仓库)
3. 点击"Create repository"

### 2. 添加远程仓库到本地项目
```bash
cd /home/openclaw/geoai-datahub-v2
git remote add origin https://github.com/YOUR_USERNAME/geoai-datahub-v2.git
```

### 3. 推送代码到GitHub
```bash
git push -u origin main
```

### 4. 配置GitHub Secrets (可选但推荐)
为了每日报告正常工作，建议配置以下Secrets：

1. 进入仓库 Settings → Secrets and variables → Actions
2. 添加以下Secrets:

| Secret名称 | 说明 | 是否必需 |
|------------|------|----------|
| `FEISHU_WEBHOOK_URL` | 飞书Webhook地址，用于发送通知 | 否 |
| `GITHUB_TOKEN` | 自动生成，用于创建Issue | 自动 |

## 🔧 GitHub Actions配置说明

### 每日进度更新工作流
位置: `.github/workflows/daily-progress-update.yml`

**触发条件**:
- 每天北京时间21:00自动运行 (13:00 UTC)
- 支持手动触发

**工作流程**:
1. 检出代码库
2. 生成每日进度报告
3. 更新项目状态总览
4. 提交并推送变更
5. 创建GitHub Issue供审阅
6. (可选) 发送飞书通知

### 手动运行
```bash
# 手动触发今日报告
git push origin main
# 然后在GitHub仓库的Actions标签页中，找到"Daily Progress Update"工作流，点击"Run workflow"
```

## 📊 每日报告系统

### 报告生成机制
- **时间**: 每天21:00自动生成
- **内容**: 基于Git提交历史、任务状态、风险分析
- **输出**:
  1. `docs/daily-reports/YYYY-MM-DD.md` - 详细报告
  2. `docs/PROJECT_STATUS.md` - 项目状态总览
  3. GitHub Issue - 供讨论和审阅

### 报告内容包含
1. 📋 今日概览 - 关键指标
2. 📊 进度指标 - 任务完成情况
3. ⚠️ 风险与问题 - 风险识别
4. 🚀 下一步计划 - 明日任务
5. 📈 趋势分析 - 进度趋势
6. 🔍 详细数据 - 完整数据

## 🛠️ 自定义配置

### 调整报告时间
编辑 `.github/workflows/daily-progress-update.yml`:
```yaml
on:
  schedule:
    # 每天北京时间09:00执行 (01:00 UTC)
    - cron: '0 1 * * *'
```

### 修改报告模板
编辑 `scripts/generate_daily_report.py`:
- 修改报告结构和内容
- 添加自定义指标
- 调整分析逻辑

### 添加通知渠道
1. **飞书**: 配置`FEISHU_WEBHOOK_URL` secret
2. **Slack/Discord**: 修改工作流添加相应步骤
3. **邮件**: 使用GitHub的邮件通知

## 🔍 监控和调试

### 查看工作流运行
1. 访问仓库的"Actions"标签页
2. 点击"Daily Progress Update"
3. 查看最新运行记录和日志

### 常见问题排查

#### 问题1: 工作流没有自动运行
- 检查: 仓库设置中Actions是否启用
- 检查: Schedule事件是否配置正确
- 检查: 主分支名称是否为`main`

#### 问题2: 报告生成失败
- 检查: Python脚本执行权限
- 检查: 依赖包是否安装
- 检查: Git历史记录是否可用

#### 问题3: Issue没有创建
- 检查: `GITHUB_TOKEN`权限
- 检查: Issue创建权限
- 检查: 报告文件是否存在

### 日志位置
- GitHub Actions运行日志
- 脚本输出日志
- 生成的报告文件

## 📈 数据备份和恢复

### 备份策略
- 所有报告存储在Git仓库中，自动备份
- 项目状态实时更新
- 历史报告可随时查看

### 数据恢复
```bash
# 恢复特定日期的报告
git checkout docs/daily-reports/2026-04-14.md

# 查看历史状态
git log --oneline docs/PROJECT_STATUS.md
```

## 🔄 与其他工具集成

### 与项目管理工具集成
1. **GitHub Projects**: 自动创建卡片和更新状态
2. **Jira/Trello**: 通过Webhook同步任务状态
3. **Notion**: 通过API同步报告内容

### 与监控工具集成
1. **Prometheus/Grafana**: 导出指标数据
2. **Datadog**: 发送自定义指标
3. **Sentry**: 错误跟踪和报告

## 🎯 最佳实践

### 代码管理
1. **每日提交**: 确保每天有代码变更
2. **提交信息规范**: 清晰的提交信息便于分析
3. **分支策略**: 使用功能分支，定期合并到main

### 文档管理
1. **及时更新**: 任务状态变化时更新文档
2. **版本控制**: 所有文档纳入Git管理
3. **链接关联**: 文档间建立清晰链接

### 团队协作
1. **每日审阅**: 团队审阅每日报告
2. **问题跟踪**: 通过GitHub Issue跟踪问题
3. **透明沟通**: 保持进度透明，及时沟通

## 📝 维护指南

### 定期维护任务
1. **每周**: 检查工作流运行状态
2. **每月**: 清理旧Issue，归档报告
3. **每季度**: 评估系统效果，优化配置

### 系统升级
1. **依赖更新**: 定期更新Python依赖
2. **脚本优化**: 根据使用反馈优化脚本
3. **功能增强**: 添加新的分析指标

### 故障处理
1. **立即响应**: 工作流失败时立即检查
2. **问题定位**: 查看日志，定位问题原因
3. **快速修复**: 提交修复，重新运行

## 🔗 相关资源

### 官方文档
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [GitHub REST API文档](https://docs.github.com/en/rest)
- [Python GitHub API](https://github.com/PyGithub/PyGithub)

### 参考项目
- [自动化报告示例](https://github.com/actions/starter-workflows)
- [进度监控模板](https://github.com/marketplace?type=actions)
- [GIS项目示例](https://github.com/topics/gis)

### 社区支持
- [GitHub社区论坛](https://github.community/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/github-actions)
- [中文GitHub社区](https://github.com/orgs/china-github/discussions)

---

## 🎉 完成配置

### 验证配置
1. 推送代码到GitHub
2. 手动触发工作流运行
3. 检查生成的报告和Issue
4. 确认自动调度正常工作

### 开始使用
```bash
# 1. 每日开发工作
# 2. 提交代码变更
# 3. GitHub Actions自动生成报告
# 4. 审阅报告，调整计划
```

### 获取帮助
- 查看本指南
- 检查示例配置
- 查阅相关文档
- 联系项目团队

---

**最后更新**: 2026-04-14
**版本**: v1.0

*配置完成后，项目将实现每日自动进度更新，提高透明度和协作效率。*