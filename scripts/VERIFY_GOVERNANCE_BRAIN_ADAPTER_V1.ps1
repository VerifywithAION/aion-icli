$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Governance Brain Adapter V1 verifier"

$required = @(
  "src\aion_cli_entry.py",
  "docs\GOVERNANCE_BRAIN_ADAPTER_V1.md"
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
  "what can you verify?"
  "how do connectors work?"
  "where is the proof?"
  "what is wired?"
  "what is missing?"
  "diagnostics on"
  "what do you know about this release?"
  "diagnostics off"
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

if ($beforeDiag -match "Capability\s*>|Subject\s*>|Urgency\s*>|Risk lens|Governance brain used|Artifacts consulted") {
  throw "Normal mode leaked diagnostics internals"
}

if ($beforeDiag -notmatch "v1\.0\.0-public-icli|public release") { throw "Release answer missing tag/release evidence" }
if ($beforeDiag -notmatch "dist/aion-icli-public-install-package-v1\.zip|package") { throw "Release answer missing package evidence" }
if ($beforeDiag -notmatch "SHA256|8B99C3") { throw "Release answer missing SHA evidence" }
if ($beforeDiag -notmatch "VERIFY_PUBLIC_INSTALL_PACKAGE_V1\.ps1|release") { throw "Release answer missing verifier linkage" }

if ($beforeDiag -notmatch "VERIFY_.*\.ps1") {
  throw "Verifier answer missing discovered VERIFY_*.ps1 scripts"
}

if ($beforeDiag -notmatch "connector|policy|schema|envelope|no live") {
  throw "Connector answer missing governed connector language"
}

if ($beforeDiag -notmatch "aion_cli_receipt_v1\.json") {
  throw "Proof answer missing receipt path"
}
if ($beforeDiag -notmatch "verifier|prove") {
  throw "Proof answer missing verifier/proof language"
}

if ($beforeDiag -notmatch "Interactive Mode V1|Capability Router V1|Voice Layer V1|Adaptive Reasoning Layer V1|Governance Brain Adapter V1|User Guide V1") {
  throw "Wired answer missing known wired layers"
}

if ($beforeDiag -notmatch "no live provider/LLM|no external API execution by default|no autonomous") {
  throw "Missing-state answer asserted unsafe capability"
}

$diagSegment = ($norm -split "Diagnostics enabled\.",2)[1]
if ([string]::IsNullOrWhiteSpace($diagSegment)) { throw "Missing diagnostics-on segment" }
if ($diagSegment -notmatch "Governance brain used\s*>\s*true") { throw "Diagnostics missing governance brain true" }
if ($diagSegment -notmatch "Artifacts consulted") { throw "Diagnostics missing artifacts consulted" }
if ($diagSegment -notmatch "GITHUB_RELEASE_V1_DRAFT|PUBLIC_INSTALL_PACKAGE|public_install_package_v1\.manifest\.json") {
  throw "Diagnostics artifacts missing release evidence files"
}

if (-not (Test-Path -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json")) {
  throw "Receipt file missing"
}
$receipt = Get-Content -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json" -Raw | ConvertFrom-Json
if ($receipt.boundary -ne "LOCAL_ONLY") { throw "Receipt boundary mismatch" }
if ($receipt.network -ne "NOT_USED") { throw "Receipt network mismatch" }
if ($receipt.mutation -ne "NOT_PERFORMED") { throw "Receipt mutation mismatch" }
if ($receipt.execution -ne "NOT_PERFORMED") { throw "Receipt execution mismatch" }
if ($receipt.governance_brain_used -ne $true) { throw "Receipt governance_brain_used should be true" }
if (-not ($receipt.PSObject.Properties.Name -contains "artifacts_consulted")) { throw "Receipt missing artifacts_consulted" }

Write-Host "AION_GOVERNANCE_BRAIN_ADAPTER_V1_VERIFY_OK"
