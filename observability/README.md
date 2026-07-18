# Observability

The target pipeline is:

```text
applications and infrastructure
  -> OpenTelemetry Collector
  -> Prometheus / Loki / Tempo
  -> Grafana
```

Dashboards and alerts must cover platform health, middleware saturation, request latency, error
rates, Redis rate-limit rejections, message retries, tracing gaps, backup status, and recovery drills.
