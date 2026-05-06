$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Public Install Package V1 verifier"

$zip = ".\dist\aion-icli-public-install-package-v1.zip"
$doc = ".\docs\PUBLIC_INSTALL_PACKAGE_V1.md"
$manifest = ".\packaging\public-install\public_install_package_v1.manifest.json"
$report = ".\reports\PUBLIC_INSTALL_PACKAGE_V1_REPORT.md"

function Assert-Exists {
  param([string]$Path, [string]$Message)
  if (-not (Test-Path -LiteralPath $Path)) {
    throw $Message
  }
}

function Assert-Absent {
  param([string]$Path, [string]$Message)
  if (Test-Path -LiteralPath $Path) {
    throw $Message
  }
}

function Test-PackageTree {
  param([string]$Root)

  $mustExist = @(
    "README.md",
    "install.ps1",
    "install.sh",
    "bin\aion.cmd",
    "bin\aion.ps1",
    "bin\aion",
    "src\aion_cli_entry.py",
    "scripts\VERIFY_PUBLIC_SAFE.ps1",
    "scripts\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1",
    "docs\PUBLIC_INSTALL_PACKAGE_V1.md",
    "reports\CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md",
    "reports\PUBLIC_INSTALL_PACKAGE_V1_REPORT.md",
    "packaging\public-install\public_install_package_v1.manifest.json"
  )

  foreach ($p in $mustExist) {
    $target = Join-Path $Root $p
    Assert-Exists $target "Missing package file: $p"
  }

  $forbidden = @(
    ".env",
    ".codara",
    ".aion",
    "node_modules",
    "private",
    "secrets",
    "receipts\local",
    "examples\governance\generated",
    "examples\api-adapter\generated",
    "examples\model-adapter\generated",
    "examples\sdk\generated",
    "examples\proofs\generated"
  )

  foreach ($f in $forbidden) {
    $target = Join-Path $Root $f
    Assert-Absent $target "Forbidden path exists in package: $f"
  }
}

Assert-Exists $doc "Missing package doc: $doc"
Assert-Exists $manifest "Missing package manifest: $manifest"
Assert-Exists $report "Missing package report: $report"

$m = Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json
if ($m.includes_exe -ne $false) { throw "Manifest must not include exe" }
if ($m.includes_signed_installer -ne $false) { throw "Manifest must not include signed installer" }
if ($m.includes_private_credentials -ne $false) { throw "Manifest must not include private credentials" }
if ($m.includes_provider_keys -ne $false) { throw "Manifest must not include provider keys" }

if (Test-Path -LiteralPath $zip) {
  $zipInfo = Get-Item -LiteralPath $zip
  if ($zipInfo.Length -le 0) {
    throw "ZIP package is empty"
  }

  $extractRoot = Join-Path $env:TEMP ("aion-icli-public-install-package-v1-verify-" + [guid]::NewGuid().ToString("N"))
  New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null

  try {
    Expand-Archive -LiteralPath $zip -DestinationPath $extractRoot -Force
    Test-PackageTree -Root $extractRoot
  }
  finally {
    if (Test-Path -LiteralPath $extractRoot) {
      Remove-Item -LiteralPath $extractRoot -Recurse -Force
    }
  }
} else {
  Test-PackageTree -Root $Repo
}

Write-Host "AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK"
