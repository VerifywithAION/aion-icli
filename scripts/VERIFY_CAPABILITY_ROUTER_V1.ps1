$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Capability Router V1 verifier"

$required = @(
  "src\aion_cli_entry.py",
  "docs\CAPABILITY_ROUTER_V1.md",
  "scripts\VERIFY_INTERACTIVE_MODE_V1.ps1"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing capability router artifact: $p"
  }
}

$source = Get-Content -LiteralPath ".\src\aion_cli_entry.py" -Raw
$doc = Get-Content -LiteralPath ".\docs\CAPABILITY_ROUTER_V1.md" -Raw

$requiredSource = @(
  "CAPABILITY_MAP",
  "detect_capability",
  "preflight_response",
  "creative_response",
  "intuition_response",
  "cortex_response",
  "connectors_response",
  "receipts_response",
  "verify_response",
  "next_response",
  "Capability Router V1"
)

foreach ($r in $requiredSource) {
  if (-not $source.Contains($r)) {
    throw "CLI source missing router text: $r"
  }
}

$requiredDoc = @(
  "AION ICLI Capability Router V1",
  "preflight",
  "creative",
  "intuition",
  "cortex",
  "connectors",
  "receipts",
  "AION_CAPABILITY_ROUTER_V1_VERIFY_OK"
)

foreach ($r in $requiredDoc) {
  if (-not $doc.Contains($r)) {
    throw "Capability Router doc missing required text: $r"
  }
}

$env:AION_FORCE_COLOR = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$script = "capabilities`npreflight review this action`ncreative design a safer flow`nintuition what feels wrong`ncortex release state`nconnectors api sdk model`nreceipts`nverify`nnext`nexit`n"
$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value $script -Encoding ASCII

try {
  $out = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String
}
finally {
  if (Test-Path -LiteralPath $tmp) {
    Remove-Item -LiteralPath $tmp -Force
  }
}

$mustOutput = @(
  "Capability Router V1",
  "Available public-safe capabilities",
  "Preflight review started",
  "Creative mode started",
  "Intuition mode started",
  "Cortex mode started",
  "Connector mode started",
  "Receipt mode started",
  "Verification mode started",
  "Recommended next build",
  "Capability > PREFLIGHT",
  "Capability > CREATIVE",
  "Capability > INTUITION",
  "Capability > CORTEX",
  "Capability > CONNECTORS",
  "Capability > RECEIPTS",
  "Capability > VERIFY",
  "Capability > NEXT"
)

foreach ($m in $mustOutput) {
  if ($out -notlike "*$m*") {
    Write-Host $out
    throw "Capability Router output missing: $m"
  }
}

if (-not (Test-Path -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json")) {
  throw "Capability Router did not write receipt"
}

$receipt = Get-Content -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json" -Raw | ConvertFrom-Json
if ($receipt.mode -ne "interactive") { throw "Receipt mode mismatch" }
if ($receipt.boundary -ne "LOCAL_ONLY") { throw "Receipt boundary mismatch" }
if ($receipt.network -ne "NOT_USED") { throw "Receipt network mismatch" }
if ($receipt.mutation -ne "NOT_PERFORMED") { throw "Receipt mutation mismatch" }
if ($receipt.execution -ne "NOT_PERFORMED") { throw "Receipt execution mismatch" }

Write-Host "AION_CAPABILITY_ROUTER_V1_VERIFY_OK"
