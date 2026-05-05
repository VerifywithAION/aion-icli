$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Repo Guided Tour V2 verifier"

$tourPath = ".\docs\REPO_GUIDED_TOUR_V1.md"
if (-not (Test-Path -LiteralPath $tourPath)) {
  throw "Missing repo guided tour"
}

$tour = Get-Content -LiteralPath $tourPath -Raw

$required = @(
  "[README](../README.md)",
  "[Public Boundary](PUBLIC_BOUNDARY.md)",
  "[Connector Policy V2](CONNECTOR_POLICY_V2.md)",
  "[Safe API Adapter Dry-Run V1](SAFE_API_ADAPTER_DRY_RUN_V1.md)",
  "[Safe Model Adapter Dry-Run V1](SAFE_MODEL_ADAPTER_DRY_RUN_V1.md)",
  "[SDK Examples V1](SDK_EXAMPLES_V1.md)",
  "[Connector Stack Acceptance Report V1](../reports/CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md)",
  "[Windows CMD launcher](../bin/aion.cmd)",
  "Can users clone and use AION ICLI now?",
  "Not included yet:",
  "standalone downloadable Windows .exe",
  "AION_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1_OK"
)

foreach ($r in $required) {
  if (-not $tour.Contains($r)) {
    throw "Repo guided tour missing required text: $r"
  }
}

Write-Host "AION_REPO_GUIDED_TOUR_V2_VERIFY_OK"
