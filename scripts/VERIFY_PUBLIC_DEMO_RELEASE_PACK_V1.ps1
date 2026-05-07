$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$zipPath = Join-Path $Repo 'dist\aion-public-demo-release-pack-v1.zip'
$manifestPath = Join-Path $Repo 'packaging\public-demo-release-pack-v1\public_demo_release_pack_v1.manifest.json'
$reportPath = Join-Path $Repo 'reports\PUBLIC_DEMO_RELEASE_PACK_V1_REPORT.md'
$extractPath = 'C:\Lab_Research\aion-public-demo-release-pack-v1-test'

if(-not (Test-Path -LiteralPath $zipPath)){ throw "Missing ZIP: $zipPath" }
if(-not (Test-Path -LiteralPath $manifestPath)){ throw "Missing manifest" }
if(-not (Test-Path -LiteralPath $reportPath)){ throw "Missing report" }

$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$report = Get-Content -LiteralPath $reportPath -Raw
$sha = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToUpperInvariant()
if($manifest.sha256 -ne $sha){ throw 'Manifest SHA mismatch' }
if($report -notmatch [regex]::Escape($sha)){ throw 'Report SHA mismatch' }

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
  $entries = @($zip.Entries | ForEach-Object { $_.FullName.Replace('/','\\') })
  $required = @(
    'README.md',
    'docs\AGENT_CLAIM_PROOF_GATE_DEMO_V1.md',
    'docs\PUBLIC_DEMO_README_SECTION_V1.md',
    'docs\PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1.md',
    'reports\PUBLIC_DEMO_PACKAGE_V1_REPORT.md',
    'reports\PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1_REPORT.md',
    'scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1',
    'scripts\VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1',
    'scripts\VERIFY_PUBLIC_DEMO_README_SECTION_V1.ps1',
    'scripts\VERIFY_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1.ps1',
    'src\aion_cli_entry.py',
    'install.ps1',
    'aion.ps1'
  )
  foreach($r in $required){ if(-not ($entries -contains $r)){ throw "Missing required ZIP entry: $r" } }

  $mustPrefix = @('demo\agent-claim-proof-gate\','bin\')
  foreach($prefix in $mustPrefix){
    if(-not ($entries | Where-Object { $_.StartsWith($prefix) })){ throw "Missing required ZIP folder content: $prefix" }
  }

  $forbiddenPatterns = @('^\.git\\','\\receipts\\local\\','^receipts\\local\\','\\node_modules\\','\\__pycache__\\','\\\.venv\\','\\venv\\','^\.env$','\\secrets\\','\\private\\')
  foreach($e in $entries){
    foreach($pat in $forbiddenPatterns){ if($e -match $pat){ throw "Forbidden ZIP entry: $e" } }
  }
}
finally {
  $zip.Dispose()
}

if(Test-Path -LiteralPath $extractPath){ Remove-Item -LiteralPath $extractPath -Recurse -Force }
Expand-Archive -LiteralPath $zipPath -DestinationPath $extractPath -Force

Push-Location $extractPath
try {
  $output = powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1 2>&1
  if($LASTEXITCODE -ne 0){ throw "Extracted demo verifier failed" }
  $joined = ($output -join "`n")
  if($joined -notmatch 'AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_VERIFY_OK'){ throw 'Missing demo verifier marker in extracted run' }
}
finally {
  Pop-Location
}

Write-Host 'AION_PUBLIC_DEMO_RELEASE_PACK_V1_VERIFY_OK'
