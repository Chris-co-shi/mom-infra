# 第三方组件声明

`mom-infra` 会部署和配置多个第三方基础设施组件。除非在本文件和来源登记中明确说明，本仓库不复制这些项目的源代码。

## 登记要求

每个进入可部署环境的第三方组件必须记录：

- 项目名称。
- 精确版本。
- 官方上游地址。
- 许可证。
- Helm Chart、Operator 或 Manifest 来源。
- 镜像仓库、Tag 和 Digest。
- 是否修改上游配置或模板。
- NOTICE、署名或再分发要求。
- 最后核验日期。

组件版本和来源的权威清单为 [`config/component-versions.yaml`](config/component-versions.yaml)。本文件用于补充许可证、再分发和本地修改说明。

## V1 计划组件

| 组件 | 用途 | 版本状态 | 许可证/来源状态 |
|---|---|---|---|
| k3s | Kubernetes 发行版 | 待兼容性冻结 | 待登记 |
| PostgreSQL | 关系型数据库 | 待兼容性冻结 | 待登记 |
| Redis | 缓存、限流和幂等辅助 | 待兼容性冻结 | 待登记 |
| Nacos | 注册发现与配置 | 待兼容性冻结 | 待登记 |
| RocketMQ | 领域事件与异步消息 | 待兼容性冻结 | 待登记 |
| Seata | 受限范围的分布式事务 | 待兼容性冻结 | 待登记 |
| OpenTelemetry Collector | 遥测采集与转发 | 待兼容性冻结 | 待登记 |
| Prometheus | 指标 | 待兼容性冻结 | 待登记 |
| Loki | 日志 | 待兼容性冻结 | 待登记 |
| Tempo | Trace | 待兼容性冻结 | 待登记 |
| Grafana | 统一可视化与调查 | 待兼容性冻结 | 待登记 |

> [!WARNING]
> 在精确版本、上游来源、许可证和镜像 Digest 未完成核验前，不得将对应组件标记为 prod-like 已批准。

## 本地修改

若修改第三方 Helm Chart、Operator、Manifest 或镜像：

1. 记录原始版本和 Commit。
2. 保存可审查的 Patch 或 Overlay。
3. 说明修改原因和影响。
4. 核验许可证是否允许该使用方式。
5. 在升级时重新评估本地修改。

## 禁止事项

- 使用无法追溯来源的镜像。
- 使用 `latest` 等浮动 Tag 进入 test/prod-like。
- 删除上游许可证或 NOTICE。
- 通过批量改名将第三方源码伪装成自研代码。
- 只在个人电脑记录版本和修改，不进入 Git。
