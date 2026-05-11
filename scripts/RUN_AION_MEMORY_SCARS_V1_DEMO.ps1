$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$demoDir = Join-Path $Repo "demo_memory"
if(-not (Test-Path -LiteralPath $demoDir)){ New-Item -ItemType Directory -Path $demoDir | Out-Null }

$scarPath = Join-Path $demoDir "scar.json"
$eventPath = Join-Path $demoDir "event.json"
$reportOut = Join-Path $Repo "reports\AION_MEMORY_SCARS_V1_DEMO_REPORT.md"
$releaseOut = Join-Path $Repo "release\AION_MEMORY_SCARS_V1_DEMO_RESULT.json"

$scar = @{
  scar_id = "scar_missing_verifier_exec"
  trigger = "agent wants to execute script without verifier"
  harm = "false confidence and unsafe execution"
  repair = "require verifier and dry-run before execution"
  future_rule = "BLOCK execution when verifier is missing"
  severity = "HIGH"
  tags = @("execution","verifier")
  public_safe = $true
}
$event = @{
  source = "PreflightGate"
  action_type = "script"
  risk_signals = @("execution")
  missing_controls = @("verifier")
  summary = "Agent wants to execute script without verifier"
}

$scar | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $scarPath
$event | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $eventPath

$addJson = ((python .\src\aion_memory_scars.py add --input $scarPath) | Out-String) | ConvertFrom-Json
$evalJson = ((python .\src\aion_memory_scars.py evaluate --input $eventPath) | Out-String) | ConvertFrom-Json

$result = [pscustomobject]@{
  demo = "AION_MEMORY_SCARS_V1"
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  add_result = $addJson
  evaluate_result = $evalJson
}
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $releaseOut

$lines = @()
$lines += "# AION Memory Scars V1 Demo Report"
$lines += ""
$lines += "- Generated UTC: " + ((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"))
$lines += "- Added scar id: " + $addJson.scar_id
$lines += "- Evaluate bias: " + $evalJson.recommended_decision_bias
$lines += "- Matched scars: " + @($evalJson.matched_scars).Count
$lines += "- Receipt: " + $evalJson.receipt_path
$lines -join "`r`n" | Set-Content -LiteralPath $reportOut

Write-Host "AION_MEMORY_SCARS_V1_DEMO_OK"
