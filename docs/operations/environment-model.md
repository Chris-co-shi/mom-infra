# Environment model

| Environment | Purpose | Persistence | Availability expectation |
|---|---|---|---|
| local | Developer verification | Disposable | Single-node acceptable |
| dev | Shared integration | Rebuildable | Short interruptions acceptable |
| test | End-to-end and fault tests | Backed up | Mirrors critical topology |
| prod-like | Interview demo and production simulation | Protected | Three-node k3s target |

## Rules

1. Base manifests remain environment-neutral.
2. Environment differences are expressed only through overlays and external secret material.
3. `prod-like` must use pinned image digests before deployment.
4. Secrets are never committed in plaintext.
5. Every destructive operation requires a documented rollback or restore step.
6. Manual cluster changes must be reconciled into Git or reverted.
