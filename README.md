# GeoAI DataHub v2 - 遥感/GIS AI运营解决方案

基于Paperclip/Edict混合架构和智能体协作框架重构的下一代遥感数据智能平台。

## 🎯 项目概述

### 核心定位
一站式GIS+遥感数据管理、处理、分析与智能搜索平台，聚焦遥感/GIS垂直领域，提供专业化的AI运营解决方案。

### 重启背景
- **原项目**: GeoAI DataHub (已取消，2026-04-07)
- **重启时间**: 2026-04-14
- **重启模式**: 基于多模型智能体协作系统的敏捷开发
- **架构升级**: 采用Paperclip(工作流) + Edict(交互)混合架构

## 🏗️ 系统架构

### 混合架构设计
```
用户界面层 (Edict风格) - 交互式状态管理，操作回滚
     ↓
API网关和状态管理层 - 统一接口，会话管理
     ↓
Paperclip工作流引擎层 - 模块化工作流，插件式扩展
     ↓
工具和模型服务层 - 专业工具链，AI模型服务
```

### 四大核心模块
1. **数据管理模块** - 多源数据接入、元数据管理、权限体系
2. **数据处理模块** - 预处理流水线、批量处理、质量控制
3. **数据分析模块** - 空间分析、时序分析、专题分析
4. **AI智能搜索模块** - 自然语言搜索、图像相似性搜索、智能推荐

## 👥 开发团队架构

### 智能体协作矩阵
| 角色 | 智能体 | 模型 | 职责 |
|------|--------|------|------|
| 项目经理 | 9号调度中心 | DeepSeek-V3 | 任务分解、进度协调、风险管理 |
| 架构师 | 推理专家 | DeepSeek-R1 | 技术架构、系统集成、测试策略 |
| 需求分析师 | 文档专家 | Qwen3.5-Plus | 需求分析、用户故事、文档管理 |
| 全栈工程师 | 开发专家 | Qwen3-Coder-Next | 前后端开发、数据库设计、部署 |
| 研究顾问 | 信息专家 | Kimi | 技术调研、竞品分析、趋势研究 |

## 📁 项目结构

```
openclaw-v2/
├── frontend/          # 前端代码 (Vue 3 + TypeScript + Cesium)
├── backend/           # 后端代码 (FastAPI + PostgreSQL + PostGIS)
├── data/              # 测试数据、配置文件
├── docs/              # 项目文档
├── config/            # 环境配置
├── deploy/            # 部署配置 (Docker, Kubernetes)
├── scripts/           # 开发工具脚本
└── .github/           # GitHub Actions工作流
```

## 🚀 技术栈

### 前端技术栈
- **框架**: Vue 3 + TypeScript + Vite
- **地图**: CesiumJS + 3D Tiles + GeoTIFF支持
- **UI组件**: Element Plus + Tailwind CSS
- **状态管理**: Pinia
- **可视化**: Chart.js + D3.js

### 后端技术栈
- **API框架**: FastAPI + Pydantic
- **数据库**: PostgreSQL + PostGIS + Redis
- **消息队列**: Celery + RabbitMQ
- **AI服务**: TensorFlow Serving + ONNX Runtime
- **存储**: MinIO (对象存储)

### 开发运维
- **容器化**: Docker + Docker Compose
- **编排**: Kubernetes (生产环境)
- **CI/CD**: GitHub Actions
- **监控**: Prometheus + Grafana

## 📅 开发计划

### 阶段一：项目评估与规划 (1周)
- [x] 项目初始化 (2026-04-14)
- [ ] 需求确认与竞品分析
- [ ] 技术评估与架构设计
- [ ] 详细项目计划制定

### 阶段二：架构设计与技术选型 (2周)
- [ ] 系统架构详细设计
- [ ] 数据库设计
- [ ] API接口设计
- [ ] 安全架构设计

### 阶段三：核心模块开发 (4周)
- [ ] 数据管理模块 (1.5周)
- [ ] 数据处理模块 (1.5周)
- [ ] 数据分析模块 (1周)
- [ ] AI搜索模块 (1周)
- [ ] 用户界面 (2周)

### 阶段四：集成测试与部署 (2周)
- [ ] 单元测试与集成测试
- [ ] 性能测试与优化
- [ ] 用户验收测试
- [ ] 生产环境部署

## 🔧 开发环境配置

### 硬件要求
- **CPU**: 4+核心 (推荐8+核心)
- **内存**: 8GB+ (推荐16GB+)
- **GPU**: 支持CUDA的NVIDIA显卡 (推荐RTX 3060+)
- **存储**: 50GB+ 可用空间

### 软件要求
- **操作系统**: Windows 10/11 + WSL2 或 Linux/macOS
- **Node.js**: v18+
- **Python**: 3.10+
- **Docker**: 24.0+
- **Git**: 2.30+

### 快速开始
```bash
# 克隆项目
git clone <repository-url>

# 前端开发
cd frontend
npm install
npm run dev

# 后端开发  
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py

# 每日进度报告 (自动)
# GitHub Actions每天21:00自动生成进度报告
# 查看报告: docs/daily-reports/ 目录
```

## 📄 文档索引

- [项目计划](/docs/PROJECT_PLAN.md) - 详细开发计划和时间表
- [需求规格](/docs/REQUIREMENTS.md) - 功能需求和非功能需求
- [架构设计](/docs/ARCHITECTURE.md) - 系统架构和技术选型
- [Cesium分析](/docs/CESIUM_VS_MAPBOX_ANALYSIS.md) - 地图引擎技术选型
- [GitHub配置](/docs/GITHUB_SETUP_GUIDE.md) - GitHub仓库和自动化配置
- [项目状态](/docs/PROJECT_STATUS.md) - 实时项目状态监控
- [每日报告](/docs/daily-reports/) - 每日进度报告存档
- [API文档](/docs/API.md) - 接口规范和示例
- [部署指南](/docs/DEPLOYMENT.md) - 环境部署和配置

## 🤝 贡献指南

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📞 联系我们

- **项目负责人**: 9号 (调度中心)
- **技术架构**: 推理专家
- **需求分析**: 文档专家
- **开发实现**: 开发专家
- **技术研究**: 信息专家

## 🔄 每日进度更新

本项目采用自动化进度跟踪系统：

### 自动更新机制
1. **每日21:00**: GitHub Actions自动生成进度报告
2. **报告内容**: 任务状态、代码变更、风险分析、下一步计划
3. **输出形式**: Markdown报告 + GitHub Issue + 项目状态总览
4. **透明协作**: 所有团队成员可实时查看项目进展

### 查看进度
- **实时状态**: [PROJECT_STATUS.md](/docs/PROJECT_STATUS.md)
- **历史报告**: [daily-reports/](/docs/daily-reports/)
- **GitHub Issues**: 每日自动创建审阅Issue
- **Actions日志**: GitHub Actions运行记录

## 📋 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

_最后更新: 2026-04-14 | 版本: v2.0.0-alpha_