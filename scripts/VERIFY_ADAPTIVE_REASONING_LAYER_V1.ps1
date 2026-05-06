$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Adaptive Reasoning Layer V1 verifier"

$required = @(
  "src\\aion_cli_entry.py",
  "docs\\ADAPTIVE_REASONING_LAYER_V1.md"
)
foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) { throw "Missing required artifact: $p" }
}

$env:AION_FORCE_COLOR = "0"
$env:AION_NO_COLOR = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$script = @(
  "should I run this script now?"
  "can I connect an API?"
  "what feels wrong here?"
  "help me design this better"
  "where is the proof?"
  "diagnostics on"
  "should I run this script now?"
  "diagnostics off"
  "should I run this script now?"
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
if ($beforeDiag -match "Capability\\s*>|Boundary\\s*>|Network\\s*>|Mutation\\s*>|Execution\\s*>") {
  throw "Normal mode exposed diagnostics markers before diagnostics on"
}

if ($norm -notmatch "Proof:\s*local-only") { throw "Missing proof footer in normal mode" }
if ($norm -notmatch "no network") { throw "Missing no network proof text" }
if ($norm -notmatch "no mutation") { throw "Missing no mutation proof text" }
if ($norm -notmatch "no execution") { throw "Missing no execution proof text" }
if ($norm -notmatch "receipt written") { throw "Missing receipt written proof text" }

if ($beforeDiag -notmatch "Don't run|Don.t run|not run") { throw "Script prompt did not refuse run" }
if ($beforeDiag -notmatch "now") { throw "Script prompt did not reflect urgency now" }
if ($beforeDiag -notmatch "script") { throw "Script prompt missing script subject" }
if ($beforeDiag -notmatch "blast radius|revers") { throw "Script prompt missing blast radius or reversibility signal" }

if ($beforeDiag -notmatch "endpoint|scope|auth|connector envelope") { throw "API prompt missing connector questions" }
if ($beforeDiag -notmatch "no live call|no live") { throw "API prompt missing no live call statement" }

if ($beforeDiag -notmatch "not visible|Show me|show me") { throw "Intuition prompt missing missing-artifact request" }
if ($beforeDiag -notmatch "hidden coupling|rollback|missing evidence") { throw "Intuition prompt missing risk families" }

if ($beforeDiag -notmatch "layer|design") { throw "Creative prompt missing layered design" }
if ($beforeDiag -notmatch "boundary|proof|rollback") { throw "Creative prompt missing boundary/proof/rollback" }

if ($beforeDiag -notmatch "aion_cli_receipt_v1\.json") { throw "Proof prompt missing receipt path" }
if ($beforeDiag -notmatch "verifier") { throw "Proof prompt missing verifier guidance" }

if ($norm -notmatch "Diagnostics enabled\.") { throw "Missing diagnostics enabled confirmation" }
if ($norm -notmatch "Capability\s*>") { throw "Diagnostics mode missing Capability line" }
if ($norm -notmatch "Subject") { throw "Diagnostics mode missing Subject line" }
if ($norm -notmatch "Urgency") { throw "Diagnostics mode missing Urgency line" }
if ($norm -notmatch "Missing evidence") { throw "Diagnostics mode missing Missing evidence line" }
if ($norm -notmatch "Risk lens") { throw "Diagnostics mode missing Risk lens line" }
if ($norm -notmatch "Boundary") { throw "Diagnostics mode missing Boundary line" }
if ($norm -notmatch "Network") { throw "Diagnostics mode missing Network line" }
if ($norm -notmatch "Mutation") { throw "Diagnostics mode missing Mutation line" }
if ($norm -notmatch "Execution") { throw "Diagnostics mode missing Execution line" }
if ($norm -notmatch "Receipt") { throw "Diagnostics mode missing Receipt line" }

$offIndex = $norm.IndexOf("Diagnostics disabled.")
if ($offIndex -lt 0) { throw "Missing diagnostics-off segment" }
$afterDiagOff = $norm.Substring($offIndex)
if ($afterDiagOff -notmatch "Proof:\s*local-only") { throw "Diagnostics off did not return to normal proof footer output" }

if (-not (Test-Path -LiteralPath ".\\receipts\\local\\aion_cli_receipt_v1.json")) {
  throw "Receipt file missing"
}
$receipt = Get-Content -LiteralPath ".\\receipts\\local\\aion_cli_receipt_v1.json" -Raw | ConvertFrom-Json
if ($receipt.mode -ne "interactive") { throw "Receipt mode mismatch" }
if ($receipt.boundary -ne "LOCAL_ONLY") { throw "Receipt boundary mismatch" }
if ($receipt.network -ne "NOT_USED") { throw "Receipt network mismatch" }
if ($receipt.mutation -ne "NOT_PERFORMED") { throw "Receipt mutation mismatch" }
if ($receipt.execution -ne "NOT_PERFORMED") { throw "Receipt execution mismatch" }

Write-Host "AION_ADAPTIVE_REASONING_LAYER_V1_VERIFY_OK"
