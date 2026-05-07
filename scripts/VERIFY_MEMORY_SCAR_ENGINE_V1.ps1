$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Memory Scar Engine V1 verifier"

$required = @(
  ".aion_public/scars/scars_seed.jsonl",
  ".aion_public/graph/proof_graph_seed.json",
  ".aion_public/evolution/evolution_ledger_seed.jsonl",
  "docs/MEMORY_SCAR_ENGINE_V1.md",
  "src/aion_cli_entry.py"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing required artifact: $p" } }

$scarLines = Get-Content .aion_public/scars/scars_seed.jsonl
if($scarLines.Count -lt 5){ throw "Insufficient scar seeds" }
$scarText = $scarLines -join "`n"
$needed = @(
  'verifier_self_scan_false_positive',
  'zip_missing_user_guide',
  'diagnostics_governance_brain_bypass',
  'classifier_voice_leak',
  'adaptive_layer_under_specified_answer'
)
foreach($n in $needed){ if($scarText -notmatch [regex]::Escape($n)){ throw "Missing scar id: $n" } }

$env:AION_FORCE_COLOR='0'
$env:AION_NO_COLOR='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'

$script = @(
  'why are you asking for the artifact?'
  'why do you need proof?'
  'what have you learned?'
  'what mistakes do you remember?'
  'how do you learn?'
  'diagnostics on'
  'why are you asking for the artifact?'
  'diagnostics off'
  'exit'
) -join "`n"

$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value ($script + "`n") -Encoding ASCII
try { $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String }
finally { if(Test-Path $tmp){ Remove-Item $tmp -Force } }

$norm = $out -replace "`e\[[0-9;]*m", ""
$beforeDiag = ($norm -split "Diagnostics enabled\.",2)[0]

if($beforeDiag -notmatch 'scar'){ throw 'Normal output missing scar context' }
if($beforeDiag -notmatch 'artifact|evidence'){ throw 'Normal output missing artifact/evidence language' }
if($beforeDiag -notmatch 'no artifact, no judgment|no verifier, no lock|false confidence'){ throw 'Normal output missing future rule language' }
if($beforeDiag -notmatch 'Proof:\s*local-only'){ throw 'Missing proof footer' }

$diag = ($norm -split 'Diagnostics enabled\.',2)[1]
if([string]::IsNullOrWhiteSpace($diag)){ throw 'Missing diagnostics segment' }
if($diag -notmatch 'Memory scar engine used'){ throw 'Diagnostics missing memory scar engine field' }
if($diag -notmatch 'Scars consulted'){ throw 'Diagnostics missing scars consulted' }
if($diag -notmatch 'Future rule'){ throw 'Diagnostics missing future rule' }

if(-not (Test-Path .\receipts\local\aion_cli_receipt_v1.json)){ throw 'Receipt missing' }
$r = Get-Content .\receipts\local\aion_cli_receipt_v1.json -Raw | ConvertFrom-Json
if($r.memory_scar_engine_used -ne $true){ throw 'Receipt memory_scar_engine_used not true' }
if(-not $r.scars_consulted -or $r.scars_consulted.Count -eq 0){ throw 'Receipt scars_consulted empty' }
if($r.boundary -ne 'LOCAL_ONLY'){ throw 'Boundary mismatch' }
if($r.network -ne 'NOT_USED'){ throw 'Network mismatch' }
if($r.mutation -ne 'NOT_PERFORMED'){ throw 'Mutation mismatch' }
if($r.execution -ne 'NOT_PERFORMED'){ throw 'Execution mismatch' }

Write-Host 'AION_MEMORY_SCAR_ENGINE_V1_VERIFY_OK'
