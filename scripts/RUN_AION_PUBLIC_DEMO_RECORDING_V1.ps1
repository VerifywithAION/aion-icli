param()
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

Write-Host "AION PUBLIC DEMO RECORDING V1"
Write-Host "=============================="

& .\bin\aion.cmd "who are you"
& powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_DEMO_ORCHESTRATOR_V1.ps1
& python .\src\aion_introspection_engine.py status

Write-Host "AION_DEMO_ORCHESTRATOR_V1_OK"
Write-Host "AION_PUBLIC_DEMO_RECORDING_V1_READY"
