$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Evidence Engine V1 verifier"

$env:AION_FORCE_COLOR='0'
$env:AION_NO_COLOR='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python -m py_compile .\src\aion_cli_entry.py

$null = python .\src\aion_cli_entry.py "evidence summary"

$required = @(
  ".aion_public/evidence/evidence_index_v1.json",
  ".aion_public/evidence/evidence_summary_v1.md",
  ".aion_public/evidence/evidence_latest_v1.json"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing evidence file: $p" } }

$idx = Get-Content .aion_public/evidence/evidence_index_v1.json -Raw | ConvertFrom-Json
$layers = @($idx.layers)
foreach($ln in @('Artifact Inspection Runner V1','Living Proof Graph V1','Memory Scar Engine V1','Roadmap Sync + End-to-End Wiring Verification V1')){
  if(-not ($layers | Where-Object { $_.layer_name -eq $ln })){ throw "Missing layer classification: $ln" }
}

$recent = @($layers | Where-Object { $_.layer_name -in @('Artifact Inspection Runner V1','Living Proof Graph V1','Memory Scar Engine V1') })
if(-not ($recent | Where-Object { $_.evidence_level -eq 'ROADMAP_WIRED' -or $_.evidence_level -eq 'ADMISSIBLE' })){ throw 'Recent completed layers are not ROADMAP_WIRED/ADMISSIBLE' }

$post = @($layers | Where-Object { $_.layer_name -in @('Artifact Inspection Runner V1','Living Proof Graph V1','Evidence Engine V1') })
if($post | Where-Object { $_.release_packaged -eq $true }){ throw 'Overclaimed RELEASE_PACKAGED for post-v1.0.0 features' }

$script = @(
  'evidence summary'
  'what evidence proves artifact inspection?'
  'is memory scar engine really locked?'
  'what claims are only documented?'
  'what is admissible right now?'
  'what evidence is weak?'
  'diagnostics on'
  'evidence summary'
  'diagnostics off'
  'exit'
) -join "`n"
$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value ($script + "`n") -Encoding ASCII
try { $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String }
finally { if(Test-Path $tmp){ Remove-Item $tmp -Force } }

$norm = $out -replace "`e\[[0-9;]*m", ""
$before = ($norm -split 'Diagnostics enabled\.',2)[0]
if($before -notmatch 'evidence'){ throw 'Missing evidence output' }
if($before -notmatch 'ROADMAP_WIRED|admissible'){ throw 'Missing roadmap/admissible output' }
if($before -notmatch 'Artifact Inspection Runner V1'){ throw 'Missing artifact inspection mention' }
if($before -notmatch 'Memory Scar Engine V1'){ throw 'Missing memory scar mention' }
if($before -notmatch 'Proof:\s*local-only'){ throw 'Missing proof footer' }

$diag = ($norm -split 'Diagnostics enabled\.',2)[1]
if($diag -notmatch 'Evidence engine used'){ throw 'Diagnostics missing evidence engine used' }
if($diag -notmatch 'Evidence items evaluated'){ throw 'Diagnostics missing items evaluated' }
if($diag -notmatch 'Highest level'){ throw 'Diagnostics missing highest level' }
if($diag -notmatch 'Weakest layers'){ throw 'Diagnostics missing weakest layers' }
if($diag -notmatch 'Evidence paths'){ throw 'Diagnostics missing evidence paths' }

if(-not (Test-Path .\receipts\local\aion_cli_receipt_v1.json)){ throw 'Receipt missing' }
$r = Get-Content .\receipts\local\aion_cli_receipt_v1.json -Raw | ConvertFrom-Json
if($r.evidence_engine_used -ne $true){ throw 'Receipt evidence_engine_used not true' }
if([int]$r.evidence_items_evaluated -le 0){ throw 'Receipt evidence_items_evaluated missing' }
if([string]::IsNullOrWhiteSpace([string]$r.evidence_index_path)){ throw 'Receipt evidence_index_path missing' }
if($r.boundary -ne 'LOCAL_ONLY'){ throw 'Boundary mismatch' }
if($r.network -ne 'NOT_USED'){ throw 'Network mismatch' }
if($r.mutation -ne 'NOT_PERFORMED'){ throw 'Mutation mismatch' }
if($r.execution -ne 'NOT_PERFORMED'){ throw 'Execution mismatch' }

Write-Host 'AION_EVIDENCE_ENGINE_V1_VERIFY_OK'
