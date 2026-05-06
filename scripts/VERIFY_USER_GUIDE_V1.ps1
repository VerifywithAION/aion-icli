$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI User Guide V1 verifier"

$guidePath = ".\docs\USER_GUIDE_V1.md"

if (-not (Test-Path -LiteralPath $guidePath)) {
  throw "Missing user guide"
}

$guide = Get-Content -LiteralPath $guidePath -Raw

$required = @(
  "AION ICLI User Guide V1",
  "Interactive Command Line Intelligence",
  "governed execution surface",
  "Governance should be felt, not seen.",
  "Boundary > LOCAL_ONLY",
  "Network  > NOT_USED",
  "Mutation > NOT_PERFORMED",
  "AION_ICLI_PUBLIC_SAFE_VERIFY_OK",
  "AION_CONNECTOR_POLICY_V2_VERIFY_OK",
  "AION_SAFE_API_ADAPTER_DRY_RUN_V1_VERIFY_OK",
  "AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_VERIFY_OK",
  "AION_SDK_EXAMPLES_V1_VERIFY_OK",
  "AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK",
  "API request envelopes",
  "model request envelopes",
  "SDK-style request JSON",
  "receipts\local\aion_cli_receipt_v1.json",
  "LOCKED as AION ICLI User Guide V1"
)

foreach ($r in $required) {
  if (-not $guide.Contains($r)) {
    throw "User guide missing required text: $r"
  }
}

Write-Host "AION_USER_GUIDE_V1_VERIFY_OK"
