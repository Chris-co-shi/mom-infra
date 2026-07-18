# ADR-004: Observability stack

- Status: Accepted
- Date: 2026-07-18

## Decision

Use OpenTelemetry Collector as the telemetry ingress, Prometheus for metrics, Loki for logs, Tempo
for traces, and Grafana for investigation and dashboards. Applications export OTLP and expose
Prometheus-compatible metrics where appropriate.

Technical trace identifiers do not replace business correlation identifiers such as workflow ID,
event ID, command ID, production order number, factory ID, or batch number.
