$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Local Governance Proxy V1 verifier"

$required = @(
  "docs\CONNECTOR_SDK_CONTRACT_V1.md",
  "docs\LOCAL_GOVERNANCE_PROXY_V1.md",
  "schemas\aion-governance-receipt-v1.schema.json",
  "examples\governance\sdk_request_allow.json",
  "examples\governance\sdk_request_block.json",
  "scripts\RUN_LOCAL_GOVERNANCE_PROXY_DEMO_V1.ps1"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) { throw "Missing required file: $p" }
}

powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\RUN_LOCAL_GOVERNANCE_PROXY_DEMO_V1.ps1"

$allow = Get-Content -LiteralPath ".\examples\governance\sdk_response_req-allow-001.json" -Raw | ConvertFrom-Json
$block = Get-Content -LiteralPath ".\examples\governance\sdk_response_req-block-001.json" -Raw | ConvertFrom-Json

if ($allow.decision -ne "ALLOW") { throw "ALLOW case failed" }
if ($block.decision -ne "BLOCK") { throw "BLOCK case failed" }

if (-not (Test-Path -LiteralPath ".\examples\governance\receipts.ndjson")) { throw "Missing receipts.ndjson" }

$receiptText = Get-Content -LiteralPath ".\examples\governance\receipts.ndjson" -Raw
if ($receiptText -like "*api_key*") { throw "Forbidden api_key text found" }
if ($receiptText -like "*secret*") { throw "Forbidden secret text found" }

Write-Host "AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK"
