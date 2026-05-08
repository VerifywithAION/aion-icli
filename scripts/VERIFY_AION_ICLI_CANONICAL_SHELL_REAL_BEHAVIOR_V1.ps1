$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Canonical Shell + Real Behavior V1 verifier"

$script = @"
what do you know about this release?
why do you need proof?
should I run this script??
should I run proof_demo_pack\VERIFY_AION_ICLI_PROOF_DEMO_PACK_V1.ps1?
diagnostics on
next
exit
"@

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

$normalized = $out -replace "`e\[[0-9;]*m", ""
$normalized = $normalized -replace "\s+", " "
$normalized = $normalized.Trim()

$must = @(
  "AION ICLI",
  "Interactive Command Line Intelligence",
  "Governed Local Mode",
  "Offline-capable by design",
  "No external APIs by default",
  "What I can do offline",
  "I can see the local release proof chain",
  "No artifact, no judgment",
  "I inspected the local artifact read-only",
  "Decision:",
  "Risk:",
  "Next build pointer",
  "Capability > NEXT",
  "Boundary > LOCAL_ONLY",
  "Network > NOT_USED",
  "Mutation > NOT_PERFORMED"
)

foreach ($m in $must) {
  if ($normalized -notlike "*$m*") {
    Write-Host "----- RAW OUTPUT -----"
    Write-Host $out
    Write-Host "----- NORMALIZED OUTPUT -----"
    Write-Host $normalized
    throw "Missing expected runtime output: $m"
  }
}

if (-not (Test-Path -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json")) {
  throw "Missing runtime receipt"
}

$receipt = Get-Content -LiteralPath ".\receipts\local\aion_cli_receipt_v1.json" -Raw | ConvertFrom-Json

if ($receipt.boundary -ne "LOCAL_ONLY") { throw "Receipt boundary mismatch" }
if ($receipt.network -ne "NOT_USED") { throw "Receipt network mismatch" }
if ($receipt.mutation -ne "NOT_PERFORMED") { throw "Receipt mutation mismatch" }
if ($receipt.execution -ne "NOT_PERFORMED") { throw "Receipt execution mismatch" }

Write-Host "AION_ICLI_CANONICAL_SHELL_REAL_BEHAVIOR_V1_VERIFY_OK"
