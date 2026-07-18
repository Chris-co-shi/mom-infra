#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
output_dir="${1:-${root_dir}/.tmp/rendered}"
environments=(local dev test prod-like)

if ! command -v kustomize >/dev/null 2>&1; then
  echo "kustomize is required; expected version is recorded in config/component-versions.yaml" >&2
  exit 1
fi

rm -rf "${output_dir}"
mkdir -p "${output_dir}"

for environment in "${environments[@]}"; do
  kustomize build "${root_dir}/environments/${environment}" > "${output_dir}/${environment}.yaml"
  echo "rendered ${environment} -> ${output_dir}/${environment}.yaml"
done
