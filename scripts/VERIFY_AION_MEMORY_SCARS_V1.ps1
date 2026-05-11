$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$src = ".\src\aion_memory_scars.py"
if(-not (Test-Path -LiteralPath $src)){ throw "Missing $src" }
python -m py_compile $src
if($LASTEXITCODE -ne 0){ throw "Python compile failed for $src" }

$demoDir = Join-Path $Repo "demo_memory"
if(-not (Test-Path -LiteralPath $demoDir)){ New-Item -ItemType Directory -Path $demoDir | Out-Null }
$scarPath = Join-Path $demoDir "verify_scar.json"
$eventPath = Join-Path $demoDir "verify_event.json"

$scar = @{
  scar_id = "verify_missing_verifier_exec"
  trigger = "agent wants to execute script without verifier"
  harm = "unsafe execution without control"
  repair = "require verifier gate and dry-run"
  future_rule = "BLOCK when verifier missing for execution"
  severity = "HIGH"
  tags = @("execution","verifier")
  public_safe = $true
}
$event = @{
  source = "PreflightGate"
  action_type = "script"
  risk_signals = @("execution")
  missing_controls = @("verifier")
  summary = "Agent wants to execute script without verifier"
}
$scar | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $scarPath
$event | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $eventPath

$add = ((python .\src\aion_memory_scars.py add --input $scarPath) | Out-String) | ConvertFrom-Json
$eval = ((python .\src\aion_memory_scars.py evaluate --input $eventPath) | Out-String) | ConvertFrom-Json

$storePath = Join-Path $Repo ".aion_public\memory\memory_scars_v1.jsonl"
if(-not (Test-Path -LiteralPath $storePath)){ throw "Memory store missing: $storePath" }
if(@($eval.matched_scars).Count -lt 1){ throw "Expected matched scars >= 1" }
if($eval.recommended_decision_bias -ne "BLOCK"){ throw "Expected recommended_decision_bias BLOCK" }
if(-not $eval.receipt_path){ throw "receipt_path missing" }
if(-not $eval.receipt_abs_path){ throw "receipt_abs_path missing" }
if($eval.receipt_written -ne $true){ throw "receipt_written not true" }
if(-not $eval.receipt_sha256){ throw "receipt_sha256 missing" }

$receiptA = Join-Path $Repo ($eval.receipt_path -replace '/', '\')
$receiptB = [string]$eval.receipt_abs_path
if(-not (Test-Path -LiteralPath $receiptA)){ throw "receipt_path file missing" }
if(-not (Test-Path -LiteralPath $receiptB)){ throw "receipt_abs_path file missing" }

if(Test-Path -LiteralPath (Join-Path $Repo "receipts\memory")){
  Remove-Item -LiteralPath (Join-Path $Repo "receipts\memory") -Recurse -Force
}

Write-Host "AION_MEMORY_SCARS_V1_VERIFY_OK"
