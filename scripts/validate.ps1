$ErrorActionPreference = 'Stop'

$requiredPaths = @(
    'config/component-versions.yaml',
    'kubernetes/base/kustomization.yaml',
    'environments/local/kustomization.yaml',
    'environments/dev/kustomization.yaml',
    'environments/test/kustomization.yaml',
    'environments/prod-like/kustomization.yaml',
    'observability/otel-collector/collector.yaml'
)

foreach ($path in $requiredPaths) {
    if (-not (Test-Path $path -PathType Leaf)) {
        throw "Missing required file: $path"
    }
}

$latestTags = Get-ChildItem -Recurse -File -Include *.yaml,*.yml |
    Select-String -Pattern 'image:\s+\S+:latest(?:\s|$)'
if ($latestTags) {
    throw 'Floating latest image tag is forbidden.'
}

$privateMaterial = Get-ChildItem -Recurse -File -Include *.pem,*.key,*.p12,*.jks
if ($privateMaterial) {
    throw 'Private key or keystore material must not be committed.'
}

Write-Host 'Infrastructure skeleton validation passed.'
