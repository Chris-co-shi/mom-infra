# ADR-002：使用 Kustomize 管理环境晋级

- 状态：Accepted
- 日期：2026-07-18
- 关联文档：[环境模型与晋级规则](../environments/环境模型与晋级规则.md)

## 1. 背景

项目需要维护 local、dev、test、prod-like 四套环境。若每套环境复制一份完整 Manifest，配置会快速分叉，难以确认差异和回滚。

## 2. 候选方案

### 方案 A：每个环境独立维护 Manifest

优点：直观。

缺点：重复严重、差异隐蔽、长期漂移风险高。

### 方案 B：Helm 统一管理全部应用和环境

优点：模板能力强。

缺点：环境差异可能隐藏在复杂 Values 和模板逻辑中，调试与审查成本高。

### 方案 C：共享 Base + Kustomize Overlay

优点：差异显式、渲染结果可审查、适合原生 Kubernetes 资源。

缺点：复杂第三方中间件仍可能需要 Helm。

## 3. 决策

应用和共享 Kubernetes 资源采用方案 C。第三方中间件可以使用官方 Helm Chart，但环境差异、版本和 Values 必须保留在本仓库并可审查。

## 4. 实施约束

- Base 保持环境无关。
- Overlay 只包含必要差异。
- 禁止复制整套 Base 到环境目录。
- Secret 真实值不进入 Overlay。
- 所有 Overlay 必须通过渲染校验。

## 5. 后果

正向：

- 环境 Diff 清晰。
- 配置可以逐级晋级。
- 漂移和未评审差异更容易发现。

负向：

- 需要掌握 Kustomize patch 规则。
- Helm 与 Kustomize 共存时需要明确边界。

## 6. 验证

local、dev、test、prod-like 均能独立渲染，Base 中不存在环境专属域名、密码、节点 IP 或固定 StorageClass。
