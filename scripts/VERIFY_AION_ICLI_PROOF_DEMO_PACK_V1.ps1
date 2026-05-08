param()

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $repoRoot

powershell -NoProfile -ExecutionPolicy Bypass `
    -File ".\proof_demo_pack\VERIFY_AION_ICLI_PROOF_DEMO_PACK_V1.ps1"

Write-Host "AION_ICLI_PROOF_DEMO_PACK_V1_ROOT_VERIFY_OK"
