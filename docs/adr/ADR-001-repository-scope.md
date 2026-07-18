# ADR-001: Infrastructure repository scope

- Status: Accepted
- Date: 2026-07-18

## Decision

`mom-infra` is the single source of truth for deployment infrastructure and operational procedures.
Application repositories own build artifacts and application behavior; they do not own shared
cluster middleware or observability deployment.

## Consequences

- infrastructure changes can be reviewed independently from business code
- application teams must publish explicit runtime contracts
- environment drift becomes visible and reviewable
