# Kubernetes 资源

本目录保存环境无关的 Kubernetes Base 与后续可复用组件。

## 目录职责

- `base/`：Namespace、通用标签和环境无关资源。
- `components/`：后续用于跨环境复用的 Kustomize Components。

## 约束

- 不在 Base 中写入环境专属域名、节点 IP、密码或真实 Secret。
- 应用工作负载从对应应用仓库获取镜像和运行契约，不复制源码。
- 环境差异统一进入 `environments/*` Overlay。
- 资源必须包含统一的 `app.kubernetes.io/*` 标签。
- test/prod-like 禁止使用浮动镜像 Tag。

详细架构见：[基础设施总体架构](../docs/architecture/基础设施总体架构.md)。
