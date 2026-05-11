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

# Clean up any stale listener on port 8765 before starting verifier-owned server.
if (Get-Command Get-NetTCPConnection -ErrorAction SilentlyContinue) {
  $listeners = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue
  foreach($l in $listeners){
    try { Stop-Process -Id $l.OwningProcess -Force -ErrorAction SilentlyContinue } catch {}
  }
}

$server = Start-Process -FilePath python -ArgumentList ".\src\aion_evaluate_api.py" -WorkingDirectory $Repo -WindowStyle Hidden -PassThru
try {
  $health = $null
  for($i=0; $i -lt 20; $i++){
    try {
      $health = Invoke-RestMethod -Uri "http://127.0.0.1:8765/health" -Method Get -TimeoutSec 2
      break
    } catch {
      Start-Sleep -Milliseconds 250
    }
  }
  if(-not $health){ throw "Health endpoint not reachable on 127.0.0.1:8765" }
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
  if($resp.execution -ne "NOT_PERFORMED"){ throw "execution mismatch" }
  if(-not $resp.receipt_path){ throw "receipt_path missing" }
  if(-not $resp.PSObject.Properties.Name.Contains("receipt_abs_path")){ throw "receipt_abs_path missing" }
  if(-not $resp.PSObject.Properties.Name.Contains("receipt_written")){ throw "receipt_written missing" }
  if(-not $resp.PSObject.Properties.Name.Contains("receipt_sha256")){ throw "receipt_sha256 missing" }
  if(-not $resp.receipt_abs_path){ throw "receipt_abs_path empty" }
  if($resp.receipt_written -ne $true){ throw "receipt_written is not true" }
  if(-not $resp.receipt_sha256){ throw "receipt_sha256 empty" }

  $receiptPathA = Join-Path $Repo ($resp.receipt_path -replace '/', '\')
  $receiptPathB = [string]$resp.receipt_abs_path

  $foundA = $false
  $foundB = $false
  for($i=0; $i -lt 10; $i++){
    $foundA = Test-Path -LiteralPath $receiptPathA
    $foundB = Test-Path -LiteralPath $receiptPathB
    if($foundA -and $foundB){ break }
    Start-Sleep -Milliseconds 500
  }
  if(-not $foundA){ throw "receipt_path does not exist: $receiptPathA" }
  if(-not $foundB){ throw "receipt_abs_path does not exist: $receiptPathB" }
}
finally {
  if($server -and -not $server.HasExited){
    Stop-Process -Id $server.Id -Force
  }
  if(Test-Path -LiteralPath (Join-Path $Repo "receipts\evaluate")){
    Remove-Item -LiteralPath (Join-Path $Repo "receipts\evaluate") -Recurse -Force
  }
}

Write-Host "AION_EVALUATE_API_V1_VERIFY_OK"
