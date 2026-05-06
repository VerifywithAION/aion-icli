$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION ICLI GitHub Release V1 Draft verifier"

$expectedReleaseDocsHead = "3ab076d"
$expectedPackageHead = "2fea528"
$expectedSha = "8B99C3C7161F2911212E7D57A4F3A3782700DBBCE404288D1E4AD6A671D7D746"
$zip = ".\dist\aion-icli-public-install-package-v1.zip"

$required = @(
  "docs\GITHUB_RELEASE_V1_DRAFT.md",
  "reports\GITHUB_RELEASE_V1_CHECKLIST.md",
  "docs\USER_GUIDE_V1.md",
  "scripts\VERIFY_GITHUB_RELEASE_V1_DRAFT.ps1",
  "scripts\VERIFY_USER_GUIDE_V1.ps1",
  "scripts\VERIFY_PUBLIC_SAFE.ps1",
  "scripts\VERIFY_CONNECTOR_POLICY_V2.ps1",
  "scripts\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1",
  $zip
)

foreach ($p in $required) {
  if (-not (Test-Path -LiteralPath $p)) {
    throw "Missing release artifact: $p"
  }
}

$head = git rev-parse --short HEAD
if ($head -ne $expectedReleaseDocsHead) {
  throw "Unexpected release docs HEAD. Expected $expectedReleaseDocsHead, got $head"
}

$sha = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash
if ($sha -ne $expectedSha) {
  throw "Unexpected ZIP SHA256. Expected $expectedSha, got $sha"
}

$draft = Get-Content -LiteralPath ".\docs\GITHUB_RELEASE_V1_DRAFT.md" -Raw
$checklist = Get-Content -LiteralPath ".\reports\GITHUB_RELEASE_V1_CHECKLIST.md" -Raw

$requiredDraftText = @(
  "AION ICLI Public Release V1",
  "v1.0.0-public-icli",
  $expectedPackageHead,
  $expectedSha,
  "AION_ICLI_PUBLIC_SAFE_VERIFY_OK",
  "AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK",
  "AION_USER_GUIDE_V1_VERIFY_OK",
  "Governance should be felt, not seen."
)

foreach ($r in $requiredDraftText) {
  if (-not $draft.Contains($r)) {
    throw "Release draft missing required text: $r"
  }
}

$requiredChecklistText = @(
  "Target commit: $expectedPackageHead",
  "Asset: dist/aion-icli-public-install-package-v1.zip",
  "SHA256: $expectedSha"
)

foreach ($r in $requiredChecklistText) {
  if (-not $checklist.Contains($r)) {
    throw "Release checklist missing required text: $r"
  }
}

Write-Host "AION_GITHUB_RELEASE_V1_DRAFT_VERIFY_OK"
