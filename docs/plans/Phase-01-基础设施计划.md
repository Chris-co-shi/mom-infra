# Phase 01：基础设施技术骨架计划

- 状态：进行中
- 目标环境：local、dev
- 目标：建立可验证、可晋级的基础设施最小闭环，不直接追求完整类生产高可用

## 1. 完成定义

Phase 01 完成时应满足：

1. 组件版本目录不再全部为 `pending`。
2. 四套 Kustomize Overlay 能完成渲染校验。
3. Namespace、标签、命名和资源目录稳定。
4. Secret 管理方案已通过 ADR 决策。
5. PostgreSQL、Redis、Nacos、RocketMQ、Seata 至少完成单实例或最小拓扑 PoC。
6. OpenTelemetry Collector、Prometheus、Loki、Tempo、Grafana 能组成最小观测闭环。
7. Linux 与 Windows 校验脚本均可使用。
8. 至少完成 PostgreSQL 或 Redis 的一次备份与恢复验证。
9. 所有部署和恢复步骤都有中文 Runbook。

## 2. Slice 01：版本与来源冻结

### 工作

- 确认 k3s、PostgreSQL、Redis、Nacos、RocketMQ、Seata 和可观测性组件版本。
- 登记官方地址、许可证、Chart/Manifest 来源和镜像仓库。
- 禁止 `latest`、`stable` 等浮动 Tag。
- 为 `prod-like` 预留镜像 Digest 字段。

### 验收

- `config/component-versions.yaml` 无未解释的 `pending`。
- `THIRD-PARTY-NOTICES.md` 与版本目录一致。
- 校验脚本可拒绝浮动 Tag。

## 3. Slice 02：Kubernetes Base 与 Overlay

### 工作

- 完善 Namespace、通用标签和 Kustomization。
- 定义 local/dev/test/prod-like Overlay 差异。
- 建立标准资源标签：`app.kubernetes.io/*`。
- 增加 Kustomize 渲染校验。

### 验收

- 四套环境均能渲染。
- Base 不包含环境专属 Secret、域名和节点地址。
- Overlay Diff 清晰且无整套资源复制。

## 4. Slice 03：存储与 Secret 基线

### 工作

- 识别本地与 k3s 可用 StorageClass。
- 定义 PostgreSQL、Redis、RocketMQ 等 PVC 需求。
- 在 SOPS+age 与外部 Secret 方案间完成决策。
- 增加敏感文件扫描。

### 验收

- Git 历史和 PR 中无明文凭证。
- Stateful 组件的容量和访问模式已记录。
- Secret 可在 local/dev 通过受控方式注入。

## 5. Slice 04：核心中间件 PoC

### 工作顺序

```text
PostgreSQL
→ Redis
→ Nacos
→ RocketMQ
→ Seata
```

每个组件至少验证：

- 启动和健康检查。
- 持久化。
- 资源限制。
- 服务发现或客户端连接。
- 重启后的数据/状态行为。
- 日志与指标采集。
- 升级和恢复入口。

### 验收

应用侧 PoC 能完成：

- 连接 PostgreSQL。
- 访问 Redis。
- 注册到 Nacos。
- 生产和消费 RocketMQ 消息。
- 验证 Seata 与 Spring Boot 4/JDK 25 兼容性。

## 6. Slice 05：可观测性最小闭环

### 工作

- 部署 OpenTelemetry Collector。
- 部署 Prometheus、Loki、Tempo、Grafana。
- 配置统一的服务和环境标签。
- 接收 MOM Gateway 或示例服务的 OTLP 数据。

### 验收

- Grafana 能查询服务指标。
- 可以从日志中的 Trace ID 进入 Trace。
- 可以从 Trace 关联服务日志。
- Collector 故障和恢复行为有记录。

## 7. Slice 06：备份恢复最小验证

### 工作

- 为 PostgreSQL 或 Redis 建立第一份备份 Runbook。
- 执行备份、删除测试数据、恢复、业务验证。
- 记录耗时、恢复点、失败和证据。

### 验收

- 恢复后的数据与预期一致。
- Runbook 可由未参与编写的人重复执行。
- 明确当前 RPO/RTO 的实测值，而非目标口号。

## 8. Slice 07：CI 与校验门禁

### 工作

- YAML Lint。
- ShellCheck。
- PowerShell 基础检查。
- Kustomize Render。
- Kubernetes Schema 校验。
- 禁止浮动 Tag。
- Secret 和私钥扫描。
- Markdown 链接检查。

### 验收

- 错误 Manifest、浮动 Tag 和明显凭证能让 CI 失败。
- README 中的验证命令与 CI 一致。
- Windows 与 Linux 本地校验结果保持一致。

## 9. 暂不进入 Phase 01

- 完整生产级 PostgreSQL 高可用。
- 多机房容灾。
- 真实云 KMS。
- 自动化混沌工程平台。
- Kafka、Flink、IoTDB、Elasticsearch。
- 真实生产证书与真实业务数据。

## 10. 风险

| 风险 | 应对 |
|---|---|
| 组件版本与 JDK25/Boot4 不兼容 | 先做 PoC，记录兼容矩阵 |
| 本地存储无法模拟生产 | 明确差异，不夸大高可用结论 |
| Secret 方案选择过重 | local/dev 先满足安全与可操作性 |
| 同时部署过多中间件 | 按依赖顺序逐项验收 |
| 只部署不恢复 | 每个 Stateful 组件必须配恢复计划 |
| 文档与 Manifest 偏离 | CI、PR 清单和 Runbook 联动更新 |
