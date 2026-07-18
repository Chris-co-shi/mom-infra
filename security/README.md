# 安全

本目录管理 Kubernetes RBAC、Namespace 安全边界、Secret 工作流、镜像来源、容器安全上下文和供应链策略。

## 计划能力

- 最小权限 ServiceAccount 与 RBAC。
- Secret 加密、注入、轮换和撤销。
- 镜像仓库、版本、Digest 和来源校验。
- 容器 `securityContext` 基线。
- 高风险配置检查：privileged、hostNetwork、hostPath 等。
- Admission Policy 与镜像漏洞证据。
- TLS、证书和管理入口安全。

## 强制规则

- 真实凭证、Token、私钥和生成后的 Secret Manifest 禁止进入 Git。
- 应用不得共享长期高权限 ServiceAccount。
- 管理端口不默认暴露公网。
- test/prod-like 关键镜像使用固定 Digest。
- 临时高权限和网络放行必须有清理步骤。

详细设计见：[安全与密钥管理](../docs/security/安全与密钥管理.md)。
