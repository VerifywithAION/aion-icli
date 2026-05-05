$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Set-Location (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition))

function Remove-AionAnsi {
  param([string]$Text)
  if ($null -eq $Text) { return "" }
  return [regex]::Replace($Text, "`e\[[0-9;]*m", "")
}
Write-Host "AION ICLI public-safe verifier"

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Invoke-Capture {
  param(
    [string]$FilePath,
    [string[]]$ArgumentList,
    [string]$Label
  )

  $tmpOut = [System.IO.Path]::GetTempFileName()
  $tmpErr = [System.IO.Path]::GetTempFileName()

  try {
    $p = Start-Process -FilePath $FilePath `
      -ArgumentList $ArgumentList `
      -NoNewWindow `
      -Wait `
      -PassThru `
      -RedirectStandardOutput $tmpOut `
      -RedirectStandardError $tmpErr

    $stdout = Get-Content -LiteralPath $tmpOut -Raw -ErrorAction SilentlyContinue
    $stderr = Get-Content -LiteralPath $tmpErr -Raw -ErrorAction SilentlyContinue
    $combined = ($stdout + "`n" + $stderr)

    if ($p.ExitCode -ne 0) {
      Write-Host "----- $Label STDOUT/STDERR -----"
      Write-Host $combined
      throw "$Label failed with exit code $($p.ExitCode)"
    }

    return $combined
  }
  finally {
    Remove-Item -LiteralPath $tmpOut,$tmpErr -Force -ErrorAction SilentlyContinue
  }
}

$required = @(
  "README.md",
  "install.ps1",
  "install.sh",
  "bin\aion.cmd",
  "bin\aion.ps1",
  "bin\aion",
  "aion.ps1",
  "src\aion_cli_entry.py",
  "docs\PUBLIC_BOUNDARY.md",
  "docs\HARDENING_NOTE_V1.md",
  "docs\REPO_GUIDED_TOUR_V1.md",
  "examples\basic_usage.txt"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing required public file: $p"
  }
}

$bad = @(
  "bounty",
  "counterfactual",
  "control-plane",
  "graph_commit",
  "authority_lock",
  "reality_transition",
  "private_key",
  "secret",
  "token"
)

$files = Get-ChildItem -Recurse -File -Force | Where-Object { $_.FullName -notmatch "\\.git\\" }

foreach ($file in $files) {
  $rel = $file.FullName.Replace((Get-Location).Path + "\", "")
  foreach ($pat in $bad) {
    if ($rel.ToLowerInvariant().Contains($pat)) {
      throw "Forbidden public filename pattern '$pat' in $rel"
    }
  }
}

$parseErrors = $null
[System.Management.Automation.PSParser]::Tokenize((Get-Content -Raw "bin\aion.ps1"), [ref]$parseErrors) | Out-Null
if ($parseErrors -and $parseErrors.Count -gt 0) {
  throw "PowerShell parse errors in bin/aion.ps1"
}

$parseErrors = $null
[System.Management.Automation.PSParser]::Tokenize((Get-Content -Raw "aion.ps1"), [ref]$parseErrors) | Out-Null
if ($parseErrors -and $parseErrors.Count -gt 0) {
  throw "PowerShell parse errors in aion.ps1"
}

python -m py_compile "src\aion_cli_entry.py"
if ($LASTEXITCODE -ne 0) {
  throw "Python CLI entry compile failed"
}

$outDirect = Invoke-Capture -FilePath "python" -ArgumentList @(".\src\aion_cli_entry.py", "Who are you, AION?") -Label "Direct Python CLI"
$outPs = Invoke-Capture -FilePath "powershell" -ArgumentList @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ".\bin\aion.ps1", "Who are you, AION?") -Label "PowerShell launcher"
$outCmd = Invoke-Capture -FilePath ".\bin\aion.cmd" -ArgumentList @("Who are you, AION?") -Label "CMD launcher"

foreach ($out in @($outDirect, $outPs, $outCmd)) {
  if ($out -notlike "*AION ICLI*") { throw "Missing AION ICLI banner" }
  if ($out -notlike "*Interactive Command Line Intelligence*") { throw "Missing ICLI definition" }
  if ($out -notlike "*Offline-capable by design*") { throw "Missing offline banner" }
  if ($out -notlike "*Boundary > LOCAL_ONLY*") { throw "Missing local boundary" }
  if ($out -notlike "*Network  > NOT_USED*") { throw "Missing network boundary" }
  if ($out -notlike "*Mutation > NOT_PERFORMED*") { throw "Missing mutation boundary" }
  if ($out -like "*Traceback*") { throw "Traceback detected in launcher output" }
  if ($out -like "*ModuleNotFoundError*") { throw "ModuleNotFoundError detected in launcher output" }
}

if (-not (Test-Path -LiteralPath "receipts\local\aion_cli_receipt_v1.json")) {
  throw "Missing local runtime receipt"
}

Write-Host "AION_ICLI_PUBLIC_SAFE_VERIFY_OK"
