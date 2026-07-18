# PostgreSQL

本目录负责共享 PostgreSQL 集群的部署、存储、资源、备份和恢复配置。

## V1 目标

- 为 IAM、MDM、MES、WMS、QMS、Integration、Traceability 等服务提供独立 Schema。
- 验证连接池、连接上限和健康检查。
- 建立备份、PITR 与恢复流程。
- 记录容量、慢查询和存储增长证据。
- 完成受控故障与恢复演练。

## 架构约束

- 每个服务拥有独立 Schema。
- 禁止跨 Schema JOIN 和跨域写入。
- 业务 DDL 与 Flyway Migration 归应用仓库管理。
- 本仓库只提供数据库实例、角色、权限、存储和运维能力。
- 未通过恢复验证前，不标记为 prod-like 可用。

## 进入部署前必须明确

- 精确版本和镜像 Digest。
- 部署方式与拓扑。
- StorageClass、PVC 和容量。
- CPU、内存与连接数基线。
- 备份频率、保留、加密与存储位置。
- 恢复 Runbook 和业务校验项。
