# 可观测性

目标数据流：

```text
应用与基础设施
→ OpenTelemetry Collector
→ Prometheus / Loki / Tempo
→ Grafana
```

## 目录职责

- `otel-collector/`：OTLP 接收、处理和转发。
- `prometheus/`：指标采集、存储和告警规则。
- `loki/`：结构化日志存储与查询。
- `tempo/`：Trace 存储与查询。
- `grafana/`：数据源、仪表盘和关联调查。

## 重点信号

- 集群和中间件健康。
- CPU、内存、存储和网络饱和度。
- 请求量、延迟和错误率。
- Redis 限流拒绝。
- RocketMQ 重试与积压。
- Outbox/Inbox 状态。
- Trace 缺口和 Collector 丢弃。
- 备份状态、恢复耗时和故障演练结果。

详细设计见：[可观测性基础设施](../docs/observability/可观测性基础设施.md)。
