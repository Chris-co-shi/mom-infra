# Repository boundaries

## Owned here

- Kubernetes and k3s deployment resources
- middleware and observability configuration
- environment overlays and promotion rules
- infrastructure validation, backup, restore, and fault-drill automation
- operational runbooks and disaster-recovery evidence

## Not owned here

- Java, Python, TypeScript, or Vue application source
- database DDL owned by business services
- domain-specific RocketMQ topics and payload schemas
- PCS or WCS equipment state-machine code
- Web or PDA prototypes

Business repositories may contribute deployment inputs such as image coordinates, ports, health
endpoints, and resource profiles. `mom-infra` converts those inputs into environment-specific
runtime configuration without taking ownership of application behavior.
