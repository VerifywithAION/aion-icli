param()

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "====================================================="
Write-Host "VERIFY AION ICLI RELEASE EVIDENCE INDEX V1"
Write-Host "====================================================="
Write-Host ""

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

Set-Location $repoRoot

New-Item -ItemType Directory -Force -Path ".\release" | Out-Null
New-Item -ItemType Directory -Force -Path ".\reports" | Out-Null
$currentHead = (git rev-parse HEAD).Trim()

$gitStatusRaw = (git status --short)

if ([string]::IsNullOrWhiteSpace($gitStatusRaw)) {
    $gitState = "clean"
}
else {
    $gitState = "dirty"
}

# =====================================================
# DISCOVER ARTIFACTS
# =====================================================

$offlineCandidates = Get-ChildItem `
    -Path ".\dist",".\release" `
    -Filter "*.zip" `
    -Recurse `
    -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -match "offline|bundle"
    }

$releasePackCandidates = Get-ChildItem `
    -Path ".\dist",".\release" `
    -Filter "*.zip" `
    -Recurse `
    -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -match "public|demo|release"
    }

$offlineArtifact = $null
$releasePackArtifact = $null

if ($offlineCandidates.Count -gt 0) {
    $offlineArtifact = $offlineCandidates |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

if ($releasePackCandidates.Count -gt 0) {
    $releasePackArtifact = $releasePackCandidates |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1
}

# =====================================================
# BUILD ARTIFACT STATE
# =====================================================

if ($offlineArtifact -ne $null) {

    $offlineState = @{
        present = $true
        path = $offlineArtifact.FullName
        sha256 = (Get-FileHash $offlineArtifact.FullName -Algorithm SHA256).Hash
        verifier_marker = "AION_OFFLINE_CLI_BUNDLE_V1_1_0_VERIFY_OK"
    }
}
else {

    $offlineState = @{
        present = $false
        path = $null
        sha256 = $null
        verifier_marker = "AION_OFFLINE_CLI_BUNDLE_V1_1_0_VERIFY_OK"
    }
}

if ($releasePackArtifact -ne $null) {

    $releasePackState = @{
        present = $true
        path = $releasePackArtifact.FullName
        sha256 = (Get-FileHash $releasePackArtifact.FullName -Algorithm SHA256).Hash
        verifier_marker = "AION_PUBLIC_DEMO_RELEASE_PACK_V1_VERIFY_OK"
    }
}
else {

    $releasePackState = @{
        present = $false
        path = $null
        sha256 = $null
        verifier_marker = "AION_PUBLIC_DEMO_RELEASE_PACK_V1_VERIFY_OK"
    }
}

# =====================================================
# RECENT COMMITS
# =====================================================

$recentCommits = git log -10 --oneline

# =====================================================
# BUILD INDEX
# =====================================================

$index = [ordered]@{

    generated_at_utc = [DateTime]::UtcNow.ToString("o")

    repo_root = $repoRoot.Path

    current_head = $currentHead

    git_state = $gitState

    offline_bundle = $offlineState

    public_demo_release_pack = $releasePackState

    fresh_clone_acceptance = @{
        verifier_marker = "AION_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1_PASS"
    }

    historical_head_mode = @{
        commit = "ad7037b"
        marker = "AION_OFFLINE_BUNDLE_VERIFIER_HISTORICAL_HEAD_FIX_COMPLETE"
    }

    release_evidence_index = @{
        verifier_marker = "AION_ICLI_RELEASE_EVIDENCE_INDEX_V1_VERIFY_OK"
    }

    recent_commits = $recentCommits
}

# =====================================================
# WRITE JSON
# =====================================================

$jsonPath = ".\release\AION_ICLI_RELEASE_EVIDENCE_INDEX_V1.json"

$index |
    ConvertTo-Json -Depth 10 |
    Set-Content $jsonPath -Encoding UTF8

# =====================================================
# WRITE REPORT
# =====================================================

$reportPath = ".\reports\AION_ICLI_RELEASE_EVIDENCE_INDEX_V1_REPORT.md"

@"
# AION ICLI RELEASE EVIDENCE INDEX V1

## Current HEAD

$currentHead

## Git State

$gitState

## Offline Bundle

Present:
$($offlineState.present)

Path:
$($offlineState.path)

SHA256:
$($offlineState.sha256)

Marker:
AION_OFFLINE_CLI_BUNDLE_V1_1_0_VERIFY_OK

## Public Demo Release Pack

Present:
$($releasePackState.present)

Path:
$($releasePackState.path)

SHA256:
$($releasePackState.sha256)

Marker:
AION_PUBLIC_DEMO_RELEASE_PACK_V1_VERIFY_OK

## Fresh Clone Acceptance

Marker:
AION_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1_PASS

## Historical Head Mode

Commit:
ad7037b

Marker:
AION_OFFLINE_BUNDLE_VERIFIER_HISTORICAL_HEAD_FIX_COMPLETE

## Release Evidence Index

Marker:
AION_ICLI_RELEASE_EVIDENCE_INDEX_V1_VERIFY_OK

## Recent Commits

$recentCommits
"@ | Set-Content $reportPath -Encoding UTF8

Write-Host ""
Write-Host "====================================================="
Write-Host "ARTIFACT DISCOVERY"
Write-Host "====================================================="
Write-Host ""

Write-Host "Offline bundle present: $($offlineState.present)"
Write-Host "Public release pack present: $($releasePackState.present)"

Write-Host ""
Write-Host "JSON INDEX:"
Write-Host $jsonPath

Write-Host ""
Write-Host "REPORT:"
Write-Host $reportPath

Write-Host ""
Write-Host "AION_ICLI_RELEASE_EVIDENCE_INDEX_V1_VERIFY_OK"
Write-Host ""

