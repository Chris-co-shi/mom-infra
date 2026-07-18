# Prometheus

本目录负责指标采集、Recording Rule、告警规则、保留周期、存储和高基数治理。

## V1 目标

- 采集 Kubernetes、PostgreSQL、Redis、Nacos、RocketMQ、Seata 和应用指标。
- 统一环境、服务、Namespace 和实例标签。
- 建立请求量、延迟、错误率、资源饱和度和中间件健康告警。
- 采集 Gateway 限流、消息积压、Outbox/Inbox 和备份状态指标。
- 为 Grafana 提供统一指标数据源。

## 标签原则

适合 Label：

- `service`
- `environment`
- `namespace`
- `route_id`
- `result`

不适合 Label：

- `trace_id`
- 用户 ID
- 工单号
- 批次号
- 事件 ID

## 进入部署前必须明确

- 抓取目标和 ServiceMonitor/静态配置方式。
- 存储容量和保留周期。
- Recording Rule 与告警阈值。
- 高基数保护。
- Prometheus 自身健康和磁盘压力告警。

## 验收

- Grafana 可查询集群、中间件和应用指标。
- 告警能覆盖 Pod 异常、资源饱和、消息积压和遥测丢失。
- 指标标签基数处于可控范围。
