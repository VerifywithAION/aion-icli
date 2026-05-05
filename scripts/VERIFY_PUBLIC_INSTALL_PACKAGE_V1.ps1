$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Public Install Package V1 verifier"

$zip = ".\dist\aion-icli-public-install-package-v1.zip"
$doc = ".\docs\PUBLIC_INSTALL_PACKAGE_V1.md"
$manifest = ".\packaging\public-install\public_install_package_v1.manifest.json"
$report = ".\reports\PUBLIC_INSTALL_PACKAGE_V1_REPORT.md"

$required = @($zip, $doc, $manifest, $report)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing package artifact: $p"
  }
}

$zipInfo = Get-Item -LiteralPath $zip
if ($zipInfo.Length -le 0) {
  throw "ZIP package is empty"
}

$m = Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json
if ($m.includes_exe -ne $false) { throw "Manifest must not include exe" }
if ($m.includes_signed_installer -ne $false) { throw "Manifest must not include signed installer" }
if ($m.includes_private_credentials -ne $false) { throw "Manifest must not include private credentials" }
if ($m.includes_provider_keys -ne $false) { throw "Manifest must not include provider keys" }

$extractRoot = Join-Path $env:TEMP ("aion-icli-public-install-package-v1-verify-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null

try {
  Expand-Archive -LiteralPath $zip -DestinationPath $extractRoot -Force

  $mustExistInZip = @(
    "README.md",
    "install.ps1",
    "install.sh",
    "bin\aion.cmd",
    "bin\aion.ps1",
    "bin\aion",
    "src\aion_cli_entry.py",
    "scripts\VERIFY_PUBLIC_SAFE.ps1",
    "docs\PUBLIC_INSTALL_PACKAGE_V1.md",
    "reports\CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md"
  )

  foreach ($p in $mustExistInZip) {
    $target = Join-Path $extractRoot $p
    if (-not (Test-Path -LiteralPath $target)) {
      throw "Missing file inside ZIP: $p"
    }
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
    $target = Join-Path $extractRoot $f
    if (Test-Path -LiteralPath $target) {
      throw "Forbidden path included in ZIP: $f"
    }
  }
}
finally {
  if (Test-Path -LiteralPath $extractRoot) {
    Remove-Item -LiteralPath $extractRoot -Recurse -Force
  }
}

Write-Host "AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK"
