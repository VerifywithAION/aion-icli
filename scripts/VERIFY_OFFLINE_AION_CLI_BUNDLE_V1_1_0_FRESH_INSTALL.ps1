$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$zipPath = Join-Path $Repo 'dist\aion-icli-offline-bundle-v1.1.0.zip'
$testRoot = 'C:\Lab_Research\aion-icli-offline-bundle-v1.1.0-test'

if(Test-Path -LiteralPath $testRoot){ Remove-Item -LiteralPath $testRoot -Recurse -Force }
New-Item -ItemType Directory -Path $testRoot | Out-Null

Expand-Archive -LiteralPath $zipPath -DestinationPath $testRoot -Force

$extractRepo = $testRoot
if(Test-Path -LiteralPath (Join-Path $testRoot 'aion-icli')){ $extractRepo = Join-Path $testRoot 'aion-icli' }

$installScript = Join-Path $extractRepo 'install.ps1'
if(-not (Test-Path -LiteralPath $installScript)){ throw 'install.ps1 missing in extracted bundle' }

powershell -NoProfile -ExecutionPolicy Bypass -File $installScript
if($LASTEXITCODE -ne 0){ throw 'Extracted install.ps1 failed' }

$cmd = Join-Path $extractRepo 'bin\aion.cmd'
if(-not (Test-Path -LiteralPath $cmd)){ throw 'bin\aion.cmd missing in extracted bundle' }

$queries = @(
  'Who are you, AION?',
  'sentinel state',
  'evidence summary',
  'show proof graph',
  'repair plan'
)
foreach($q in $queries){
  $out = & $cmd $q | Out-String
  if(($out -notmatch 'Proof:') -and ($out -notmatch 'LOCAL_ONLY')){ throw "Missing proof/boundary output for query: $q" }
}

$verifiers = @(
  'VERIFY_SENTINEL_CONSISTENCY_ENGINE_V1.ps1',
  'VERIFY_SELF_REPAIR_PLANNER_V1.ps1',
  'VERIFY_CONTRADICTION_ENGINE_V1.ps1',
  'VERIFY_INTROSPECTION_GATE_V1.ps1',
  'VERIFY_EVIDENCE_ENGINE_V1.ps1',
  'VERIFY_LIVING_PROOF_GRAPH_V1.ps1',
  'VERIFY_ARTIFACT_INSPECTION_RUNNER_V1.ps1',
  'VERIFY_MEMORY_SCAR_ENGINE_V1.ps1',
  'VERIFY_PUBLIC_SAFE.ps1'
)
foreach($v in $verifiers){
  $vp = Join-Path $extractRepo ("scripts\" + $v)
  if(-not (Test-Path -LiteralPath $vp)){ throw "Missing extracted verifier: $v" }
  powershell -NoProfile -ExecutionPolicy Bypass -File $vp
  if($LASTEXITCODE -ne 0){ throw "Extracted verifier failed: $v" }
}

$receiptLocal = Join-Path $extractRepo 'receipts\local'
if(Test-Path -LiteralPath $receiptLocal){ Remove-Item -LiteralPath $receiptLocal -Recurse -Force }

Write-Host 'AION_OFFLINE_CLI_BUNDLE_V1_1_0_FRESH_INSTALL_VERIFY_OK'
