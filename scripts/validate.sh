#!/usr/bin/env bash
set -euo pipefail

required_paths=(
  config/component-versions.yaml
  kubernetes/base/kustomization.yaml
  environments/local/kustomization.yaml
  environments/dev/kustomization.yaml
  environments/test/kustomization.yaml
  environments/prod-like/kustomization.yaml
  observability/otel-collector/collector.yaml
)

for path in "${required_paths[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "missing required file: $path" >&2
    exit 1
  fi
done

if command -v yamllint >/dev/null 2>&1; then
  mapfile -t yaml_files < <(find . -type f \( -name '*.yaml' -o -name '*.yml' \) -not -path './.git/*' | sort)
  yamllint -c .yamllint.yml "${yaml_files[@]}"
else
  echo "yamllint not installed; skipping YAML lint" >&2
fi

if command -v shellcheck >/dev/null 2>&1; then
  shellcheck scripts/*.sh
else
  echo "shellcheck not installed; skipping shell lint" >&2
fi

if grep -RInE 'image:[[:space:]]+[^[:space:]]+:latest([[:space:]]|$)' . \
  --include='*.yaml' --include='*.yml' --exclude-dir=.git; then
  echo "floating latest image tag is forbidden" >&2
  exit 1
fi

if find . -type f \( -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '*.jks' \) \
  -not -path './.git/*' | grep -q .; then
  echo "private key or keystore material must not be committed" >&2
  exit 1
fi

echo "infrastructure skeleton validation passed"
