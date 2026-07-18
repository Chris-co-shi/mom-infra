# Kubernetes resources

`base/` contains environment-neutral resources. Reusable cross-cutting fragments may later be added
under `components/`. Business workloads should consume image and runtime contracts from their source
repositories rather than duplicating source code here.
