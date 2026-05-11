param()
$ErrorActionPreference = "Stop"

$repo = "C:\Lab_Research\aion-live-demo"
$doc = Join-Path $repo "docs\AION_PUBLIC_DEMO_RECORDING_PACK_V1.md"
$run = Join-Path $repo "scripts\RUN_AION_PUBLIC_DEMO_RECORDING_V1.ps1"

if (!(Test-Path $doc)) { throw "Missing doc: $doc" }
if (!(Test-Path $run)) { throw "Missing run script: $run" }

& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo "scripts\VERIFY_AION_DEMO_ORCHESTRATOR_V1.ps1")

$output = & powershell -NoProfile -ExecutionPolicy Bypass -File $run | Out-String
if ($output -notmatch "AION_DEMO_ORCHESTRATOR_V1_OK") { throw "Missing orchestrator marker in recording output" }
if ($output -notmatch "AION_PUBLIC_DEMO_RECORDING_V1_READY") { throw "Missing recording ready marker" }

Write-Host "AION_PUBLIC_DEMO_RECORDING_PACK_V1_VERIFY_OK"
