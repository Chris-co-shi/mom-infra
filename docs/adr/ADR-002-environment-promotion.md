# ADR-002: Environment promotion through overlays

- Status: Accepted
- Date: 2026-07-18

## Decision

Use a shared Kubernetes base and Kustomize overlays for `local`, `dev`, `test`, and `prod-like`.
Helm may package third-party middleware, but environment differences remain reviewable in this
repository and must not be hidden in operator workstations.
