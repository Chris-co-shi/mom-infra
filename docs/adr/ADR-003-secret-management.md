# ADR-003: Secret-management boundary

- Status: Accepted
- Date: 2026-07-18

## Decision

Plaintext credentials, private keys, and generated secret manifests are forbidden in Git. The first
deployable slice must choose and document a secret workflow such as SOPS with age or an external
secret manager. Until then, manifests may reference secret names but must not contain real values.
