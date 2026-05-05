$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Safe API Adapter Dry-Run V1 verifier"

$required = @(
  "docs\SAFE_API_ADAPTER_DRY_RUN_V1.md",
  "examples\api-adapter\api_request_read_dryrun_v1.json",
  "examples\api-adapter\api_request_write_dryrun_v1.json",
  "scripts\RUN_SAFE_API_ADAPTER_DRY_RUN_V1.ps1"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing required file: $p"
  }
}

$output = powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\RUN_SAFE_API_ADAPTER_DRY_RUN_V1.ps1" 2>&1
$joined = ($output | Out-String)

if ($joined -notlike "*AION_SAFE_API_ADAPTER_DRY_RUN_V1_OK*") {
  Write-Host $joined
  throw "Safe API adapter dry-run marker missing"
}

$readReceipt = ".\examples\api-adapter\generated\api-dryrun-read-001.receipt.json"
$writeReceipt = ".\examples\api-adapter\generated\api-dryrun-write-001.receipt.json"

if (-not (Test-Path -LiteralPath $readReceipt)) { throw "Missing read receipt" }
if (-not (Test-Path -LiteralPath $writeReceipt)) { throw "Missing write receipt" }

$r1 = Get-Content -LiteralPath $readReceipt -Raw | ConvertFrom-Json
$r2 = Get-Content -LiteralPath $writeReceipt -Raw | ConvertFrom-Json

if ($r1.live_api_call_performed -ne $false) { throw "Read receipt must not perform live API call" }
if ($r2.live_api_call_performed -ne $false) { throw "Write receipt must not perform live API call" }
if ($r1.network_used -ne $false) { throw "Read receipt must not use network" }
if ($r2.network_used -ne $false) { throw "Write receipt must not use network" }
if ($r1.mutation_performed -ne $false) { throw "Read receipt must not mutate" }
if ($r2.mutation_performed -ne $false) { throw "Write receipt must not mutate" }

Write-Host "AION_SAFE_API_ADAPTER_DRY_RUN_V1_VERIFY_OK"
