param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_self_repair_planner.py"
if (!(Test-Path $Src)) { throw "Missing source" }
& $Py -m py_compile $Src

$tempDir = Join-Path $Repo "release\_runtime\self_repair_verify"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name, [hashtable]$Payload)
  $path = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $path -Encoding UTF8
  $raw = & $Py $Src --input $path
  return ($raw | ConvertFrom-Json)
}

$a = Invoke-Case -Name "missing_controls" -Payload @{
  source = "PreflightGate"
  problem_type = "missing_controls"
  governance_decision = "BLOCK"
  risk_level = "HIGH"
  missing_controls = @("verifier","rollback","dry_run")
  contradictions = @()
  missing_artifacts = @()
  context = "preflight missing controls"
}
$b = Invoke-Case -Name "contradiction" -Payload @{
  source = "Sentinel"
  problem_type = "contradiction"
  governance_decision = "BLOCK"
  risk_level = "HIGH"
  missing_controls = @()
  contradictions = @("ready_to_ship_without_verifier")
  missing_artifacts = @()
  context = "contradiction"
}
$c = Invoke-Case -Name "proof" -Payload @{
  source = "Introspection"
  problem_type = "missing_proof_surface"
  governance_decision = "REVIEW_ONLY"
  risk_level = "MEDIUM"
  missing_controls = @()
  contradictions = @()
  missing_artifacts = @("docs/AION_EXAMPLE.md","scripts/VERIFY_AION_EXAMPLE.ps1")
  context = "missing proof"
}

foreach($r in @($a,$b,$c)){
  if($r.planner -ne "AION_SELF_REPAIR_PLANNER_V1"){ throw "planner mismatch" }
  if($r.repair_status -ne "PLAN_ONLY"){ throw "repair_status mismatch" }
  if($r.forbidden_actions -notcontains "do_not_execute_target_action"){ throw "forbidden missing" }
  if($r.mutation -ne "NOT_PERFORMED_ON_TARGET"){ throw "mutation mismatch" }
  if($r.execution -ne "NOT_PERFORMED"){ throw "execution mismatch" }
  if([string]::IsNullOrWhiteSpace($r.receipt_path)){ throw "receipt_path missing" }
  if([string]::IsNullOrWhiteSpace($r.receipt_abs_path)){ throw "receipt_abs_path missing" }
  if($r.receipt_written -ne $true){ throw "receipt_written false" }
  if([string]::IsNullOrWhiteSpace($r.receipt_sha256)){ throw "receipt sha missing" }
  if(!(Test-Path (Join-Path $Repo $r.receipt_path))){ throw "receipt_path not found" }
  if(!(Test-Path $r.receipt_abs_path)){ throw "receipt_abs not found" }
}

$titlesA = @($a.repair_plan | ForEach-Object { $_.title.ToLower() }) -join " | "
if($titlesA -notmatch "verifier"){ throw "missing_controls case missing verifier step" }
if($titlesA -notmatch "rollback"){ throw "missing_controls case missing rollback step" }
if($titlesA -notmatch "dry-run"){ throw "missing_controls case missing dry-run step" }

$titlesB = @($b.repair_plan | ForEach-Object { $_.title.ToLower() + ' ' + $_.rationale.ToLower() }) -join " | "
if($titlesB -notmatch "downgrade|evidence"){ throw "contradiction case missing downgrade/evidence step" }

$dir = Join-Path $Repo "receipts\self_repair"
if(Test-Path $dir){ Remove-Item -Path $dir -Recurse -Force -ErrorAction SilentlyContinue }

Write-Host "AION_SELF_REPAIR_PLANNER_V1_VERIFY_OK"
