$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Public Release Lock V1 verifier"

$required = @(
  "README.md",
  "docs\PUBLIC_BOUNDARY.md",
  "docs\HARDENING_NOTE_V1.md",
  "docs\REPO_GUIDED_TOUR_V1.md",
  "docs\PUBLIC_RELEASE_LOCK_V1.md",
  "reports\FRESH_CLONE_CLEANLINESS_TEST_V3.md",
  "scripts\VERIFY_PUBLIC_SAFE.ps1",
  "scripts\VERIFY_LOCAL_GOVERNANCE_PROXY_V1.ps1",
  "scripts\RUN_LOCAL_GOVERNANCE_PROXY_DEMO_V1.ps1",
  "bin\aion.cmd",
  "bin\aion.ps1",
  "bin\aion",
  "src\aion_cli_entry.py"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) { throw "Missing required release lock file: $p" }
}

powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\VERIFY_PUBLIC_SAFE.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\VERIFY_LOCAL_GOVERNANCE_PROXY_V1.ps1"

$lock = Get-Content -LiteralPath ".\docs\PUBLIC_RELEASE_LOCK_V1.md" -Raw
if ($lock -notlike "*No external APIs by default*") { throw "Missing no external APIs boundary" }
if ($lock -notlike "*No private AION internals exposed*") { throw "Missing private internals boundary" }
if ($lock -notlike "*LOCKED as public-safe release baseline*") { throw "Missing locked status" }

$report = Get-Content -LiteralPath ".\reports\FRESH_CLONE_CLEANLINESS_TEST_V3.md" -Raw
if ($report -notlike "*AION_ICLI_FRESH_CLONE_CLEANLINESS_TEST_V3_PASS*") { throw "Missing fresh clone pass marker" }

if (Test-Path -LiteralPath ".\receipts\local") {
  Remove-Item -LiteralPath ".\receipts\local" -Recurse -Force
}

Write-Host "AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK"
