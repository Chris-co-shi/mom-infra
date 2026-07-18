# Grafana

本目录保存 Grafana 数据源、Folder、Dashboard 和告警视图的可重复配置。

## V1 目标

- 自动配置 Prometheus、Loki 和 Tempo 数据源。
- 建立平台总览、中间件健康、限流、消息、链路追踪和恢复演练仪表盘。
- 支持日志与 Trace 双向跳转。
- 展示环境、服务、Namespace 和关键业务关联信息。

## 约束

- 重要 Dashboard 必须以 JSON、Provisioning 或代码方式进入 Git。
- 禁止仅在 UI 中手工维护而不导出回库。
- Dashboard 变量不得制造无界高基数查询。
- 数据源凭证通过 Secret 注入，不写入配置文件。
- 告警视图和阈值变化需要评审和回滚路径。

## 验收

- 全新环境可从 Git 自动恢复数据源与核心 Dashboard。
- 能从错误日志跳转到对应 Trace。
- 能查看 PostgreSQL、Redis、RocketMQ 和应用健康概览。
