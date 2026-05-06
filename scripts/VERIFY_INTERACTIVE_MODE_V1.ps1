$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Interactive Mode V1 verifier"

$required = @(
  "src\aion_cli_entry.py",
  "docs\INTERACTIVE_MODE_V1.md",
  "bin\aion.cmd",
  "bin\aion.ps1"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing interactive mode artifact: $p"
  }
}

$source = Get-Content -LiteralPath ".\src\aion_cli_entry.py" -Raw
$doc = Get-Content -LiteralPath ".\docs\INTERACTIVE_MODE_V1.md" -Raw

$requiredSource = @(
  "def run_interactive",
  "Interactive Mode V1",
  "Type help for commands",
  "mode=`"interactive`"",
  "help",
  "receipt",
  "boundary",
  "verify",
  "exit"
)

foreach ($r in $requiredSource) {
  if (-not $source.Contains($r)) {
    throw "CLI source missing interactive text: $r"
  }
}

$requiredDoc = @(
  "AION ICLI Interactive Mode V1",
  "local-first",
  "no network by default",
  "receipt-bound",
  "AION_INTERACTIVE_MODE_V1_VERIFY_OK"
)

foreach ($r in $requiredDoc) {
  if (-not $doc.Contains($r)) {
    throw "Interactive doc missing required text: $r"
  }
}

$env:AION_FORCE_COLOR = "1"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$oneShot = cmd.exe /d /c '".\bin\aion.cmd" "Who are you, AION?"' 2>&1 | Out-String
if ($oneShot -notlike "*Boundary >*LOCAL_ONLY*" -or $oneShot -notlike "*Receipt  >*") {
  Write-Host $oneShot
  throw "One-shot CLI smoke failed after interactive mode patch"
}

$script = "help`nreceipt`nboundary`nexit`n"
$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value $script -Encoding ASCII

try {
  $interactive = cmd.exe /d /c "type `"$tmp`" | .\bin\aion.cmd" 2>&1 | Out-String
}
finally {
  if (Test-Path -LiteralPath $tmp) {
    Remove-Item -LiteralPath $tmp -Force
  }
}

if ($interactive -notlike "*Interactive Mode V1*" -or
    $interactive -notlike "*Available commands*" -or
    $interactive -notlike "*Latest receipt path*" -or
    $interactive -notlike "*Current boundary: LOCAL_ONLY*" -or
    $interactive -notlike "*Session closed*") {
  Write-Host $interactive
  throw "Interactive mode scripted smoke failed"
}

if (-not (Test-Path -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json")) {
  throw "Interactive mode did not write receipt"
}

$receipt = Get-Content -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json" -Raw | ConvertFrom-Json
if ($receipt.mode -ne "interactive") {
  throw "Interactive receipt mode mismatch"
}
if ($receipt.boundary -ne "LOCAL_ONLY") {
  throw "Interactive receipt boundary mismatch"
}
if ($receipt.network -ne "NOT_USED") {
  throw "Interactive receipt network mismatch"
}
if ($receipt.mutation -ne "NOT_PERFORMED") {
  throw "Interactive receipt mutation mismatch"
}

Write-Host "AION_INTERACTIVE_MODE_V1_VERIFY_OK"
