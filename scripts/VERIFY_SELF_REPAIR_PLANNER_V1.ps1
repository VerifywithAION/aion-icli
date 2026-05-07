$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Self-Repair Planner V1 verifier"

$env:AION_FORCE_COLOR='0'
$env:AION_NO_COLOR='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python -m py_compile .\src\aion_cli_entry.py
$null = python .\src\aion_cli_entry.py "repair plan"

$required = @(
  ".aion_public/self_repair/self_repair_plan_v1.json",
  ".aion_public/self_repair/self_repair_summary_v1.md",
  ".aion_public/self_repair/self_repair_latest_v1.json"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing self-repair file: $p" } }

$plan = Get-Content .aion_public/self_repair/self_repair_plan_v1.json -Raw | ConvertFrom-Json
$items = @($plan.repair_items)
$stale = $items | Where-Object { $_.repair_id -eq 'rebuild_public_offline_bundle_v1_1_0' }
if(-not $stale){ throw 'Missing stale package repair item' }
foreach($k in @('recommended_steps','forbidden_steps','verification_steps','rollback_notes','expected_marker')){
  if($null -eq $stale[0].$k){ throw "Stale repair missing field: $k" }
}

$script = @(
  'repair plan'
  'what should we repair next?'
  'how do we fix the stale package?'
  'what is the safest repair plan?'
  'diagnostics on'
  'repair plan'
  'diagnostics off'
  'exit'
) -join "`n"
$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value ($script + "`n") -Encoding ASCII
try { $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String }
finally { if(Test-Path $tmp){ Remove-Item $tmp -Force } }

$norm = $out -replace "`e\[[0-9;]*m", ""
$before = ($norm -split 'Diagnostics enabled\.',2)[0]
if($before -notmatch 'repair'){ throw 'Missing repair output' }
if($before -notmatch 'v1\.1\.0|offline bundle|stale package'){ throw 'Missing stale package/offline bundle context' }
if($before -notmatch 'do not overwrite v1\.0\.0'){ throw 'Missing do-not-overwrite guard' }
if($before -notmatch 'verifier|fresh ZIP'){ throw 'Missing verifier/fresh ZIP step' }
if($before -notmatch 'Proof:\s*local-only'){ throw 'Missing proof footer' }

$diag = ($norm -split 'Diagnostics enabled\.',2)[1]
foreach($k in @('Self-repair planner used','Repair items','Highest severity','Ready for review','Plan path')){
  if($diag -notmatch [regex]::Escape($k)){ throw "Diagnostics missing: $k" }
}

if(-not (Test-Path .\receipts\local\aion_cli_receipt_v1.json)){ throw 'Receipt missing' }
$r = Get-Content .\receipts\local\aion_cli_receipt_v1.json -Raw | ConvertFrom-Json
if($r.self_repair_planner_used -ne $true){ throw 'Receipt self_repair_planner_used not true' }
if([int]$r.repair_items -lt 0){ throw 'Receipt repair_items missing' }
if([string]::IsNullOrWhiteSpace([string]$r.repair_plan_path)){ throw 'Receipt repair_plan_path missing' }
if($r.boundary -ne 'LOCAL_ONLY'){ throw 'Boundary mismatch' }
if($r.network -ne 'NOT_USED'){ throw 'Network mismatch' }
if($r.mutation -ne 'NOT_PERFORMED'){ throw 'Mutation mismatch' }
if($r.execution -ne 'NOT_PERFORMED'){ throw 'Execution mismatch' }

Write-Host 'AION_SELF_REPAIR_PLANNER_V1_VERIFY_OK'
