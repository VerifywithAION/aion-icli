$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Local Governance Proxy V1"

$ExampleDir = Join-Path $Repo "examples\governance"
$GeneratedDir = Join-Path $ExampleDir "generated"

if (-not (Test-Path -LiteralPath $ExampleDir)) { throw "Missing examples/governance directory" }

New-Item -ItemType Directory -Force -Path $GeneratedDir | Out-Null

$inputFiles = Get-ChildItem -LiteralPath $ExampleDir -Filter "sdk_request_*.json" -File -ErrorAction SilentlyContinue
if ($null -eq $inputFiles -or $inputFiles.Count -eq 0) { throw "No sdk_request_*.json files found" }

$receiptStream = Join-Path $GeneratedDir "receipts.ndjson"
if (Test-Path -LiteralPath $receiptStream) { Remove-Item -LiteralPath $receiptStream -Force }

foreach ($file in $inputFiles) {
  $json = Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json
  $risk = ""
  if ($json.target -and ($json.target.PSObject.Properties.Name -contains "risk_hint")) {
    $risk = [string]$json.target.risk_hint
  }

  if ($risk.ToLowerInvariant() -eq "high") {
    $decision = "BLOCK"
    $reason = "RISK_HINT_HIGH"
  } elseif ($risk.ToLowerInvariant() -eq "low") {
    $decision = "ALLOW"
    $reason = "RISK_HINT_LOW"
  } else {
    $decision = "WARN"
    $reason = "RISK_HINT_MISSING"
  }

  $receipt = [ordered]@{
    receipt_fingerprint = ""
    agent = $json.agent
    claim_id = $json.claim_id
    claim_type = $json.claim_type
    decision = $decision
    reason_code = $reason
    policy_id = $json.policy_id
    timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    runtime_boundaries = [ordered]@{
      offline_mode = $true
      network_used = $false
      external_api_called = $false
      external_model_called = $false
      autonomous_execution_performed = $false
      local_receipts_only = $true
    }
  }

  $canonical = ($receipt | ConvertTo-Json -Depth 20 -Compress)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($canonical)
  $hash = $sha.ComputeHash($bytes)
  $hex = -join ($hash | ForEach-Object { $_.ToString("x2") })
  $receipt.receipt_fingerprint = $hex

  $response = [ordered]@{
    decision = $decision
    reason_code = $reason
    receipt = $receipt
  }

  $outFile = Join-Path $GeneratedDir ("sdk_response_" + $json.claim_id + ".json")
  $response | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $outFile -Encoding UTF8
  ($receipt | ConvertTo-Json -Depth 20 -Compress) | Add-Content -LiteralPath $receiptStream -Encoding UTF8

  Write-Host ("Processed " + $file.Name + ": " + $decision)
}

Write-Host ("Wrote generated outputs to " + $GeneratedDir)
Write-Host "AION_LOCAL_GOVERNANCE_PROXY_V1_DEMO_OK"
