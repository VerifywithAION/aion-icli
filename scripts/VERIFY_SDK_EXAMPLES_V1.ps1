$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI SDK Examples V1 verifier"

$required = @(
  "docs\SDK_EXAMPLES_V1.md",
  "examples\sdk\sdk_request_safe_read_v1.json",
  "examples\sdk\sdk_request_review_write_v1.json",
  "examples\sdk\sdk_request_model_envelope_v1.json",
  "examples\sdk\sdk_request_api_envelope_v1.json",
  "scripts\RUN_SDK_EXAMPLES_V1.ps1"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing required file: $p"
  }
}

$output = powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\RUN_SDK_EXAMPLES_V1.ps1" 2>&1
$joined = ($output | Out-String)

if ($joined -notlike "*AION_SDK_EXAMPLES_V1_OK*") {
  Write-Host $joined
  throw "SDK examples marker missing"
}

$receipts = @(
  ".\examples\sdk\generated\sdk-safe-read-001.receipt.json",
  ".\examples\sdk\generated\sdk-review-write-001.receipt.json",
  ".\examples\sdk\generated\sdk-model-envelope-001.receipt.json",
  ".\examples\sdk\generated\sdk-api-envelope-001.receipt.json"
)

foreach ($r in $receipts) {
  if (-not (Test-Path -LiteralPath $r)) {
    throw "Missing SDK receipt: $r"
  }

  $json = Get-Content -LiteralPath $r -Raw | ConvertFrom-Json

  if ($json.network_used -ne $false) { throw "SDK receipt used network: $r" }
  if ($json.mutation_performed -ne $false) { throw "SDK receipt performed mutation: $r" }
  if ($json.execution_performed -ne $false) { throw "SDK receipt performed execution: $r" }
  if ($json.provider_called -ne $false) { throw "SDK receipt called provider: $r" }
  if ($json.api_called -ne $false) { throw "SDK receipt called API: $r" }
}

Write-Host "AION_SDK_EXAMPLES_V1_VERIFY_OK"
