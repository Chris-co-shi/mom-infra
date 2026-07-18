# ADR-004：OpenTelemetry 与 Grafana 可观测性栈

- 状态：Accepted
- 日期：2026-07-18
- 关联文档：[可观测性基础设施](../observability/可观测性基础设施.md)

## 1. 背景

MOM、PCS、WCS 和 Integration Hub 同时包含 HTTP、Feign、RocketMQ、任务和设备命令链路，需要统一观测技术调用和长业务流程。

## 2. 候选方案

### 方案 A：仅依赖应用日志

优点：部署简单。

缺点：无法稳定关联跨服务、消息和设备链路。

### 方案 B：多套独立 APM/日志产品

优点：各产品能力丰富。

缺点：部署复杂、数据割裂、学习和资源成本较高。

### 方案 C：OpenTelemetry + Prometheus + Loki + Tempo + Grafana

优点：开放标准、指标日志追踪可统一调查，与 Spring/Micrometer 体系匹配。

缺点：需要自行配置采集、存储、关联和容量治理。

## 3. 决策

采用方案 C：

- OpenTelemetry Collector 作为遥测入口。
- Prometheus 存储指标。
- Loki 存储日志。
- Tempo 存储 Trace。
- Grafana 作为统一调查入口。

## 4. 关键边界

- `trace_id` 仅表示技术调用链。
- 长业务流程使用 `correlation_id`、`workflow_id`、`event_id`、`command_id` 等关联。
- 高基数字段不作为 Prometheus Label。
- 观测后端故障不得阻塞核心业务。

## 5. 后果

正向：

- HTTP、消息、任务和设备命令可统一调查。
- 技术故障可以与业务流程关联。
- 项目具备完整的面试展示和故障演练能力。

负向：

- 需要额外存储容量和保留策略。
- 采样、高基数和日志量必须治理。

## 6. 验证

- Grafana 可查询指标、日志和 Trace。
- 日志与 Trace 双向关联。
- 至少一条 RocketMQ 异步链路可追踪。
- Collector 故障不影响核心业务，并有恢复 Runbook。
