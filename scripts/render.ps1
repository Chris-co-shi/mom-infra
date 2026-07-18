param(
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
$rootDirectory = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
    $OutputDirectory = Join-Path $rootDirectory '.tmp/rendered'
}

if (-not (Get-Command kustomize -ErrorAction SilentlyContinue)) {
    throw 'kustomize is required; expected version is recorded in config/component-versions.yaml'
}

if (Test-Path $OutputDirectory) {
    Remove-Item $OutputDirectory -Recurse -Force
}
New-Item $OutputDirectory -ItemType Directory -Force | Out-Null

foreach ($environment in @('local', 'dev', 'test', 'prod-like')) {
    $environmentPath = Join-Path $rootDirectory "environments/$environment"
    $outputPath = Join-Path $OutputDirectory "$environment.yaml"
    $rendered = & kustomize build $environmentPath
    if ($LASTEXITCODE -ne 0) {
        throw "kustomize build failed for $environment"
    }
    [System.IO.File]::WriteAllLines($outputPath, $rendered)
    Write-Host "rendered $environment -> $outputPath"
}
