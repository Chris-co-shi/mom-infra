# RocketMQ

本目录负责 RocketMQ NameServer、Broker、存储、监控和故障恢复配置。

## V1 目标

- 支撑 MOM 领域事件、Outbox/Inbox、PCS/WCS 命令与回执。
- 定义 NameServer、Broker、Topic、Consumer Group 和 ACL 的基础治理方式。
- 配置重试、死信、消息保留和存储容量。
- 接入日志、指标与 Trace。
- 验证重复投递、消费积压、Broker 中断和恢复。

## 架构边界

- 领域事件名称、Payload 和兼容策略归应用仓库所有。
- 本仓库负责 Broker 能力、资源、Topic 创建机制和运维治理。
- 应用必须按照至少一次投递设计幂等，不能假设消息绝不重复。
- RocketMQ 不可用时，Outbox 应保留待发布事实并支持恢复后补发。

## 进入部署前必须明确

- 精确版本及 Spring Boot 4 集成兼容性。
- NameServer 与 Broker 拓扑。
- PVC、磁盘容量和消息保留周期。
- ACL 与网络访问。
- 重试次数、死信处理和人工补偿入口。
- 升级、回滚、备份和恢复 Runbook。
