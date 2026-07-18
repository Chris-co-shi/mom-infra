$ErrorActionPreference = 'Stop'
$rootDirectory = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $rootDirectory

foreach ($commandName in @('python', 'yamllint', 'kustomize', 'kubeconform', 'gitleaks')) {
    if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
        throw "Required validation tool is missing: $commandName"
    }
}

& python scripts/validate.py --mode source
if ($LASTEXITCODE -ne 0) {
    throw 'Source policy validation failed.'
}

$yamlFiles = Get-ChildItem $rootDirectory -Recurse -File -Include *.yaml,*.yml |
    Where-Object {
        $_.FullName -notmatch '[\\/]\.git[\\/]' -and
        $_.FullName -notmatch '[\\/]\.tmp[\\/]' -and
        $_.FullName -notmatch '[\\/]rendered[\\/]'
    } |
    ForEach-Object { $_.FullName }

& yamllint -c (Join-Path $rootDirectory '.yamllint.yml') @yamlFiles
if ($LASTEXITCODE -ne 0) {
    throw 'YAML lint failed.'
}

& (Join-Path $PSScriptRoot 'render.ps1')

& python scripts/validate.py --mode rendered --rendered-dir .tmp/rendered
if ($LASTEXITCODE -ne 0) {
    throw 'Rendered policy validation failed.'
}

foreach ($environment in @('local', 'dev', 'test', 'prod-like')) {
    $manifest = Join-Path $rootDirectory ".tmp/rendered/$environment.yaml"
    & kubeconform -strict -summary $manifest
    if ($LASTEXITCODE -ne 0) {
        throw "Kubernetes schema validation failed for $environment."
    }
}

& gitleaks dir $rootDirectory --redact --no-banner
if ($LASTEXITCODE -ne 0) {
    throw 'Gitleaks detected a secret or failed to scan the repository.'
}

Write-Host 'Infrastructure validation passed.'
