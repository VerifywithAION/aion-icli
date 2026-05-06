$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Governance Brain Integration Fix V1 verifier"

$required = @(
  "src\aion_cli_entry.py",
  "docs\GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.md"
)
foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) { throw "Missing required artifact: $p" }
}

$env:AION_FORCE_COLOR = "0"
$env:AION_NO_COLOR = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$script = @(
  "what do you know about this release?"
  "what is wired?"
  "what is missing?"
  "diagnostics on"
  "what do you know about this release?"
  "exit"
) -join "`n"

$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value ($script + "`n") -Encoding ASCII

try {
  $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String
}
finally {
  if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force }
}

$norm = $out -replace "`e\[[0-9;]*m", ""
$beforeDiag = ($norm -split "Diagnostics enabled\.",2)[0]

if ($beforeDiag -notmatch "v1\.0\.0-public-icli|public release") { throw "Release output missing release tag/signal" }
if ($beforeDiag -notmatch "dist/aion-icli-public-install-package-v1\.zip|package") { throw "Release output missing package artifact" }
if ($beforeDiag -notmatch "SHA256|8B99C3") { throw "Release output missing SHA evidence" }
if ($beforeDiag -notmatch "VERIFY_PUBLIC_INSTALL_PACKAGE_V1\.ps1|release") { throw "Release output missing verifier linkage" }

if ($beforeDiag -notmatch "Governance Brain Adapter V1") { throw "Wired output missing Governance Brain Adapter V1" }
if ($beforeDiag -match "live provider/LLM.*active") { throw "Missing output incorrectly claims live provider execution" }

$diag = ($norm -split "Diagnostics enabled\.",2)[1]
if ([string]::IsNullOrWhiteSpace($diag)) { throw "Missing diagnostics-on segment" }
if ($diag -notmatch "Governance brain used\s*>\s*true") { throw "Diagnostics did not show governance brain used true" }
if ($diag -notmatch "Artifacts consulted") { throw "Diagnostics missing artifacts consulted" }
if ($diag -notmatch "GITHUB_RELEASE_V1_DRAFT|PUBLIC_INSTALL_PACKAGE|public_install_package_v1\.manifest\.json") {
  throw "Diagnostics artifacts missing release evidence files"
}

if (-not (Test-Path -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json")) { throw "Receipt missing" }
$receipt = Get-Content -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json" -Raw | ConvertFrom-Json
if ($receipt.governance_brain_used -ne $true) { throw "Receipt governance_brain_used not true" }
if ($receipt.boundary -ne "LOCAL_ONLY") { throw "Boundary mismatch" }
if ($receipt.network -ne "NOT_USED") { throw "Network mismatch" }
if ($receipt.mutation -ne "NOT_PERFORMED") { throw "Mutation mismatch" }
if ($receipt.execution -ne "NOT_PERFORMED") { throw "Execution mismatch" }

Write-Host "AION_GOVERNANCE_BRAIN_INTEGRATION_FIX_V1_VERIFY_OK"
