param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$src = Join-Path $Repo "src\aion_demo_orchestrator.py"

$raw = & $Py $src run
$result = $raw | ConvertFrom-Json

$resultPath = Join-Path $Repo "release\AION_DEMO_ORCHESTRATOR_V1_RESULT.json"
$reportPath = Join-Path $Repo "reports\AION_DEMO_ORCHESTRATOR_V1_REPORT.md"

if (!(Test-Path $resultPath)) { throw "Missing $resultPath" }
if (!(Test-Path $reportPath)) { throw "Missing $reportPath" }

$steps = @{}
foreach($s in $result.steps){ $steps[$s.step] = $s }

Write-Host "AION DEMO ORCHESTRATOR V1"
Write-Host "Preflight: $($steps['preflight'].actual)"
Write-Host "Memory: $($steps['memory'].actual)"
Write-Host "Sentinel: $($steps['sentinel'].actual)"
Write-Host "Self-Repair: $($steps['self_repair'].actual)"
Write-Host "Sandbox: $($steps['sandbox'].actual)"
Write-Host "Domain Governor: $($steps['domain_governor'].actual)"
Write-Host "Intuition: $($steps['intuition'].actual)"
Write-Host "Introspection: $($steps['introspection'].actual)"
Write-Host "Final: $($result.final_demo_verdict)"
Write-Host "AION_DEMO_ORCHESTRATOR_V1_OK"
