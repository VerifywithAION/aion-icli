$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION Evaluate API Adapter V1"
Write-Host "Starting local server at http://127.0.0.1:8765"
Write-Host "Stop with Ctrl+C"

python .\src\aion_evaluate_api.py
