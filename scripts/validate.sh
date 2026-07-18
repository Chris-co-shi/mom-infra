#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${root_dir}"

required_commands=(python3 yamllint shellcheck kustomize kubeconform gitleaks)
for command_name in "${required_commands[@]}"; do
  if ! command -v "${command_name}" >/dev/null 2>&1; then
    echo "required validation tool is missing: ${command_name}" >&2
    exit 1
  fi
done

python3 scripts/validate.py --mode source

mapfile -t yaml_files < <(
  find . -type f \( -name '*.yaml' -o -name '*.yml' \) \
    -not -path './.git/*' \
    -not -path './.tmp/*' \
    -not -path './rendered/*' \
    | sort
)
yamllint -c .yamllint.yml "${yaml_files[@]}"
shellcheck scripts/*.sh

bash scripts/render.sh
python3 scripts/validate.py --mode rendered --rendered-dir .tmp/rendered

for environment in local dev test prod-like; do
  kubeconform -strict -summary ".tmp/rendered/${environment}.yaml"
done

gitleaks dir "${root_dir}" --redact --no-banner

echo "infrastructure validation passed"
