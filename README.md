# TradingAgents 中文增强版

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-v1.1.0-green.svg)](./VERSION)
[![Documentation](https://img.shields.io/badge/docs-中文文档-green.svg)](./docs/)
[![Original](https://img.shields.io/badge/基于-TauricResearch/TradingAgents-orange.svg)](https://github.com/TauricResearch/TradingAgents)

---


## 🗺️ Development Roadmap

The platform will be delivered incrementally. Each phase should produce a runnable vertical slice before the next major capability is added.

### Phase 1 — TradingAgents Production-Ready

- [ ] Run the TradingAgents workflow end-to-end
- [ ] Expose a stable Analysis API
- [ ] Finalize and version `AnalysisSignal v1`
- [ ] Persist analysis jobs/results across restarts
- [ ] Add health checks, metrics and failure visibility
- [ ] Deploy TradingAgents to a reachable environment
- [ ] Validate signal freshness through `dataTimestamp` and `validUntil`
- [ ] Ensure TradingAgents remains decision support only and never submits broker/exchange orders

**Exit criterion:** an external consumer can reliably request/query analysis and consume a versioned AnalysisSignal.

### Phase 2 — TradeMonitor + TradingAgents

- [ ] Connect TradeMonitor to TradingAgents through explicit API/events
- [ ] Build an independent TradeMonitor read model
- [ ] Show analysis jobs and signal history
- [ ] Show analysis latency and failures
- [ ] Show model/version information
- [ ] Add LLM token/cost monitoring where available
- [ ] Add initial alerting
- [ ] Verify TradeMonitor failure does not affect TradingAgents

**Exit criterion:** TradeMonitor provides an operational view of AI analysis without reading TradingAgents storage directly.

### Phase 3 — StockTrader + Alpaca Paper Trading

- [ ] Consume `AnalysisSignal v1`
- [ ] Implement Strategy → `TradeIntent`
- [ ] Implement deterministic pre-trade Risk checks
- [ ] Implement the Order Management state machine
- [ ] Implement Portfolio/position state
- [ ] Implement `ExecutionGateway` and Alpaca Paper Trading adapter
- [ ] Execute BUY/SELL flows in the Alpaca test environment
- [ ] Handle partial fills, rejects and cancellations
- [ ] Implement idempotency and duplicate-signal protection
- [ ] Implement timeout/unknown-order-state recovery
- [ ] Implement Alpaca reconciliation
- [ ] Publish versioned stock trading events
- [ ] Validate stateless multi-instance behavior and horizontal scaling

**Exit criterion:** a valid TradingAgents signal can pass Strategy → Risk → OMS → Alpaca and update the owned portfolio safely.

### Phase 3.1 — TradeMonitor Stock Dashboard

- [ ] Consume StockTrader order/execution/position/risk events
- [ ] Add stock order lifecycle view
- [ ] Add executions/fills view
- [ ] Add positions and PnL
- [ ] Add exposure and risk-rejection view
- [ ] Add Alpaca connectivity status
- [ ] Add StockTrader ↔ Alpaca reconciliation status
- [ ] Add business alerts

**Exit criterion:** stock trading can be monitored end-to-end without TradeMonitor accessing the StockTrader database.

### Phase 4 — CrypTrader + Binance

- [ ] Consume `AnalysisSignal v1`
- [ ] Implement Crypto Strategy → Risk → OMS → Portfolio flow
- [ ] Implement Binance market-data adapter
- [ ] Implement Binance execution adapter
- [ ] Support 24/7 market operation
- [ ] Handle WebSocket reconnect/resubscribe
- [ ] Handle sequence/order-book consistency where required
- [ ] Handle symbol precision, lot size and tick size
- [ ] Handle Binance rate limits and exchange errors
- [ ] Implement idempotency and safe retries
- [ ] Implement Binance reconciliation
- [ ] Publish versioned crypto trading events
- [ ] Validate stateless multi-instance behavior and horizontal scaling

**Exit criterion:** CrypTrader can safely execute and reconcile automated trades in the selected Binance test environment.

### Phase 4.1 — TradeMonitor Crypto Dashboard

- [ ] Consume CrypTrader order/execution/position/risk events
- [ ] Add crypto order lifecycle view
- [ ] Add executions/fills view
- [ ] Add balances, positions and PnL
- [ ] Add exposure and risk-rejection view
- [ ] Add Binance/WebSocket connectivity status
- [ ] Add CrypTrader ↔ Binance reconciliation status
- [ ] Add crypto-specific business alerts

**Exit criterion:** crypto trading can be monitored end-to-end from the shared TradeMonitor platform.

### Phase 5 — Architecture Hardening

- [ ] Run multiple StockTrader instances
- [ ] Run multiple CrypTrader instances
- [ ] Run multiple TradeMonitor instances
- [ ] Verify no duplicate trades under concurrent processing
- [ ] Verify safe concurrent portfolio/order updates
- [ ] Test Kafka/event replay and duplicate delivery
- [ ] Test database/process restart recovery
- [ ] Test Alpaca timeout/failure scenarios
- [ ] Test Binance disconnect/recovery scenarios
- [ ] Add/complete OpenTelemetry tracing
- [ ] Add Prometheus metrics and Grafana dashboards
- [ ] Measure p95/p99 analysis and order-processing latency
- [ ] Monitor Kafka lag and database connection pools
- [ ] Review authentication, authorization and secret management
- [ ] Run resilience/failure tests and document results

**Exit criterion:** the platform demonstrates horizontal scalability, failure isolation, recovery, observability and operational readiness.

### Roadmap overview

```text
Phase 1   TradingAgents Production-Ready
                    ↓
Phase 2   TradeMonitor + AI Monitoring
                    ↓
Phase 3   StockTrader + Alpaca Paper Trading
                    ↓
Phase 3.1 TradeMonitor Stock Dashboard
                    ↓
Phase 4   CrypTrader + Binance
                    ↓
Phase 4.1 TradeMonitor Crypto Dashboard
                    ↓
Phase 5   Scalability / Resilience / Observability Hardening
```


## 🧩 在总体交易平台中的定位

> 本仓库基于现有 TradingAgents-CN / 上游开源能力进行学习、架构研究和扩展。原项目的版权、许可证、专有目录和商业授权要求以本 README 下方及仓库 LICENSE/COPYRIGHT 文件中的原始说明为准。

在总体架构中，TradingAgents-CN 被定位为 **AI Market Intelligence / Decision Support SCS**，负责市场研究和结构化分析，不负责最终交易决策、风险审批或订单执行。

### 主要职责

- 汇集市场数据、新闻、基本面等研究输入
- 使用多智能体/LLM 生成市场分析
- 对外提供版本化的 Analysis API / AnalysisSignal
- 输出方向、置信信息、风险因素、数据时间和有效期等决策支持信息
- 管理 LLM Provider、模型路由、超时、重试和后续成本/Token 可观测能力
- 保持 AI 分析与确定性的交易执行边界

### 总体平台架构

```text
Market Data / News / Fundamentals
              │
              ▼
       TradingAgents-CN
    AI Market Intelligence
              │
       AnalysisSignal / API
        ┌─────┴─────┐
        ▼           ▼
   StockTrader   CrypTrader
      │              │
    Alpaca          Binance
      │              │
      └── trading ───┘
          events
            │
            ▼
       TradeMonitor
```

核心原则：

```text
AI Analysis / Signal != Trading Decision
```

TradingAgents-CN 不直接向 Alpaca/Binance 下单。下游 Trader SCS 必须结合实时市场状态、Strategy、Portfolio 和确定性的 Risk Rules 后才能形成订单。

### 下游契约方向

计划向下游提供类似以下的版本化结构化结果：

```text
AnalysisSignal
├── analysisId
├── instrument
├── direction / market view
├── confidence / score
├── risk factors
├── dataTimestamp
├── validUntil
└── modelVersion
```

下游系统必须自行处理 freshness、版本、重复消息和过期分析。

### 与其他 SCS 的边界

| SCS | 职责 |
|---|---|
| TradingAgents-CN | AI 市场研究、分析与 Decision Support |
| StockTrader | 股票 Strategy、Risk、OMS、Portfolio 与 Alpaca 执行 |
| CrypTrader | Crypto Strategy、Risk、OMS、Portfolio 与 Binance 执行 |
| TradeMonitor | 交易业务监控、告警、PnL/Exposure 视图与 Reconciliation |

SCS 之间不共享数据库，通过显式 API 或版本化事件契约集成。

---

## ⚠️ 重要版权声明与授权说明

### 🚨 版权侵权警告

**我们注意到 `tradingagents-ai.com` 网站未经授权使用了我们的专有代码，并声称是他们公司的产品。**

**⚠️ 重要提醒**：
- ❌ **我们项目组目前没有给任何组织或个人进行过商业授权**
- ❌ **该网站未经授权使用我们的代码，属于侵权行为**
- ⚠️ **请大家注意识别，避免上当受骗**

**✅ 官方唯一渠道**：
- 📦 GitHub 仓库：https://github.com/hsliuping/TradingAgents-CN
- 📧 官方邮箱：hsliup@163.com
- 📱 微信公众号：TradingAgents-CN

如发现任何未经授权的商业使用，请通过上述渠道联系我们。

### 📋 版本授权说明

#### v1.1.0（已开源）
- ✅ **个人使用**：完全开源，可自由使用
- ❌ **商业使用**：**必须获得商业授权**，未经授权禁止商业使用
- 📧 **授权联系**：[hsliup@163.com](mailto:hsliup@163.com)

#### v2.0（即将开源）
- 🔄 **开发状态**：已开发完成，稳定运行中
- 🔓 **开源计划**：**v2.0 将完整开源**（Apache 2.0 + 商业使用限制条款）
- 📢 **开源时间**：v3.0 正式发布后，v2.0 开源
- ⚠️ **商业使用**：开源后商业使用仍需获得授权

#### v3.0（即将发布）
- 🎉 **开发状态**：开发完成，内测启动中
- ✨ **新功能**：AI 工作流设计器、复盘研究、持仓研究、Skill 系统、智能助手等
- 🚀 **版本定位**：最新版本，包含全部专业功能
- 📧 **内测申请**：[hsliup@163.com](mailto:hsliup@163.com)

### 📄 许可证详情

本项目采用**混合许可证**模式：
- 🔓 **开源部分**（Apache 2.0）：除 `app/` 和 `frontend/` 外的所有文件
- 🔒 **专有部分**（需商业授权）：`app/`（FastAPI后端）和 `frontend/`（Vue前端）目录

详细说明请查看：[版权声明](./COPYRIGHT.md) | [许可证文件](./LICENSE)

### 🤝 贡献者招募

我们正在寻找核心贡献者！贡献代码可获得 Pro 版授权和收入分成：
- 合并 1 个 PR → Pro 版 3 个月授权
- 合并 3 个 PR → Pro 版 1 年授权
- 核心贡献者 → 永久授权 + 收入分成

详见：[贡献指南](./docs/development/CONTRIBUTING.md)

### ⚖️ 免责声明

> **本工具仅提供数据分析，不构成任何投资建议。**
> 投资有风险，决策需谨慎。分析结果由 AI 生成，仅供参考，用户需自行判断并承担投资风险。
> 本平台不提供实盘交易指令，定位为学习与研究用途。

### 🗺️ 项目路线图

我们坚持**逐步开源**策略，旧版本会在新版本稳定后逐步开源：

| 版本 | 状态 | 说明 |
|------|------|------|
| v1.0 | ✅ 已开源 | 基础功能，吸引社区参与 |
| v2.0 | 🔓 即将开源 | 完整功能，建立用户习惯 |
| v3.0 | 🚀 即将发布 | 最新版本，专业功能 |

**开源承诺**：旧版本会逐步免费开源，使用最新版本的用户始终能获得最新的功能和优先支持。

**长期方向**：
- 持续完善 AI 多智能体分析能力
- 探索策略回测、知识图谱等专业方向
- 建设开源社区，欢迎贡献者参与

---

>
> 🎓 **学习中心**: AI基础 | 提示词工程 | 模型选择 | 多智能体分析原理 | 风险与局限 | 源项目与论文 | 实战教程（部分为外链） | 常见问题
> 🎯 **核心功能**: 原生OpenAI支持 | Google AI全面集成 | 自定义端点配置 | 智能模型选择 | 多LLM提供商支持 | 模型选择持久化 | Docker容器化部署 | 专业报告导出 | 完整A股支持 | 中文本地化

面向中文用户的**多智能体与大模型股票分析学习平台**。帮助你系统化学习如何使用多智能体交易框架与 AI 大模型进行合规的股票研究与策略实验，不提供实盘交易指令，平台定位为学习与研究用途。

## 🙏 致敬源项目

感谢 [Tauric Research](https://github.com/TauricResearch) 团队创造的革命性多智能体交易框架 [TradingAgents](https://github.com/TauricResearch/TradingAgents)！

**🎯 我们的定位与使命**: 专注学习与研究，提供中文化学习中心与工具，合规友好，支持 A股/港股/美股 的分析与教学，推动 AI 金融技术在中文社区的普及与正确使用。

## 🎉 v1.1.0 版本说明 - 火山方舟集成与开发体验增强

> 🚀 **当前推荐版本**: `v1.1.0` 已正式可用，在 v1.0.1 基础上，重点集成火山方舟模型服务、增强推理模型支持、统一开发启动脚本，并完善项目文档体系。

### ✨ 核心特性

#### 🏗️ **全新技术架构**
- **后端升级**: 从 Streamlit 迁移到 FastAPI，提供更强大的 RESTful API
- **前端重构**: 采用 Vue 3 + Element Plus，打造现代化的单页应用
- **数据库优化**: MongoDB + Redis 双数据库架构，性能提升 10 倍
- **容器化部署**: 完整的 Docker 多架构支持（amd64 + arm64）

#### 🚀 **v1.1.0 重点增强**
- **火山方舟集成**: 新增火山方舟（VolcEngine Ark）Provider，支持编程版模型硬编码配置与密码兼容
- **推理模型优化**: `reasoning_effort` 全链路传递，推理模型超时保护优化
- **数据模型扩展**: 添加 `reasoning_effort` / `test_model` 字段，支持火山方舟模型过滤
- **统一启动脚本**: 新增 `start_dev.ps1`，支持 v1.0/v2.0/v2.1/v3.0 多版本开发环境一键启动
- **连接修复**: MongoDB 连接字符串自动构建，Tushare 写 tk.csv 权限错误修复
- **文档体系完善**: 更新版权声明与授权说明、贡献者指南（贡献换授权机制）、项目发展战略规划

#### 🎯 **企业级功能**
- **用户权限管理**: 完整的用户认证、角色管理、操作日志系统
- **配置管理中心**: 可视化的大模型配置、数据源管理、系统设置
- **缓存管理系统**: 智能缓存策略，支持 MongoDB/Redis/文件多级缓存
- **实时通知系统**: SSE+WebSocket 双通道推送，实时跟踪分析进度和系统状态
- **批量分析功能**: 支持多只股票同时分析，提升工作效率
- **智能股票筛选**: 基于多维度指标的股票筛选和排序系统
- **自选股管理**: 个人自选股收藏、分组管理和跟踪功能
- **个股详情页**: 完整的个股信息展示和历史分析记录
- **模拟交易系统**: 虚拟交易环境，验证投资策略效果

#### 🤖 **智能分析增强**
- **动态供应商管理**: 支持动态添加和配置 LLM 供应商
- **模型能力管理**: 智能模型选择，根据任务自动匹配最佳模型
- **多数据源同步**: 统一的数据源管理，支持 Tushare、AkShare、BaoStock
- **报告导出功能**: 支持 Markdown/Word/PDF 多格式专业报告导出

#### 🔧 **重大Bug修复**
- **技术指标计算修复**: 彻底解决市场分析师技术指标计算不准确问题
- **基本面数据修复**: 修复基本面分析师PE、PB等关键财务数据计算错误
- **死循环问题修复**: 解决部分用户在分析过程中触发的无限循环问题
- **数据一致性优化**: 确保所有分析师使用统一、准确的数据源

#### 🐳 **Docker 多架构支持**
- **跨平台部署**: 支持 x86_64 和 ARM64 架构（Apple Silicon、树莓派、AWS Graviton）
- **GitHub Actions**: 自动化构建和发布 Docker 镜像
- **一键部署**: 完整的 Docker Compose 配置，5 分钟快速启动

### 📊 技术栈升级

| 组件 | v0.1.x | v1.1.0 |
|------|--------|----------------|
| **后端框架** | Streamlit | FastAPI + Uvicorn |
| **前端框架** | Streamlit | Vue 3 + Vite + Element Plus |
| **数据库** | 可选 MongoDB | MongoDB + Redis |
| **API 架构** | 单体应用 | RESTful API + WebSocket |
| **部署方式** | 本地/Docker | Docker 多架构 + GitHub Actions |



#### 📥 安装部署

**两种部署方式，任选其一**：

| 部署方式 | 适用场景 | 难度 | 文档链接 |
|---------|---------|------|---------|
| 🐳 **Docker版** | 生产环境、跨平台 | ⭐⭐ 中等 | [Docker 部署指南](https://mp.weixin.qq.com/s/JkA0cOu8xJnoY_3LC5oXNw) |
| 💻 **本地代码版** | 开发者、定制需求 | ⭐⭐⭐ 较难 | [本地安装指南](https://mp.weixin.qq.com/s/cqUGf-sAzcBV19gdI4sYfA) |

⚠️ **重要提醒**：在分析股票之前，请按相关文档要求，将股票数据同步完成，否则分析结果将会出现数据错误。



#### 📚 使用指南

在使用前，建议先阅读详细的使用指南：
- **[v1.1.0 发布说明](./docs/releases/v1.1.0-release-notes.md)**
- **[v1.1.0 使用手册](./docs/guides/v1.1.0-user-manual.md)**
- **[v1.1.0 升级指南](./docs/releases/upgrade-guide.md)**
- **[完整更新日志](./docs/releases/CHANGELOG.md)**
- **[0、📘 TradingAgents-CN v1.0.0-preview 快速入门视频](https://www.bilibili.com/video/BV1i2CeBwEP7/?vd_source=5d790a5b8d2f46d2c10fd4e770be1594)**

- **[1、📘 TradingAgents-CN v1.0.0-preview 使用指南](https://mp.weixin.qq.com/s/ppsYiBncynxlsfKFG8uEbw)**
- **[2、📘 使用 Docker Compose 部署TradingAgents-CN v1.0.0-preview（完全版）](https://mp.weixin.qq.com/s/JkA0cOu8xJnoY_3LC5oXNw)**
- **[3、📘 从 Docker Hub 更新 TradingAgents‑CN 镜像](https://mp.weixin.qq.com/s/WKYhW8J80Watpg8K6E_dSQ)**
- **[4、📘 TradingAgents-CN v1.0.0-preview绿色版安装和升级指南](https://mp.weixin.qq.com/s/eoo_HeIGxaQZVT76LBbRJQ)**
- **[5、📘 TradingAgents-CN v1.0.0-preview绿色版端口配置说明](https://mp.weixin.qq.com/s/o5QdNuh2-iKkIHzJXCj7vQ)**
- **[6、📘 TradingAgents v1.0.0-preview 源码版安装手册（修订版）](https://mp.weixin.qq.com/s/cqUGf-sAzcBV19gdI4sYfA)**
- **[7、📘 TradingAgents v1.0.0-preview 源码安装视频教程](https://www.bilibili.com/video/BV1FxCtBHEte/?vd_source=5d790a5b8d2f46d2c10fd4e770be1594)**


使用指南包含：
- ✅ 完整的功能介绍和操作演示
- ✅ 详细的配置说明和最佳实践
- ✅ 常见问题解答和故障排除
- ✅ 实际使用案例和效果展示

### 数据库运维补充

- 数据库版本隔离、共享库保护、迁移脚本与 provider 规范化说明：
  - [数据库版本隔离与 Provider 规范化](./docs/deployment/database/DB_VERSION_ISOLATION_AND_PROVIDER_NORMALIZATION.md)

### 上游吸收补充

- 当前项目采用人工选择性吸收上游更新：
  - [上游同步策略](./docs/maintenance/upstream-sync.md)
  - [人工上游吸收清单](./docs/maintenance/manual-upstream-absorption-checklist.md)

- `v1.1.0` 已明确同步到当前版本的上游能力包括：
  - `llm_clients` 抽象层主链路
  - 共享模型目录与轻量校验
  - provider canonical key 规范化
  - `trading_graph.py` 主要 provider 初始化路径收口
  - `fundamentals_analyst.py` 中 qwen fresh llm 重建逻辑
  - 图层参数透传、工厂别名兼容、风控引用修复
  - provider 默认 URL / 环境变量映射统一
  - MongoDB 默认库名、版本隔离命名与迁移脚本增强

#### 关注公众号

1. **关注公众号**: 微信搜索 **"TradingAgents-CN"** 并关注
2. 公众号每天推送项目最新进展和使用教程


- **微信公众号**: TradingAgents-CN（推荐）

  <img src="assets/wexin.png" alt="微信公众号" width="200"/>


## 🆚 中文增强特色

**相比原版新增**: 智能新闻分析 | 多层次新闻过滤 | 新闻质量评估 | 统一新闻工具 | 多LLM提供商集成 | 模型选择持久化 | 快速切换按钮 | | 实时进度显示 | 智能会话管理 | 中文界面 | A股数据 | 国产LLM | Docker部署 | 专业报告导出 | 统一日志管理 | Web配置界面 | 成本优化



## 🤝 贡献指南

我们欢迎各种形式的贡献：

### 贡献类型

- 🐛 **Bug修复** - 发现并修复问题
- ✨ **新功能** - 添加新的功能特性
- 📚 **文档改进** - 完善文档和教程
- 🌐 **本地化** - 翻译和本地化工作
- 🎨 **代码优化** - 性能优化和代码重构

### 贡献流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📋 查看贡献者

查看所有贡献者和详细贡献内容：**[🤝 贡献者名单](CONTRIBUTORS.md)**

## 📄 许可证详情

本项目采用**混合许可证**模式，详见 [LICENSE](LICENSE) 文件：

### 🔓 开源部分（Apache 2.0）
- **适用范围**：除 `app/` 和 `frontend/` 外的所有文件
- **权限**：商业使用 ✅ | 修改分发 ✅ | 私人使用 ✅ | 专利使用 ✅
- **条件**：保留版权声明 ❗ | 包含许可证副本 ❗

### 🔒 专有部分（需商业授权）
- **适用范围**：`app/`（FastAPI后端）和 `frontend/`（Vue前端）目录
- **商业使用**：需要单独许可协议
- **联系授权**：[hsliup@163.com](mailto:hsliup@163.com)

### 📋 许可证选择建议
- **个人学习/研究**：可自由使用全部功能
- **商业应用**：请联系获取专有组件授权
- **定制开发**：欢迎咨询商业合作方案

### 📚 相关文档

- [版权声明](./COPYRIGHT.md) - 详细的版权信息和使用条款
- [主许可证](./LICENSE) - Apache 2.0 许可证
- [后端专有许可证](./app/LICENSE) - 后端专有组件许可证
- [前端专有许可证](./frontend/LICENSE) - 前端专有组件许可证

## 🙏 致谢与感恩

### 🌟 向源项目开发者致敬

我们向 [Tauric Research](https://github.com/TauricResearch) 团队表达最深的敬意和感谢：

- **🎯 愿景领导者**: 感谢您们在AI金融领域的前瞻性思考和创新实践
- **💎 珍贵源码**: 感谢您们开源的每一行代码，它们凝聚着无数的智慧和心血
- **🏗️ 架构大师**: 感谢您们设计了如此优雅、可扩展的多智能体框架
- **💡 技术先驱**: 感谢您们将前沿AI技术与金融实务完美结合
- **🔄 持续贡献**: 感谢您们持续的维护、更新和改进工作

### 🤝 社区贡献者致谢

感谢所有为TradingAgents-CN项目做出贡献的开发者和用户！

详细的贡献者名单和贡献内容请查看：**[📋 贡献者名单](CONTRIBUTORS.md)**

包括但不限于：

- 🐳 **Docker容器化** - 部署方案优化
- 📄 **报告导出功能** - 多格式输出支持
- 🐛 **Bug修复** - 系统稳定性提升
- 🔧 **代码优化** - 用户体验改进
- 📝 **文档完善** - 使用指南和教程
- 🌍 **社区建设** - 问题反馈和推广
- **🌍 开源贡献**: 感谢您们选择Apache 2.0协议，给予开发者最大的自由
- **📚 知识分享**: 感谢您们提供的详细文档和最佳实践指导

**特别感谢**：[TradingAgents](https://github.com/TauricResearch/TradingAgents) 项目为我们提供了坚实的技术基础。虽然Apache 2.0协议赋予了我们使用源码的权利，但我们深知每一行代码的珍贵价值，将永远铭记并感谢您们的无私贡献。

### 🇨🇳 推广使命的初心

创建这个中文增强版本，我们怀着以下初心：

- **🌉 技术传播**: 让优秀的TradingAgents技术在中国得到更广泛的应用
- **🎓 教育普及**: 为中国的AI金融教育提供更好的工具和资源
- **🤝 文化桥梁**: 在中西方技术社区之间搭建交流合作的桥梁
- **🚀 创新推动**: 推动中国金融科技领域的AI技术创新和应用

### 🌍 开源社区

感谢所有为本项目贡献代码、文档、建议和反馈的开发者和用户。正是因为有了大家的支持，我们才能更好地服务中文用户社区。

### 🤝 合作共赢

我们承诺：

- **尊重原创**: 始终尊重源项目的知识产权和开源协议
- **反馈贡献**: 将有价值的改进和创新反馈给源项目和开源社区
- **持续改进**: 不断完善中文增强版本，提供更好的用户体验
- **开放合作**: 欢迎与源项目团队和全球开发者进行技术交流与合作

## 🙏 感谢赞助

<table>
    <tr>
        <td width="180"><a href="https://www.volcengine.com/activity/ai618?utm_campaign=hw&utm_content=hw&utm_medium=devrel_tool_web&utm_source=OWO&utm_term=TradingAgents-CN"><img src="assets/huoshan.png" alt="火山引擎" width="150"></a></td>
        <td>感谢<a href="https://www.volcengine.com/activity/ai618?utm_campaign=hw&utm_content=hw&utm_medium=devrel_tool_web&utm_source=OWO&utm_term=TradingAgents-CN">字节火山引擎</a>赞助本项目！<br>
【专属活动优惠】19元Tokens包！享字节自研豆包模型+满血版开源 SOTA模型，覆盖文本、VLM、图像生成，全模态一站配齐：Seed-2.1、Seedream-5.0、GLM-5.2、DeepSeek、Qwen等。不止编程、更能解决 Agent 复杂长程任务 → 注册即领2500万Tokens，立即前往<br>
👉 <a href="https://www.volcengine.com/activity/ai618?utm_campaign=hw&utm_content=hw&utm_medium=devrel_tool_web&utm_source=OWO&utm_term=TradingAgents-CN">点击链接抢购</a></td>
    </tr>
</table>

## 📈 版本历史

- **v1.1.0** (2026-07-24): 🚀 火山方舟集成、reasoning_effort 推理优化、统一启动脚本、文档体系完善 ✨ **当前版本**
- **v1.0.1** (2026-04-14): 🔧 配置管理优化、AiHubMix 聚合厂家、单股同步增强与上游能力吸收
- **v1.0.0-preview** (2025-10-10): 🏗️ FastAPI + Vue 3 新架构预览版
- **v0.1.13** (2025-08-02): 🤖 原生OpenAI支持与Google AI生态系统全面集成
- **v0.1.12** (2025-07-29): 🧠 智能新闻分析模块与项目结构优化
- **v0.1.11** (2025-07-27): 🤖 多LLM提供商集成与模型选择持久化
- **v0.1.10** (2025-07-18): 🚀 Web界面实时进度显示与智能会话管理
- **v0.1.9** (2025-07-16): 🎯 CLI用户体验重大优化与统一日志管理
- **v0.1.8** (2025-07-15): 🎨 Web界面全面优化与用户体验提升
- **v0.1.7** (2025-07-13): 🐳 容器化部署与专业报告导出
- **v0.1.6** (2025-07-11): 🔧 阿里百炼修复与数据源升级
- **v0.1.5** (2025-07-08): 📊 添加Deepseek模型支持
- **v0.1.4** (2025-07-05): 🏗️ 架构优化与配置管理重构
- **v0.1.3** (2025-06-28): 🇨🇳 A股市场完整支持
- **v0.1.2** (2025-06-15): 🌐 Web界面和配置管理
- **v0.1.1** (2025-06-01): 🧠 国产LLM集成

📋 **详细更新日志**: [CHANGELOG.md](./docs/releases/CHANGELOG.md)

## 📞 联系方式

- **GitHub Issues**: [提交问题和建议](https://github.com/hsliuping/TradingAgents-CN/issues)
- **邮箱**: hsliup@163.com
- 项目ＱＱ群：1091917201
- 项目微信公众号：TradingAgents-CN

  <img src="assets/wexin.png" alt="微信公众号" width="200"/>

- **原项目**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- **文档**: [完整文档目录](docs/)

## ⚠️ 风险提示

**重要声明**: 本框架仅用于研究和教育目的，不构成投资建议。

- 📊 交易表现可能因多种因素而异
- 🤖 AI模型的预测存在不确定性
- 💰 投资有风险，决策需谨慎
- 👨‍💼 建议咨询专业财务顾问

---

<div align="center">

**🌟 如果这个项目对您有帮助，请给我们一个 Star！**

[⭐ Star this repo](https://github.com/hsliuping/TradingAgents-CN) | [🍴 Fork this repo](https://github.com/hsliuping/TradingAgents-CN/fork) | [📖 Read the docs](./docs/)

</div>


---

## 🏗️ 架构现代化 Case Study（个人学习与系统设计实践）

> 本部分用于记录在现有开源项目基础上的架构分析、工程化改造与系统设计实践。项目中的原始开源代码、版权与许可证边界以仓库现有说明为准；后续新增内容会明确区分“上游开源能力”与“个人新增的架构设计/实现”。

### 🎯 目标

本项目不仅用于功能开发，也作为一个完整的 **Software / Solution Architecture Case Study**。重点不是简单增加功能，而是围绕真实业务场景训练和展示以下能力：

- 理解和评估已有复杂系统
- 从业务目标与 NFR（非功能性需求）出发设计方案
- 对技术方案做 Trade-off 分析，而不是只做技术堆叠
- 处理并发、数据一致性、失败恢复、可观测性和成本问题
- 通过 ADR（Architecture Decision Record）记录关键架构决策
- 用可运行实现、测试和指标验证架构判断

### 🧭 计划中的架构演进

#### 1. 重新梳理系统边界

当前核心链路可概括为：

```text
Vue Frontend
    ↓
FastAPI Backend
    ↓
Agent Orchestration
    ↓
LLM Providers / Market Data Providers
    ↓
MongoDB / Redis
```

后续会进一步明确 Domain Boundary，并评估哪些能力应保持在模块化单体中、哪些适合独立服务：

```text
API / Backend
    ├── Analysis Orchestrator
    ├── Market Data Service
    ├── Portfolio / Watchlist
    ├── LLM Gateway
    ├── Report Service
    └── Notification Service
```

重点问题：

- 为什么拆分？
- 是否真的需要 Microservices？
- 服务边界如何定义？
- 谁拥有数据？
- 如何避免分布式系统复杂度超过收益？

#### 2. 引入 Event-Driven Analysis Pipeline

针对耗时较长的 AI 分析任务，计划对比同步请求与异步事件驱动模式。

目标架构：

```text
POST /analysis
      ↓
Create Analysis Job
      ↓
Kafka: analysis.requested
      ↓
Worker / Agent Orchestrator
      ↓
Kafka: analysis.completed
      ↓
MongoDB
      ↓
SSE / WebSocket
      ↓
Frontend
```

重点验证：

- Partitioning 与 Ordering
- Consumer Group 与水平扩展
- At-least-once 与 Duplicate
- Idempotent Consumer
- Retry / Backoff / DLT
- Backpressure
- Replay / Recovery
- Schema Evolution

#### 3. Redis：从“使用缓存”到“设计缓存”

计划将 Redis 用于并验证不同架构场景：

- Market Data Cache
- LLM Response Cache
- Analysis Result Cache
- Rate Limiting
- Distributed Lock

重点研究：

```text
TTL
Cache Invalidation
Cache Stampede
Cache Penetration
Stale Data
Distributed Lock Expiration
Lock Ownership
Fencing Token
```

尤其会设计失败场景，例如：

```text
Instance A obtains lock
→ processing takes 10s
→ lock TTL expires after 5s
→ Instance B obtains the lock
→ both instances can now modify the same resource
```

并讨论什么时候 Redis Lock 足够、什么时候需要更严格的协调机制。

#### 4. LLM Gateway / AI Platform Layer

计划把 LLM 调用从具体 Agent 中进一步抽象：

```text
Agents
   ↓
LLM Gateway
   ├── Model Routing
   ├── Timeout
   ├── Retry
   ├── Rate Limiting
   ├── Token Accounting
   ├── Fallback
   ├── Tracing
   └── Cost Monitoring
```

目标是系统化回答：

- 如何控制 Token / Model Cost？
- Provider 故障时如何降级？
- 如何降低 Vendor Lock-in？
- 如何追踪单次分析的 LLM latency 与 token usage？
- 哪些任务需要高能力模型，哪些任务可路由到更便宜模型？
- 如何限制 Agent Tool 权限与 Side Effects？

#### 5. Observability & Production Engineering

计划建立完整可观测链路：

```text
analysisId / traceId
      ↓
API
      ↓
Kafka
      ↓
Agent
      ↓
LLM
      ↓
Market Data
      ↓
MongoDB / Redis
```

关注指标：

- API latency (p50 / p95 / p99)
- Analysis end-to-end latency
- LLM latency / error rate
- Token usage / estimated cost
- Cache hit ratio
- Kafka consumer lag
- Retry / DLT count
- MongoDB / Redis latency
- CPU / memory / error rate

候选技术：

- OpenTelemetry
- Prometheus
- Grafana
- Structured Logging

#### 6. Failure Model 与 Recovery

项目会主动设计和验证失败场景，而不是只验证 happy path：

- MongoDB 暂时不可用
- Redis cache miss / Redis outage
- Kafka consumer crash
- LLM Provider timeout
- Duplicate event
- Out-of-order event
- Worker restart
- Partial failure between persistence and message publishing

目标是明确：

```text
Timeout
Retry
Idempotency
Circuit Breaker
Outbox
Replay
Recovery
Fallback
Degraded Mode
```

### 📐 Architecture Documentation

计划逐步补充以下架构文档：

```text
docs/architecture/
├── 01-current-state.md
├── 02-target-architecture.md
├── 03-domain-boundaries.md
├── 04-data-flow.md
├── 05-failure-model.md
├── 06-scalability.md
├── 07-security.md
├── 08-observability.md
├── 09-capacity-estimation.md
└── adr/
    ├── ADR-001-kafka-for-analysis-jobs.md
    ├── ADR-002-mongodb-vs-postgresql.md
    ├── ADR-003-redis-cache-strategy.md
    ├── ADR-004-llm-gateway.md
    ├── ADR-005-sync-vs-async.md
    └── ADR-006-modular-monolith-vs-microservices.md
```

每个 ADR 将尽量保持统一结构：

```text
Context
→ Problem
→ Requirements
→ Options
→ Advantages / Disadvantages
→ Decision
→ Why
→ Consequences
→ When would we reconsider?
```

### 🔄 Architecture Evolution，而不是一次性“完美设计”

本 Case Study 会刻意记录系统从简单方案向更复杂方案演进的原因：

```text
V1  Synchronous Processing
    ↓
V2  Async / Kafka
    ↓
V3  Idempotency + Retry + DLT
    ↓
V4  Replay / Recovery
    ↓
V5  Observability + SLO
    ↓
V6  LLM Gateway + Cost / Provider Governance
```

每一步都要求能够回答：

1. 当前版本解决了什么问题？
2. 为什么需要下一步演进？
3. 替代方案是什么？
4. 新方案引入了什么复杂度？
5. 如何通过测试和指标证明它值得？

### ✅ 最终希望展示的能力

```text
1. Understand an existing complex system
2. Identify architectural weaknesses
3. Define functional and non-functional requirements
4. Evaluate alternatives and trade-offs
5. Make and document architecture decisions
6. Implement critical parts of the design
7. Test failure and recovery scenarios
8. Measure performance and operational behavior
9. Explain the architecture to technical and non-technical stakeholders
```

这个项目的目标不是证明“所有代码都是从零写的”，而是透明地展示：**如何基于一个真实且复杂的开源系统，完成架构评估、关键设计决策、工程化实现与生产级改进。**
