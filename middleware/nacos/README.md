# Nacos

本目录负责 Nacos 注册发现与配置中心的部署和运行治理。

## V1 目标

- 支持 MOM、PCS、WCS 服务注册与发现。
- 使用 `spring.config.import` 加载配置。
- 定义 Namespace、Group、Data ID 和环境隔离约定。
- 启用认证并限制管理入口。
- 验证持久化、健康检查、客户端重连和配置回滚。

## 进入部署前必须明确

- 精确版本及与 Spring Boot 4 / Spring Cloud Alibaba 的兼容性。
- 单机 PoC 与 test/prod-like 拓扑。
- PostgreSQL 持久化依赖。
- Namespace 与 Group 命名规范。
- 管理账号和 Secret 注入。
- 配置导出、备份和恢复方式。
- Nacos 不可用时应用的缓存、重连和降级行为。

## 故障验证

- 注册中心短时不可用。
- 配置中心不可用。
- 错误配置发布和回滚。
- 客户端重连风暴。
- 服务恢复后的实例和配置一致性。
