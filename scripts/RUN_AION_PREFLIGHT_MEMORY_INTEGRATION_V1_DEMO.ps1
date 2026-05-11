$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$reportOut = Join-Path $Repo "reports\AION_PREFLIGHT_MEMORY_INTEGRATION_V1_DEMO_REPORT.md"
$releaseOut = Join-Path $Repo "release\AION_PREFLIGHT_MEMORY_INTEGRATION_V1_DEMO_RESULT.json"
$scarPath = Join-Path $Repo "demo_memory\integration_scar.json"
$eventPath = Join-Path $Repo "demo_memory\integration_event.json"

if(-not (Test-Path -LiteralPath (Split-Path $scarPath -Parent))){
  New-Item -ItemType Directory -Path (Split-Path $scarPath -Parent) | Out-Null
}

$scar = @{
  scar_id = "integration_missing_verifier_exec"
  trigger = "agent wants to execute script without verifier"
  harm = "unsafe execution without verification guard"
  repair = "require verifier + dry-run before any execution request"
  future_rule = "BLOCK execution when verifier is missing"
  severity = "HIGH"
  tags = @("execution","verifier")
  public_safe = $true
}
$event = @{
  source = "PreflightGate"
  action_type = "script"
  target = "scripts/deploy.ps1"
  intent = "execute script directly"
  risk_signals = @("execution")
  controls = @{
    rollback = $true
    dry_run = $true
    verifier = $false
    receipt_expected = $true
    human_review = $false
  }
  boundary = "LOCAL_ONLY"
  requested_execution = $true
}

$scar | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $scarPath
$event | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $eventPath

$add = ((python .\src\aion_memory_scars.py add --input $scarPath) | Out-String) | ConvertFrom-Json
$preflight = ((python .\src\aion_preflight_gate.py --input $eventPath) | Out-String) | ConvertFrom-Json

$out = [pscustomobject]@{
  demo = "AION_PREFLIGHT_MEMORY_INTEGRATION_V1"
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  scar_add_result = $add
  preflight_result = $preflight
}
$out | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $releaseOut

$lines = @()
$lines += "# AION Preflight + Memory Integration V1 Demo Report"
$lines += ""
$lines += "- Generated UTC: " + ((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"))
$lines += "- Scar added: " + $add.scar_id
$lines += "- Decision: " + $preflight.governance_decision
$lines += "- Memory bias: " + $preflight.memory_influence.recommended_decision_bias
$lines += "- Matched scars: " + @($preflight.memory_influence.matched_scars).Count
$lines += "- Receipt: " + $preflight.receipt_path
$lines -join "`r`n" | Set-Content -LiteralPath $reportOut

Write-Host "AION_PREFLIGHT_MEMORY_INTEGRATION_V1_DEMO_OK"
