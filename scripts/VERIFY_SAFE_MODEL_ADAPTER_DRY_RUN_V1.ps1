$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Safe Model Adapter Dry-Run V1 verifier"

$required = @(
  "docs\SAFE_MODEL_ADAPTER_DRY_RUN_V1.md",
  "examples\model-adapter\model_request_safe_dryrun_v1.json",
  "examples\model-adapter\model_request_review_dryrun_v1.json",
  "scripts\RUN_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing required file: $p"
  }
}

$output = powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\RUN_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1" 2>&1
$joined = ($output | Out-String)

if ($joined -notlike "*AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_OK*") {
  Write-Host $joined
  throw "Safe model adapter dry-run marker missing"
}

$safeReceipt = ".\examples\model-adapter\generated\model-dryrun-safe-001.receipt.json"
$reviewReceipt = ".\examples\model-adapter\generated\model-dryrun-review-001.receipt.json"

if (-not (Test-Path -LiteralPath $safeReceipt)) { throw "Missing safe model receipt" }
if (-not (Test-Path -LiteralPath $reviewReceipt)) { throw "Missing review model receipt" }

$r1 = Get-Content -LiteralPath $safeReceipt -Raw | ConvertFrom-Json
$r2 = Get-Content -LiteralPath $reviewReceipt -Raw | ConvertFrom-Json

if ($r1.provider_called -ne $false) { throw "Safe receipt must not call provider" }
if ($r2.provider_called -ne $false) { throw "Review receipt must not call provider" }
if ($r1.model_called -ne $false) { throw "Safe receipt must not call model" }
if ($r2.model_called -ne $false) { throw "Review receipt must not call model" }
if ($r1.network_used -ne $false) { throw "Safe receipt must not use network" }
if ($r2.network_used -ne $false) { throw "Review receipt must not use network" }
if ($r1.external_tool_used -ne $false) { throw "Safe receipt must not use external tool" }
if ($r2.external_tool_used -ne $false) { throw "Review receipt must not use external tool" }
if ($r1.mutation_performed -ne $false) { throw "Safe receipt must not mutate" }
if ($r2.mutation_performed -ne $false) { throw "Review receipt must not mutate" }

Write-Host "AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_VERIFY_OK"
