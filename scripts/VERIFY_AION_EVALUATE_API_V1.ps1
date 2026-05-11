$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$src = ".\src\aion_evaluate_api.py"
$run = ".\scripts\RUN_AION_EVALUATE_API_V1.ps1"
$demo = ".\scripts\RUN_AION_EVALUATE_API_V1_DEMO.ps1"

if(-not (Test-Path -LiteralPath $src)){ throw "Missing $src" }
if(-not (Test-Path -LiteralPath $run)){ throw "Missing $run" }
if(-not (Test-Path -LiteralPath $demo)){ throw "Missing $demo" }

python -m py_compile $src
if($LASTEXITCODE -ne 0){ throw "Python compile failed for $src" }

$server = Start-Process -FilePath python -ArgumentList ".\src\aion_evaluate_api.py" -WorkingDirectory $Repo -WindowStyle Hidden -PassThru
try {
  Start-Sleep -Seconds 2
  $health = Invoke-RestMethod -Uri "http://127.0.0.1:8765/health" -Method Get
  if($health.status -ne "ok"){ throw "Health status not ok" }

  $flagged = @{
    source = "BuzzShield"
    chain = "ethereum"
    contract_address = "0xabc123abc123abc123abc123abc123abc123abc1"
    score = 25
    verdict = "FLAGGED"
    patterns = @("drain")
    summary = "Detected high-risk drain pattern."
    confidence = 0.93
    recommended_action = "block"
  } | ConvertTo-Json -Depth 8

  $resp = Invoke-RestMethod -Uri "http://127.0.0.1:8765/evaluate" -Method Post -Body $flagged -ContentType "application/json"
  if($resp.governance_decision -ne "BLOCK"){ throw "Expected BLOCK decision" }
  if($resp.boundary -ne "LOCAL_ONLY"){ throw "boundary mismatch" }
  if($resp.network -ne "NOT_USED"){ throw "network mismatch" }
  if($resp.mutation -ne "NOT_PERFORMED"){ throw "mutation mismatch" }
  if(-not $resp.receipt_path){ throw "receipt_path missing" }

  $receiptPath = Join-Path $Repo ($resp.receipt_path -replace '/', '\')
  if(-not (Test-Path -LiteralPath $receiptPath)){ throw "receipt_path does not exist: $receiptPath" }
}
finally {
  if($server -and -not $server.HasExited){
    Stop-Process -Id $server.Id -Force
  }
}

Write-Host "AION_EVALUATE_API_V1_VERIFY_OK"
