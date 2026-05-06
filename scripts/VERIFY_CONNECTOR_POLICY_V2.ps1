$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Connector Policy V2 verifier"

$SelfRelative = "scripts\VERIFY_CONNECTOR_POLICY_V2.ps1"

$required = @(
  "docs\CONNECTOR_POLICY_V2.md",
  "schemas\aion-connector-request-v2.schema.json",
  "examples\connectors\connector_request_allow_v2.json",
  "examples\connectors\connector_request_block_v2.json"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing connector policy artifact: $p"
  }
}

$doc = Get-Content -LiteralPath ".\docs\CONNECTOR_POLICY_V2.md" -Raw
$schema = Get-Content -LiteralPath ".\schemas\aion-connector-request-v2.schema.json" -Raw
$allow = Get-Content -LiteralPath ".\examples\connectors\connector_request_allow_v2.json" -Raw | ConvertFrom-Json
$block = Get-Content -LiteralPath ".\examples\connectors\connector_request_block_v2.json" -Raw | ConvertFrom-Json

$mustContain = @(
  "Connector Policy V2",
  "local",
  "receipt"
)

foreach ($m in $mustContain) {
  if (-not $doc.ToLowerInvariant().Contains($m.ToLowerInvariant())) {
    throw "Connector policy doc missing required concept: $m"
  }
}

if (-not $schema.Contains("connector")) {
  throw "Connector request schema missing connector concept"
}

if ($null -eq $allow.request_id) {
  throw "Allow connector example missing request_id"
}

if ($null -eq $block.request_id) {
  throw "Block connector example missing request_id"
}

$scanFiles = @()

if (Test-Path -LiteralPath ".\.git") {
  $gitFiles = git ls-files 2>$null
  if ($LASTEXITCODE -eq 0 -and $gitFiles) {
    $scanFiles = @($gitFiles)
  }
}

if (-not $scanFiles -or $scanFiles.Count -eq 0) {
  $scanFiles = Get-ChildItem -LiteralPath "." -Recurse -File |
    Where-Object {
      $_.FullName -notmatch "\\\.git\\" -and
      $_.FullName -notmatch "\\dist\\" -and
      $_.FullName -notmatch "\\examples\\.*\\generated\\" -and
      $_.FullName -notmatch "\\receipts\\local\\"
    } |
    ForEach-Object {
      Resolve-Path -LiteralPath $_.FullName -Relative
    }
}

$forbidden = @(
  "OPENAI_API_KEY=",
  "ANTHROPIC_API_KEY=",
  "GEMINI_API_KEY=",
  "PRIVATE_KEY=",
  "SECRET_KEY=",
  "ACCESS_TOKEN=",
  "BEARER_TOKEN="
)

foreach ($file in $scanFiles) {
  $normalized = $file.Replace("/", "\").TrimStart(".", "\")

  if ($normalized -ieq $SelfRelative) {
    continue
  }

  if (-not (Test-Path -LiteralPath $file)) {
    continue
  }

  $item = Get-Item -LiteralPath $file
  if ($item.Length -gt 1048576) {
    continue
  }

  $content = Get-Content -LiteralPath $file -Raw -ErrorAction SilentlyContinue
  if ($null -eq $content) {
    continue
  }

  foreach ($bad in $forbidden) {
    if ($content.Contains($bad)) {
      throw "Forbidden secret-like assignment found in ${file}: $bad"
    }
  }
}

Write-Host "AION_CONNECTOR_POLICY_V2_VERIFY_OK"

