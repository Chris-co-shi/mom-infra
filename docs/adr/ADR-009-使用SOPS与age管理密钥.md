# ADR-009：使用 SOPS 与 age 管理密钥

- 状态：Accepted
- 日期：2026-07-18
- 关联 ADR：[ADR-003：密钥不得明文进入 Git](ADR-003-密钥不得明文进入Git.md)
- 关联文档：[安全与密钥管理](../security/安全与密钥管理.md)

## 1. 背景

ADR-003 已禁止明文凭证进入 Git，但尚未完成工具选型。当前环境以本地 Windows、macOS、Linux 和自建 k3s 为主，没有稳定依赖云 KMS、Vault 或其他外部密钥平台。

## 2. 候选方案

### 方案 A：SOPS + age

优点：离线可用、跨平台、适合 Git 审查，不依赖云服务。

风险：必须安全保管 age 私钥，并建立轮换和恢复流程。

### 方案 B：External Secrets + 外部密钥服务

优点：运行时集中管理和轮换能力更强。

风险：Phase 01 需要额外部署、认证和恢复外部密钥服务，本地环境复杂度过高。

### 方案 C：人工创建 Kubernetes Secret

优点：PoC 快。

风险：不可审查、不可重复、容易漂移，不满足 Git 权威源要求。

## 3. 决策

Phase 01 采用 SOPS + age：

1. Git 可保存经过 SOPS 加密的 YAML 文件，但不得保存 age 私钥。
2. 每个环境使用独立 age recipient；禁止共用 `prod-like` 与低环境私钥。
3. `.sops.yaml` 只保存公钥 recipient 和加密规则。
4. age identity 由操作者安全保管，并通过环境变量或受控文件路径提供给 SOPS。
5. CI 默认只校验密文结构，不解密真实环境 Secret。
6. 需要部署验证时，通过受保护的 CI Secret 或人工受控流程提供测试环境 identity。
7. External Secrets 保留为后续演进方案；引入时必须新增 ADR，并定义外部密钥服务的高可用、备份和恢复。

## 4. 工具基线

Phase 01 工具基线：

- SOPS `3.13.0`
- age `1.3.1`

工具升级必须更新组件目录、验证 Linux/Windows/macOS 解密兼容性，并保留回退版本。

## 5. 文件与命名约定

```text
security/sops/
├── README.md
├── .sops.yaml.example
└── templates/
```

- 明文模板只能包含占位符，不包含可用凭证。
- 加密文件建议使用 `*.sops.yaml` 后缀。
- 解密输出只能进入临时目录，使用后必须清理。
- 禁止把解密文件、age identity、`.env` 或生成后的明文 Secret Manifest 提交 Git。

## 6. 密钥生命周期

必须覆盖：

1. 生成 recipient/identity。
2. 公钥登记。
3. identity 分发与最小权限保存。
4. 加密和解密。
5. recipient 轮换与重新加密。
6. identity 丢失后的恢复。
7. 人员离开或设备丢失后的撤销处置。

## 7. 后果

正向：Phase 01 获得可审查、可重复、跨平台且无需外部服务的 Secret 工作流。

负向：age 私钥成为关键恢复材料；若无备份会导致仓库中的密文不可恢复。

## 8. 验证

- 仓库中不存在 age identity 或明文凭证。
- 示例文件能在 Linux、Windows、macOS 使用相同 recipient 规则加密。
- 完成一次测试凭证轮换和重新加密。
- 完成一次 identity 备份恢复演练。
- CI 能识别未加密 Kubernetes Secret 和常见凭证模式。
