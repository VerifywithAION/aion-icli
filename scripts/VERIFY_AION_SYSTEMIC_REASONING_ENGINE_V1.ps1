param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

if (!(Test-Path .\src\aion_systemic_reasoning_engine.py)) { throw "Missing systemic reasoning source" }
$tmp1 = Join-Path $env:TEMP "aion_systemic_reasoning_engine_v2.pyc"
$tmp2 = Join-Path $env:TEMP "aion_evaluate_api_v2.pyc"
python -c "import py_compile; py_compile.compile(r'.\\src\\aion_systemic_reasoning_engine.py', cfile=r'$tmp1', doraise=True)"
if ($LASTEXITCODE -ne 0) { throw "py_compile failed for aion_systemic_reasoning_engine.py" }
python -c "import py_compile; py_compile.compile(r'.\\src\\aion_evaluate_api.py', cfile=r'$tmp2', doraise=True)"
if ($LASTEXITCODE -ne 0) { throw "py_compile failed for aion_evaluate_api.py" }

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1 | Out-Null
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_COMPANION_RUNTIME_V1.ps1 | Out-Null

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_BUZZSHIELD_SYSTEMIC_HUMA_DEMO_V1.ps1 | Out-Null
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_BUZZSHIELD_WASABI_SYSTEMIC_V2_DEMO.ps1 | Out-Null

if (!(Test-Path .\release\AION_BUZZSHIELD_SYSTEMIC_HUMA_RESULT_V2.json)) { throw "Missing huma demo result JSON" }
$result = Get-Content -Raw -Path .\release\AION_BUZZSHIELD_SYSTEMIC_HUMA_RESULT_V2.json | ConvertFrom-Json
$resp = $result.response

if ($resp.governance_decision -ne "BLOCK") { throw "Expected BLOCK governance decision" }
if ($resp.risk_level -ne "HIGH") { throw "Expected HIGH risk level" }

if (-not $resp.normalized_payload_summary) { throw "Missing normalized_payload_summary" }
if ($resp.normalized_payload_summary.source -ne "BuzzShield") { throw "Expected BuzzShield source normalization" }
if ($resp.normalized_payload_summary.score -ne 21) { throw "Expected normalized score 21" }
if ($resp.normalized_payload_summary.verdict -ne "FLAGGED") { throw "Expected normalized verdict FLAGGED" }

if (-not $resp.systemic_reasoning) { throw "Missing systemic_reasoning object" }
foreach ($field in @(
  "systemic_summary",
  "trust_boundary_collapse",
  "violated_invariant",
  "hidden_governance_assumption",
  "generalized_fragility_law",
  "adjacent_risk_domains",
  "autonomy_implication",
  "humanoid_implication",
  "non_obvious_insight",
  "next_governance_question"
)) {
  if (-not $resp.systemic_reasoning.$field) { throw "Missing systemic field: $field" }
}

if (-not $resp.receipt_written) { throw "receipt_written not true" }
if (-not (Test-Path $resp.receipt_abs_path)) { throw "receipt_abs_path missing" }
if ($resp.systemic_reasoning.systemic_summary -notmatch "state transition") { throw "Expected state-machine-specific systemic summary for Huma" }

if (!(Test-Path .\release\AION_BUZZSHIELD_WASABI_SYSTEMIC_RESULT_V2.json)) { throw "Missing wasabi demo result JSON" }
$w = Get-Content -Raw -Path .\release\AION_BUZZSHIELD_WASABI_SYSTEMIC_RESULT_V2.json | ConvertFrom-Json
$wr = $w.response
if ($wr.governance_decision -ne "BLOCK") { throw "Wasabi expected BLOCK governance decision" }
if ($wr.risk_level -ne "HIGH") { throw "Wasabi expected HIGH risk level" }
if (-not $wr.receipt_written) { throw "Wasabi receipt_written not true" }
if (-not (Test-Path $wr.receipt_abs_path)) { throw "Wasabi receipt_abs_path missing" }
if ($wr.systemic_reasoning.systemic_summary -notmatch "Single-admin|single-admin|single-EOA|upgrade") { throw "Expected admin-key/upgradeability-specific summary for Wasabi" }
if ($wr.systemic_reasoning.adjacent_risk_domains -notcontains "dao_governance") { throw "Expected exploit-class adjacent domains for Wasabi" }

Write-Host "AION_SYSTEMIC_REASONING_ENGINE_V2_VERIFY_OK"
