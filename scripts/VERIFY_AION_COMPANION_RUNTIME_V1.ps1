param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

if (!(Test-Path .\src\aion_companion_runtime.py)) { throw "Missing companion runtime source" }
if (!(Test-Path .\scripts\RUN_AION_COMPANION_RUNTIME_V1_DEMO.ps1)) { throw "Missing companion demo runner" }
if (!(Test-Path .\docs\AION_COMPANION_RUNTIME_V1.md)) { throw "Missing companion runtime doc" }

python -m py_compile .\src\aion_companion_runtime.py
python -m py_compile .\src\aion_cli_entry.py

$prompts = @(
  "protect my trading agent overnight so it can make money without blowing up my account",
  "protect my house while I am away and make sure the robot does not do anything dangerous",
  "help me delegate grocery buying but keep it inside my rules",
  "protect my coding agent and help it ship without breaking production",
  "mirror what I am really trying to build"
)

foreach ($p in $prompts) {
  $out = & .\bin\aion.cmd $p | Out-String
  if ($out -notmatch "One question that matters") { throw "Missing companion question output for prompt: $p" }
  if ($out -notmatch "Safe next step") { throw "Missing companion safe next step output for prompt: $p" }
  if ($out -notmatch "LOCAL_ONLY") { throw "Missing LOCAL_ONLY posture for prompt: $p" }
  if ($out -notmatch "NOT_USED") { throw "Missing NOT_USED posture for prompt: $p" }
  if ($out -notmatch "NOT_PERFORMED") { throw "Missing NOT_PERFORMED posture for prompt: $p" }
}

$receiptDir = Join-Path $repo "receipts\companion"
if (!(Test-Path $receiptDir)) { throw "Companion receipt folder missing" }
$latest = Get-ChildItem -Path $receiptDir -File | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1
if (-not $latest) { throw "No companion receipts found" }
$receipt = Get-Content -Raw -Path $latest.FullName | ConvertFrom-Json
if ($receipt.result.engine -ne "AION_COMPANION_RUNTIME_V1") { throw "Companion engine mismatch in receipt" }
if (-not (Test-Path $latest.FullName)) { throw "Companion latest receipt missing" }
if ([string]::IsNullOrWhiteSpace($receipt.result.human_response)) { throw "Companion human_response missing in receipt" }

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_COMPANION_RUNTIME_V1_DEMO.ps1 | Out-Null
if (!(Test-Path .\release\AION_COMPANION_RUNTIME_V1_DEMO_RESULT.json)) { throw "Missing companion demo result JSON" }
if (!(Test-Path .\reports\AION_COMPANION_RUNTIME_V1_DEMO_REPORT.md)) { throw "Missing companion demo report" }

Write-Host "AION_COMPANION_RUNTIME_V1_VERIFY_OK"
