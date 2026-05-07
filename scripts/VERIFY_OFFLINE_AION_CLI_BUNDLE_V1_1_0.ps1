$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$zipPath = Join-Path $Repo 'dist\aion-icli-offline-bundle-v1.1.0.zip'
$manifestPath = Join-Path $Repo 'packaging\offline-bundle-v1.1.0\offline_bundle_v1_1_0.manifest.json'
$reportPath = Join-Path $Repo 'reports\OFFLINE_AION_CLI_BUNDLE_V1_1_0_REPORT.md'

if(-not (Test-Path -LiteralPath $zipPath)){ throw "ZIP missing: $zipPath" }
if(-not (Test-Path -LiteralPath $manifestPath)){ throw "Manifest missing" }
if(-not (Test-Path -LiteralPath $reportPath)){ throw "Report missing" }

$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$report = Get-Content -LiteralPath $reportPath -Raw

$sha = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
if($manifest.sha256.ToLowerInvariant() -ne $sha){ throw 'Manifest SHA mismatch' }
if($report -notmatch [regex]::Escape($sha)){ throw 'Report SHA mismatch' }

$head = (git -C $Repo rev-parse --short HEAD).Trim()
if($manifest.source_head -ne $head){ throw "Manifest source_head mismatch: expected $head got $($manifest.source_head)" }

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
  $entries = @($zip.Entries | ForEach-Object { $_.FullName })
  $required = @(
    'src/aion_cli_entry.py',
    'docs/SENTINEL_CONSISTENCY_ENGINE_V1.md',
    'docs/SELF_REPAIR_PLANNER_V1.md',
    'docs/CONTRADICTION_ENGINE_V1.md',
    'docs/INTROSPECTION_GATE_V1.md',
    'docs/EVIDENCE_ENGINE_V1.md',
    'docs/LIVING_PROOF_GRAPH_V1.md',
    'docs/ARTIFACT_INSPECTION_RUNNER_V1.md',
    'docs/MEMORY_SCAR_ENGINE_V1.md',
    '.aion_public/sentinel/sentinel_state_v1.json',
    '.aion_public/evidence/evidence_index_v1.json',
    '.aion_public/proof_graph/proof_graph_latest_v1.json',
    '.aion_public/scars/scars_seed.jsonl'
  )
  foreach($r in $required){ if(-not ($entries -contains $r)){ throw "Missing required ZIP entry: $r" } }

  $forbiddenPatterns = @('/\\.git/','^\\.git/','receipts/local/','^\\.env$','/node_modules/','/__pycache__/','/\\.venv/','/venv/')
  foreach($e in $entries){
    foreach($pat in $forbiddenPatterns){ if($e -match $pat){ throw "Forbidden ZIP entry: $e" } }
  }
}
finally {
  $zip.Dispose()
}

Write-Host 'AION_OFFLINE_CLI_BUNDLE_V1_1_0_VERIFY_OK'
