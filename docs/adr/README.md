# 基础设施架构决策记录

ADR 用于记录影响长期架构、运维、安全和恢复能力的关键决策。

## 状态

- `Proposed`：待验证和评审。
- `Accepted`：当前有效。
- `Deprecated`：不再推荐，但保留历史。
- `Superseded`：已被新 ADR 替代。

## 决策清单

| ADR | 标题 | 状态 | 关联文档 |
|---|---|---|---|
| [ADR-001](ADR-001-基础设施仓库边界.md) | 基础设施仓库边界 | Accepted | [仓库边界](../architecture/仓库边界.md) |
| [ADR-002](ADR-002-使用Kustomize管理环境晋级.md) | 使用 Kustomize 管理环境晋级 | Accepted | [环境模型](../environments/环境模型与晋级规则.md) |
| [ADR-003](ADR-003-密钥不得明文进入Git.md) | 密钥不得明文进入 Git | Accepted | [安全与密钥管理](../security/安全与密钥管理.md) |
| [ADR-004](ADR-004-OpenTelemetry与Grafana可观测性栈.md) | OpenTelemetry 与 Grafana 可观测性栈 | Accepted | [可观测性基础设施](../observability/可观测性基础设施.md) |
| [ADR-005](ADR-005-组件版本与镜像锁定.md) | 组件版本与镜像锁定 | Accepted | [Phase 01 计划](../plans/Phase-01-基础设施计划.md) |
| [ADR-006](ADR-006-备份必须通过恢复验证.md) | 备份必须通过恢复验证 | Accepted | [备份恢复与容灾](../disaster-recovery/备份恢复与容灾.md) |
| [ADR-007](ADR-007-环境与集群拓扑.md) | 环境与集群拓扑 | Accepted | [环境模型](../environments/环境模型与晋级规则.md) |
| [ADR-008](ADR-008-第三方组件部署方式.md) | 第三方组件部署方式 | Accepted | [Phase 01 计划](../plans/Phase-01-基础设施计划.md) |
| [ADR-009](ADR-009-使用SOPS与age管理密钥.md) | 使用 SOPS 与 age 管理密钥 | Accepted | [安全与密钥管理](../security/安全与密钥管理.md) |

## 维护规则

1. 每个 ADR 只记录一个核心决策。
2. 已 Accepted 的 ADR 不直接改写历史结论。
3. 决策变化时新建 ADR，并将旧 ADR 标记为 Superseded。
4. ADR 必须包含背景、候选方案、决策、后果、风险和验证方式。
5. 配置或 Manifest 与 ADR 冲突时，必须修复偏离或正式替代决策。
