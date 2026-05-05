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

$allowPath = ".\examples\governance\generated\sdk_response_req-allow-001.json"
$blockPath = ".\examples\governance\generated\sdk_response_req-block-001.json"
$receiptPath = ".\examples\governance\generated\receipts.ndjson"

if (-not (Test-Path -LiteralPath $allowPath)) { throw "Missing generated ALLOW response" }
if (-not (Test-Path -LiteralPath $blockPath)) { throw "Missing generated BLOCK response" }
if (-not (Test-Path -LiteralPath $receiptPath)) { throw "Missing generated receipts.ndjson" }

$allow = Get-Content -LiteralPath $allowPath -Raw | ConvertFrom-Json
$block = Get-Content -LiteralPath $blockPath -Raw | ConvertFrom-Json

if ($allow.decision -ne "ALLOW") { throw "ALLOW case failed" }
if ($block.decision -ne "BLOCK") { throw "BLOCK case failed" }

$receiptText = Get-Content -LiteralPath $receiptPath -Raw
if ($receiptText -like "*api_key*") { throw "Forbidden api_key text found" }
if ($receiptText -like "*secret*") { throw "Forbidden secret text found" }

Write-Host "AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK"
