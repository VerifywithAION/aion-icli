$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

foreach($req in @(".\src\aion_preflight_gate.py",".\src\aion_memory_scars.py")){
  if(-not (Test-Path -LiteralPath $req)){ throw "Missing required file: $req" }
}

python -m py_compile .\src\aion_preflight_gate.py
python -m py_compile .\src\aion_memory_scars.py

$demoDir = Join-Path $Repo "demo_memory"
if(-not (Test-Path -LiteralPath $demoDir)){ New-Item -ItemType Directory -Path $demoDir | Out-Null }
$scarPath = Join-Path $demoDir "verify_integration_scar.json"
$eventPath = Join-Path $demoDir "verify_integration_event.json"

$scar = @{
  scar_id = "integration_missing_verifier_exec"
  trigger = "agent wants to execute script without verifier"
  harm = "unsafe execution without verification guard"
  repair = "require verifier + dry-run before any execution request"
  future_rule = "BLOCK execution when verifier is missing"
  severity = "HIGH"
  tags = @("execution","verifier")
  public_safe = $true
}
$event = @{
  source = "PreflightGate"
  action_type = "script"
  target = "scripts/deploy.ps1"
  intent = "execute script directly"
  risk_signals = @("execution")
  controls = @{
    rollback = $true
    dry_run = $true
    verifier = $false
    receipt_expected = $true
    human_review = $false
  }
  boundary = "LOCAL_ONLY"
  requested_execution = $true
}
$scar | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $scarPath
$event | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $eventPath

$null = ((python .\src\aion_memory_scars.py add --input $scarPath) | Out-String) | ConvertFrom-Json
$preflight = ((python .\src\aion_preflight_gate.py --input $eventPath) | Out-String) | ConvertFrom-Json

if($preflight.governance_decision -ne "BLOCK"){ throw "Expected governance_decision BLOCK" }
if(-not $preflight.memory_influence){ throw "memory_influence missing" }
if($preflight.memory_influence.recommended_decision_bias -ne "BLOCK"){ throw "Expected memory influence BLOCK" }
if(@($preflight.memory_influence.matched_scars).Count -lt 1){ throw "Expected matched_scars >= 1" }
if($preflight.boundary -ne "LOCAL_ONLY"){ throw "boundary mismatch" }
if($preflight.network -ne "NOT_USED"){ throw "network mismatch" }
if($preflight.mutation -ne "NOT_PERFORMED"){ throw "mutation mismatch" }
if($preflight.execution -ne "NOT_PERFORMED"){ throw "execution mismatch" }
if(-not $preflight.receipt_path){ throw "receipt_path missing" }
if(-not $preflight.receipt_abs_path){ throw "receipt_abs_path missing" }
if($preflight.receipt_written -ne $true){ throw "receipt_written not true" }
if(-not $preflight.receipt_sha256){ throw "receipt_sha256 missing" }

$r1 = Join-Path $Repo ($preflight.receipt_path -replace '/', '\')
$r2 = [string]$preflight.receipt_abs_path
if(-not (Test-Path -LiteralPath $r1)){ throw "receipt_path file missing" }
if(-not (Test-Path -LiteralPath $r2)){ throw "receipt_abs_path file missing" }

if(Test-Path -LiteralPath (Join-Path $Repo "receipts\preflight")){ Remove-Item -LiteralPath (Join-Path $Repo "receipts\preflight") -Recurse -Force }
if(Test-Path -LiteralPath (Join-Path $Repo "receipts\memory")){ Remove-Item -LiteralPath (Join-Path $Repo "receipts\memory") -Recurse -Force }
if(Test-Path -LiteralPath (Join-Path $Repo "demo_memory")){ Remove-Item -LiteralPath (Join-Path $Repo "demo_memory") -Recurse -Force }

Write-Host "AION_PREFLIGHT_MEMORY_INTEGRATION_V1_VERIFY_OK"
