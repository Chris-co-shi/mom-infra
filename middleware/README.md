# 中间件

本目录管理 PostgreSQL、Redis、Nacos、RocketMQ、Seata 等共享中间件的部署边界和运行配置。

## 每个组件必须具备

- 官方来源、许可证和精确版本。
- Helm Chart、Operator 或 Manifest 来源。
- 镜像 Tag 与 Digest。
- 拓扑和高可用目标。
- StorageClass、PVC 和容量基线。
- CPU、内存和临时存储基线。
- Readiness、Liveness 和业务健康验证。
- 备份、恢复、升级和回滚方式。
- 日志、指标和故障演练入口。

## 约束

- `prod-like` 禁止浮动镜像 Tag。
- 不在本目录定义业务表结构和领域消息 Payload。
- 有状态组件未完成恢复验证前，不标记为类生产可用。
- 组件版本以 [`config/component-versions.yaml`](../config/component-versions.yaml) 为权威来源。

当前实施顺序：PostgreSQL → Redis → Nacos → RocketMQ → Seata。
