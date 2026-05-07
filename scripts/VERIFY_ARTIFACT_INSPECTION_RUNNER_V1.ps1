$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Artifact Inspection Runner V1 verifier"

$required = @(
  "src/aion_cli_entry.py",
  "docs/ARTIFACT_INSPECTION_RUNNER_V1.md",
  "examples/inspection/fixture_safe_script.ps1",
  "examples/inspection/fixture_risky_script.ps1"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing required artifact: $p" } }

$env:AION_FORCE_COLOR='0'
$env:AION_NO_COLOR='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'

$script = @(
  'should I run examples\inspection\fixture_safe_script.ps1?'
  'should I run examples\inspection\fixture_risky_script.ps1?'
  'should I run this script now?'
  'inspect docs\USER_GUIDE_V1.md'
  'diagnostics on'
  'should I run examples\inspection\fixture_risky_script.ps1?'
  'diagnostics off'
  'exit'
) -join "`n"

$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value ($script + "`n") -Encoding ASCII
try { $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String }
finally { if(Test-Path $tmp){ Remove-Item $tmp -Force } }

$norm = $out -replace "`e\[[0-9;]*m", ""
$beforeDiag = ($norm -split "Diagnostics enabled\.",2)[0]

if($beforeDiag -notmatch 'inspected'){ throw 'Safe fixture output missing inspected' }
if($beforeDiag -notmatch 'Decision|risk'){ throw 'Safe fixture output missing decision/risk' }
if($beforeDiag -notmatch 'Proof:\s*local-only'){ throw 'Proof footer missing in normal mode' }

if($beforeDiag -notmatch 'REVIEW_ONLY|BLOCK_EXECUTION|HIGH|MEDIUM'){ throw 'Risky fixture did not escalate' }
if($beforeDiag -notmatch 'network|mutation|execution'){ throw 'Risky fixture missing pattern families' }
if($beforeDiag -notmatch 'rollback|dry-run|verifier'){ throw 'Risky fixture missing control guidance' }

if($beforeDiag -notmatch 'script path|artifact|cannot inspect what I cannot see|no artifact, no judgment'){ throw 'Missing-path response missing guidance' }
if($beforeDiag -notmatch 'docs\\USER_GUIDE_V1.md'){ throw 'Doc inspection missing target path' }
if($beforeDiag -notmatch 'LOW|SAFE_TO_READ|REVIEW_ONLY'){ throw 'Doc inspection missing low/review decision' }

$diag = ($norm -split 'Diagnostics enabled\.',2)[1]
if([string]::IsNullOrWhiteSpace($diag)){ throw 'Missing diagnostics segment' }
if($diag -notmatch 'Artifact inspection used'){ throw 'Diagnostics missing artifact inspection used' }
if($diag -notmatch 'Artifact path'){ throw 'Diagnostics missing artifact path' }
if($diag -notmatch 'Risk level'){ throw 'Diagnostics missing risk level' }
if($diag -notmatch 'Detected patterns'){ throw 'Diagnostics missing detected patterns' }
if($diag -notmatch 'Missing controls'){ throw 'Diagnostics missing missing controls' }

if(-not (Test-Path .\receipts\local\aion_cli_receipt_v1.json)){ throw 'Receipt missing' }
$r = Get-Content .\receipts\local\aion_cli_receipt_v1.json -Raw | ConvertFrom-Json
if($r.artifact_inspection_used -ne $true){ throw 'Receipt artifact_inspection_used not true' }
if([string]::IsNullOrWhiteSpace([string]$r.artifact_path)){ throw 'Receipt artifact_path missing' }
if([string]::IsNullOrWhiteSpace([string]$r.decision)){ throw 'Receipt decision missing' }
if([string]::IsNullOrWhiteSpace([string]$r.risk_level)){ throw 'Receipt risk_level missing' }
if($r.boundary -ne 'LOCAL_ONLY'){ throw 'Boundary mismatch' }
if($r.network -ne 'NOT_USED'){ throw 'Network mismatch' }
if($r.mutation -ne 'NOT_PERFORMED'){ throw 'Mutation mismatch' }
if($r.execution -ne 'NOT_PERFORMED'){ throw 'Execution mismatch' }

Write-Host 'AION_ARTIFACT_INSPECTION_RUNNER_V1_VERIFY_OK'
