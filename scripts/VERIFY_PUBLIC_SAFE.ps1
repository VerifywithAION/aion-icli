$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Remove-AionAnsi {
  param([string]$Text)

  if ($null -eq $Text) {
    return ""
  }

  $esc = [char]27
  $pattern = [regex]::Escape([string]$esc) + "\[[0-9;?]*[ -/]*[@-~]"
  $s = [regex]::Replace($Text, $pattern, "")
  $s = $s -replace "`0", ""
  $s = $s -replace "`r`n", "`n"
  $s = $s -replace "`r", "`n"
  return $s
}

function Invoke-AionCapture {
  param(
    [string]$Label,
    [string]$Command
  )

  $env:PYTHONUTF8 = "1"
  $env:PYTHONIOENCODING = "utf-8"
  $env:AION_FORCE_COLOR = "1"

  $output = cmd.exe /d /c $Command 2>&1
  $exitCode = $LASTEXITCODE
  $combined = Remove-AionAnsi (($output | Out-String))

  if ($exitCode -ne 0) {
    Write-Host "----- ${Label} STDOUT/STDERR -----"
    Write-Host $combined
    throw "${Label} failed with exit code $exitCode"
  }

  return $combined
}

function Assert-ContainsLiteral {
  param(
    [string]$Text,
    [string]$Needle,
    [string]$Message
  )

  if (-not $Text.Contains($Needle)) {
    Write-Host "----- CAPTURED OUTPUT BEGIN -----"
    Write-Host $Text
    Write-Host "----- CAPTURED OUTPUT END -----"
    throw $Message
  }
}

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI public-safe verifier"

$required = @(
  "README.md",
  "install.ps1",
  "install.sh",
  "aion.ps1",
  "bin\aion.cmd",
  "bin\aion.ps1",
  "bin\aion",
  "src\aion_cli_entry.py",
  "docs\PUBLIC_BOUNDARY.md",
  "docs\HARDENING_NOTE_V1.md"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing required public-safe file: $p"
  }
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $pythonCmd) {
  throw "Missing command on PATH: python"
}

$direct = Invoke-AionCapture `
  -Label "Direct Python CLI" `
  -Command 'python ".\src\aion_cli_entry.py" "Who are you, AION?"'

Assert-ContainsLiteral $direct "AION ICLI" "Missing AION title"
Assert-ContainsLiteral $direct "Interactive Command Line Intelligence" "Missing ICLI subtitle"
Assert-ContainsLiteral $direct "Boundary > LOCAL_ONLY" "Missing local boundary"
Assert-ContainsLiteral $direct "Network  > NOT_USED" "Missing network boundary"
Assert-ContainsLiteral $direct "Mutation > NOT_PERFORMED" "Missing mutation boundary"
Assert-ContainsLiteral $direct "Receipt  > receipts\local\aion_cli_receipt_v1.json" "Missing receipt path"

$cmd = Invoke-AionCapture `
  -Label "Windows CMD launcher" `
  -Command '".\bin\aion.cmd" "Who are you, AION?"'

Assert-ContainsLiteral $cmd "Boundary > LOCAL_ONLY" "CMD launcher missing local boundary"
Assert-ContainsLiteral $cmd "Network  > NOT_USED" "CMD launcher missing network boundary"
Assert-ContainsLiteral $cmd "Mutation > NOT_PERFORMED" "CMD launcher missing mutation boundary"

$ps = Invoke-AionCapture `
  -Label "PowerShell launcher" `
  -Command 'powershell -NoProfile -ExecutionPolicy Bypass -File ".\bin\aion.ps1" "Who are you, AION?"'

Assert-ContainsLiteral $ps "Boundary > LOCAL_ONLY" "PowerShell launcher missing local boundary"
Assert-ContainsLiteral $ps "Network  > NOT_USED" "PowerShell launcher missing network boundary"
Assert-ContainsLiteral $ps "Mutation > NOT_PERFORMED" "PowerShell launcher missing mutation boundary"

$forbiddenPaths = @(
  ".env",
  "node_modules",
  ".codara",
  ".aion",
  "private",
  "secrets",
  "aion-icli"
)

foreach ($fp in $forbiddenPaths) {
  if (Test-Path -LiteralPath $fp) {
    throw "Forbidden public repo path exists: $fp"
  }
}

Write-Host "AION_ICLI_PUBLIC_SAFE_VERIFY_OK"
