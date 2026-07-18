# Phase 01A：可执行基础与校验门禁

- 状态：进行中
- 目标环境：local、dev；test、prod-like 只要求可渲染和策略校验
- 上位计划：[Phase 01 基础设施计划](Phase-01-基础设施计划.md)

## 1. 目标

在部署第一个有状态中间件之前，建立可重复渲染、可跨平台验证、可审查 Secret、可追踪版本状态的基础设施执行基线。

Phase 01A 不部署 PostgreSQL、Redis、Nacos、RocketMQ 或 Seata。

## 2. 范围

### 包含

- 明确环境与集群拓扑。
- 固定 Namespace 名称，使用环境标签而非名称前缀。
- 明确第三方组件的 Manifest、Helm、Operator 选择规则。
- 选择 SOPS + age 作为 Phase 01 Secret 方案。
- 四套 Overlay 的 Kustomize 渲染。
- Kubernetes Schema 校验。
- 明文 Secret、浮动镜像、高风险工作负载和过度 RBAC 检查。
- Gitleaks 扫描。
- Linux 与 Windows 双平台 CI。
- 组件目录表达“已锁定、已选择、待候选、待验证”等状态。

### 不包含

- 中间件正式部署。
- PostgreSQL 高可用。
- External Secrets、Vault 或云 KMS。
- GitOps Controller。
- 完整 NetworkPolicy、ResourceQuota 和 Pod Security 基线。
- 业务应用部署。

## 3. Slice

### Slice 01：架构决策

- [x] ADR-007：环境与集群拓扑。
- [x] ADR-008：第三方组件部署方式。
- [x] ADR-009：SOPS + age Secret 管理。

### Slice 02：Overlay 契约

- [x] 删除会改变 Namespace 的 `namePrefix`。
- [x] 四套环境增加 `mom.io/environment` 标签。
- [x] 渲染结果验证固定 Namespace 集合。

### Slice 03：跨平台校验

- [x] Python 统一策略校验器。
- [x] Linux 渲染与校验脚本。
- [x] Windows 渲染与校验脚本。
- [x] Kustomize Render。
- [x] Kubeconform Schema 校验。
- [x] Gitleaks 工作区扫描。
- [x] GitHub Actions Linux/Windows Job。

### Slice 04：Secret 工作流

- [x] SOPS + age 使用说明。
- [x] 多环境 recipient 配置示例。
- [x] age identity 与解密文件忽略规则。
- [ ] 由仓库所有者生成四套环境公钥并提交真实 `.sops.yaml`。
- [ ] 完成测试密文的加密、解密和 recipient 轮换验证。

### Slice 05：版本目录

- [x] 固定校验工具版本。
- [x] 增加平台兼容目标。
- [x] 为未验证组件记录明确状态和下一验证动作。
- [ ] 记录现有三节点 k3s 的实际版本、StorageClass 和节点信息。

## 4. 验收标准

1. `local`、`dev`、`test`、`prod-like` 均可执行 `kustomize build`。
2. 四套渲染结果均包含五个固定 Namespace，并带正确环境标签。
3. 渲染结果通过 Kubeconform。
4. 明文 Kubernetes Secret、浮动镜像 Tag、无 Tag 镜像、`prod-like` 非 Digest 镜像会使校验失败。
5. `privileged`、`hostNetwork`、`hostPID`、`hostIPC`、`hostPath` 和 `cluster-admin` 绑定默认失败，显式例外必须记录原因。
6. Gitleaks 检测到常见凭证时 CI 失败。
7. Linux 与 Windows Job 均通过。
8. 组件目录中不存在含义不明的 `pending`；未验证项必须包含状态和下一动作。
9. Secret 工具选型完成，age identity 不进入 Git。

## 5. 本地命令

Linux/macOS：

```bash
./scripts/validate.sh
```

Windows：

```powershell
./scripts/validate.ps1
```

仅渲染：

```bash
make render
```

## 6. 完成后的下一阶段

Phase 01A 通过后进入 Phase 01B：PostgreSQL local/dev 纵向 PoC，必须同时完成部署、持久化、探针、资源限制、监控、备份、删除测试数据、恢复和业务验证。
