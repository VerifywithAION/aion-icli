param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-live-demo"
Set-Location $repo

$src = Join-Path $repo "src\aion_living_voice_adapter.py"
if (!(Test-Path $src)) { throw "Missing adapter source" }
python -m py_compile $src
python -m py_compile .\src\aion_cli_entry.py

& powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_LIVING_VOICE_ADAPTER_V1_DEMO.ps1 | Out-Null

$resultPath = Join-Path $repo "release\AION_LIVING_VOICE_ADAPTER_V1_DEMO_RESULT.json"
$reportPath = Join-Path $repo "reports\AION_LIVING_VOICE_ADAPTER_V1_DEMO_REPORT.md"
if (!(Test-Path $resultPath)) { throw "Missing demo result JSON" }
if (!(Test-Path $reportPath)) { throw "Missing demo report" }

$data = Get-Content -Raw -Path $resultPath | ConvertFrom-Json
if ($data.adapter -ne "AION_LIVING_VOICE_ADAPTER_V1") { throw "Adapter marker mismatch" }
if ($data.captures.Count -lt 5) { throw "Expected five demo captures" }

$all = ($data.captures | ForEach-Object { $_.output }) -join "`n"
if ($all -notmatch "Continuity note|continuity") { throw "Adaptive continuity framing not detected" }
if ($all -notmatch "cannot guarantee|uncertainty|partial") { throw "Truth-preserving bounded language not detected" }
if ($all -notmatch "govern") { throw "Governance-aware language not detected" }

$receiptPath = Join-Path $repo "receipts\local\aion_cli_receipt_v1.json"
if (!(Test-Path $receiptPath)) { throw "Missing receipt" }
$receipt = Get-Content -Raw -Path $receiptPath | ConvertFrom-Json
if ($receipt.boundary -ne "LOCAL_ONLY") { throw "Boundary must remain LOCAL_ONLY" }
if ($receipt.network -ne "NOT_USED") { throw "Network must remain NOT_USED" }
if ([string]::IsNullOrWhiteSpace($receipt.response)) { throw "Receipt response missing" }

Write-Host "AION_LIVING_VOICE_ADAPTER_V1_VERIFY_OK"
