$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Voice Layer V1 verifier"

$required = @(
  "src\aion_cli_entry.py",
  "docs\VOICE_LAYER_V1.md"
)
foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) { throw "Missing required artifact: $p" }
}

$env:AION_FORCE_COLOR = "0"
$env:AION_NO_COLOR = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$script = @(
  "should I run this script?"
  "what feels wrong here?"
  "help me design this better"
  "what do you know about this release?"
  "can I connect an API?"
  "where is the proof?"
  "diagnostics on"
  "should I run this script?"
  "diagnostics off"
  "should I run this script?"
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

$normalized = $out -replace "`e\[[0-9;]*m", ""

# Default mode must hide machine routing.
if ($normalized -match "Capability\s*>|Boundary\s*>|Network\s*>|Mutation\s*>|Execution\s*>") {
  # allow diagnostics block later, so only validate first segment before diagnostics was enabled
  $beforeDiag = ($normalized -split "Diagnostics enabled\.",2)[0]
  if ($beforeDiag -match "Capability\s*>|Boundary\s*>|Network\s*>|Mutation\s*>|Execution\s*>") {
    throw "Default voice mode leaked diagnostics markers"
  }
}

if ($normalized -notmatch "Proof:\s*local-only") { throw "Missing proof footer in normal mode" }
if ($normalized -notmatch "no network") { throw "Missing no network proof text" }
if ($normalized -notmatch "no mutation") { throw "Missing no mutation proof text" }
if ($normalized -notmatch "no execution") { throw "Missing no execution proof text" }
if ($normalized -notmatch "receipt written") { throw "Missing receipt written proof text" }

# Diagnostics segment must show internal markers.
$diagSegment = ($normalized -split "Diagnostics enabled\.",2)[1]
if ([string]::IsNullOrWhiteSpace($diagSegment)) { throw "Diagnostics segment not found" }
if ($diagSegment -notmatch "Capability\s*>") { throw "Diagnostics mode missing Capability line" }
if ($diagSegment -notmatch "Boundary") { throw "Diagnostics mode missing Boundary line" }
if ($diagSegment -notmatch "Network") { throw "Diagnostics mode missing Network line" }
if ($diagSegment -notmatch "Mutation") { throw "Diagnostics mode missing Mutation line" }
if ($diagSegment -notmatch "Execution") { throw "Diagnostics mode missing Execution line" }
if ($diagSegment -notmatch "Receipt") { throw "Diagnostics mode missing Receipt line" }

# After diagnostics off, markers should hide again.
$afterDiagOff = ($normalized -split "Diagnostics disabled\.",2)[1]
if ([string]::IsNullOrWhiteSpace($afterDiagOff)) { throw "Missing diagnostics off segment" }
$afterPromptChunk = ($afterDiagOff -split "exit")[0]
if ($afterPromptChunk -match "Capability\s*>|Boundary\s*>|Network\s*>|Mutation\s*>|Execution\s*>") {
  throw "Diagnostics markers remained visible after diagnostics off"
}

if (-not (Test-Path -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json")) {
  throw "Receipt file missing"
}
$receipt = Get-Content -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json" -Raw | ConvertFrom-Json
if ($receipt.mode -ne "interactive") { throw "Receipt mode mismatch" }
if ($receipt.boundary -ne "LOCAL_ONLY") { throw "Receipt boundary mismatch" }
if ($receipt.network -ne "NOT_USED") { throw "Receipt network mismatch" }
if ($receipt.mutation -ne "NOT_PERFORMED") { throw "Receipt mutation mismatch" }
if ($receipt.execution -ne "NOT_PERFORMED") { throw "Receipt execution mismatch" }

Write-Host "AION_VOICE_LAYER_V1_VERIFY_OK"
