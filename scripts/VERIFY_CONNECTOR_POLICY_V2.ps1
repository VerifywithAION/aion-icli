function Test-AionGitRepo {
  return (Test-Path -LiteralPath ".\.git")
}

function Invoke-AionGitIfPresent {
  param([string[]]$GitArgs)

  if (Test-AionGitRepo) {
    & git @GitArgs
  }
}
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI Connector Policy V2 verifier"

$required = @(
  "docs\CONNECTOR_POLICY_V2.md",
  "schemas\aion-connector-request-v2.schema.json",
  "examples\connectors\connector_request_allow_v2.json",
  "examples\connectors\connector_request_block_v2.json"
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing required file: $p"
  }
}

$policy = Get-Content -LiteralPath ".\docs\CONNECTOR_POLICY_V2.md" -Raw
$mustContain = @(
  "Connect to AION governance.",
  "Do not expose, bypass, clone, or reconstruct AION internals.",
  "network access is off by default",
  "mutation is off by default",
  "receipts are required",
  "LOCKED as public connector boundary policy"
)

foreach ($m in $mustContain) {
  if ($policy -notlike "*$m*") {
    throw "Connector policy missing required text: $m"
  }
}

$allow = Get-Content -LiteralPath ".\examples\connectors\connector_request_allow_v2.json" -Raw | ConvertFrom-Json
$block = Get-Content -LiteralPath ".\examples\connectors\connector_request_block_v2.json" -Raw | ConvertFrom-Json

if ($allow.network_policy.requested -ne $false) { throw "ALLOW example should not request network" }
if ($allow.mutation_policy.requested -ne $false) { throw "ALLOW example should not request mutation" }
if ($allow.execution_mode -ne "dry_run") { throw "ALLOW example should be dry_run" }

if ($block.network_policy.requested -ne $true) { throw "BLOCK example should request network" }
if ($block.mutation_policy.requested -ne $true) { throw "BLOCK example should request mutation" }
if ($block.execution_mode -ne "execute") { throw "BLOCK example should request execute" }

$badExact = @(
  "secret_key",
  "api_key_value",
  "bearer ",
  "sk-",
  "xoxb-"
)

$allText = ""
foreach ($file in (if (Test-AionGitRepo) { git ls-files } | Where-Object { $_ -match "\.(md|txt|ps1|py|json|cmd|sh|yml|yaml|svg)$" })) {
  if ($file -eq "scripts/VERIFY_CONNECTOR_POLICY_V2.ps1") {
    continue
  }
  if (Test-Path -LiteralPath $file) {
    $allText += "`nFILE: $file`n"
    $allText += Get-Content -LiteralPath $file -Raw -ErrorAction SilentlyContinue
  }
}
$allText += "`nFILE: docs/CONNECTOR_POLICY_V2.md`n"
$allText += $policy

foreach ($b in $badExact) {
  if ($allText.ToLowerInvariant() -like ("*" + $b.ToLowerInvariant() + "*")) {
    throw "Found forbidden secret-like pattern: $b"
  }
}

Write-Host "AION_CONNECTOR_POLICY_V2_VERIFY_OK"


