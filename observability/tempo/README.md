# Tempo

本目录负责分布式 Trace 的存储、保留、查询和与日志/指标的关联配置。

## V1 目标

- 接收 OpenTelemetry Collector 转发的 Trace。
- 覆盖 Gateway、Feign、RocketMQ、定时任务、Integration Hub、PCS/WCS 命令链路。
- 支持 Grafana 中从 Trace 跳转到 Loki 日志和 Prometheus 指标。
- 验证 Span Link 和业务关联标识查询。

## 设计原则

- `trace_id` 只表示技术调用链。
- 数小时或数天的业务流程通过 `correlation_id`、`workflow_id`、`event_id`、`command_id` 和 Span Link 关联多个 Trace。
- 明确采样率、存储容量和保留周期。
- 错误、高延迟和关键业务链路优先保留。
- Tempo 故障不得阻塞业务请求。

## 验收

- 能查询一条完整 HTTP 同步链路。
- 能查询一条 RocketMQ 异步链路。
- 错误 Trace 能关联对应日志。
- 重复消息场景能看到多次处理尝试。
- 存储压力和 Trace 丢弃有监控与告警。
