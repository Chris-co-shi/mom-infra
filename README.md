# MOM Infrastructure

`mom-infra` is the infrastructure-as-code and operations repository for the Industrial MOM project.
It owns k3s deployment foundations, middleware provisioning, observability, backup and recovery,
security baselines, environment promotion, and production-like fault drills.

## Scope

- k3s and Kubernetes resource organization
- PostgreSQL, Redis, Nacos, RocketMQ, and Seata deployment assets
- OpenTelemetry Collector, Prometheus, Grafana, Tempo, and Loki
- ingress, certificates, network policy, and secret-management conventions
- backup, restore, rolling upgrade, rollback, and fault-drill runbooks
- local, development, test, and production-like environment overlays

Application source code belongs in `mom-platform`, `pcs-platform`, `wcs-platform`, `mom-web`,
`mom-mobile`, or `erp-simulator`; it must not be added here.

## Repository structure

```text
mom-infra/
├── config/                 # Version catalog and shared infrastructure metadata
├── docs/                   # ADRs, architecture notes, and runbooks
├── environments/           # Environment-specific Kustomize overlays
├── kubernetes/             # Shared Kubernetes base resources
├── middleware/             # Middleware deployment boundaries and values
├── observability/          # Metrics, logs, traces, and dashboards
├── networking/             # Ingress, DNS, TLS, and network policy
├── security/               # Secrets, RBAC, image, and supply-chain policies
├── backup/                 # Backup jobs and restore procedures
├── disaster-recovery/      # Recovery objectives and recovery drills
├── fault-drills/           # Controlled production-like failure scenarios
└── scripts/                # Validation and operational helper scripts
```

## Current status

This initial skeleton defines ownership, directory contracts, validation gates, namespaces, and
observability configuration. It intentionally does **not** deploy production middleware yet.
Component versions, storage classes, resource requests, topology, and credentials must pass a
compatibility and capacity review before manifests are promoted.

## Validate locally

Linux/macOS:

```bash
./scripts/validate.sh
```

Windows PowerShell:

```powershell
./scripts/validate.ps1
```

## Environment promotion

```text
local -> dev -> test -> prod-like
```

Each promotion must preserve immutable source manifests and introduce differences only through the
environment overlay. Direct edits to a running cluster are considered drift and must be reconciled
back into this repository.

## License

MIT. Third-party components retain their own licenses; see `THIRD-PARTY-NOTICES.md`.
