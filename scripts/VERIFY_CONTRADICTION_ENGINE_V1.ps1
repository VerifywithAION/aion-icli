$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Contradiction Engine V1 verifier"

$env:AION_FORCE_COLOR='0'
$env:AION_NO_COLOR='1'
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python -m py_compile .\src\aion_cli_entry.py
$null = python .\src\aion_cli_entry.py "contradiction summary"

$required = @(
  ".aion_public/contradictions/contradiction_index_v1.json",
  ".aion_public/contradictions/contradiction_summary_v1.md",
  ".aion_public/contradictions/contradiction_latest_v1.json"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing contradiction file: $p" } }

$idx = Get-Content .aion_public/contradictions/contradiction_index_v1.json -Raw | ConvertFrom-Json
$contr = @($idx.contradictions)

$stale = $contr | Where-Object { $_.type -eq 'release_package_stale_relative_to_main' }
if(-not $stale){ throw 'Missing stale package caveat contradiction' }
if(-not ($stale | Where-Object { $_.status -eq 'ACCEPTED_CAVEAT' })){ throw 'Stale package contradiction must be ACCEPTED_CAVEAT' }
if($contr | Where-Object { $_.severity -eq 'CRITICAL' }){ throw 'Unexpected CRITICAL contradiction in clean state' }

$script = @(
  'contradiction summary'
  'what contradicts?'
  'is the release stale?'
  'what needs repair?'
  'diagnostics on'
  'contradiction summary'
  'diagnostics off'
  'exit'
) -join "`n"
$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value ($script + "`n") -Encoding ASCII
try { $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String }
finally { if(Test-Path $tmp){ Remove-Item $tmp -Force } }

$norm = $out -replace "`e\[[0-9;]*m", ""
$before = ($norm -split 'Diagnostics enabled\.',2)[0]
if($before -notmatch 'contradiction'){ throw 'Normal output missing contradiction' }
if($before -notmatch 'stale|caveat|no critical contradiction'){ throw 'Normal output missing stale/caveat/no-critical framing' }
if($before -notmatch 'release|package'){ throw 'Normal output missing release/package context' }
if($before -notmatch 'Proof:\s*local-only'){ throw 'Normal output missing proof footer' }

$diag = ($norm -split 'Diagnostics enabled\.',2)[1]
foreach($k in @('Contradiction engine used','Contradictions found','Open contradictions','Accepted caveats','Highest severity')){
  if($diag -notmatch [regex]::Escape($k)){ throw "Diagnostics missing: $k" }
}

if(-not (Test-Path .\receipts\local\aion_cli_receipt_v1.json)){ throw 'Receipt missing' }
$r = Get-Content .\receipts\local\aion_cli_receipt_v1.json -Raw | ConvertFrom-Json
if($r.contradiction_engine_used -ne $true){ throw 'Receipt contradiction_engine_used not true' }
if([int]$r.contradictions_found -lt 0){ throw 'Receipt contradictions_found missing' }
if([string]::IsNullOrWhiteSpace([string]$r.contradiction_index_path)){ throw 'Receipt contradiction_index_path missing' }
if($r.boundary -ne 'LOCAL_ONLY'){ throw 'Boundary mismatch' }
if($r.network -ne 'NOT_USED'){ throw 'Network mismatch' }
if($r.mutation -ne 'NOT_PERFORMED'){ throw 'Mutation mismatch' }
if($r.execution -ne 'NOT_PERFORMED'){ throw 'Execution mismatch' }

Write-Host 'AION_CONTRADICTION_ENGINE_V1_VERIFY_OK'
