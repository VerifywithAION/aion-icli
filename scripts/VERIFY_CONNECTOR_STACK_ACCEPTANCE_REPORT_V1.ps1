$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Connector Stack Acceptance Report V1 verifier"

$reportPath = ".\reports\CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md"

if (-not (Test-Path -LiteralPath $reportPath)) {
  throw "Missing connector stack acceptance report"
}

$report = Get-Content -LiteralPath $reportPath -Raw

$required = @(
  "AION ICLI Connector Stack Acceptance Report V1",
  "60b01a4 Add SDK examples v1",
  "AION_ICLI_CONNECTOR_STACK_ACCEPTANCE_TEST_V1_PASS",
  "AION_ICLI_PUBLIC_REPO_HEAD_60B01A4_CONFIRMED",
  "AION_CONNECTOR_POLICY_V2_VERIFY_OK",
  "AION_SAFE_API_ADAPTER_DRY_RUN_V1_VERIFY_OK",
  "AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_VERIFY_OK",
  "AION_SDK_EXAMPLES_V1_VERIFY_OK",
  "Governance should be felt, not seen.",
  "LOCKED as Connector Stack Acceptance Report V1"
)

foreach ($r in $required) {
  if ($report -notlike "*$r*") {
    throw "Report missing required text: $r"
  }
}

$badExact = @(
  "private AION engine",
  "private AION systems",
  "proprietary AION internals",
  "private AION logic",
  "confidential control plane",
  "private orchestration",
  "reconstruction kit"
)

foreach ($b in $badExact) {
  if ($report -like "*$b*") {
    throw "Report contains forbidden public phrase: $b"
  }
}

Write-Host "AION_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1_VERIFY_OK"
