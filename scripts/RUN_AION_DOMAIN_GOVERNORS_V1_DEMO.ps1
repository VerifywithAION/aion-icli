param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_domain_governors.py"
$tempDir = Join-Path $Repo "release\_runtime\domain_demo_inputs"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name,[hashtable]$Payload)
  $p = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $p -Encoding UTF8
  $raw = & $Py $Src --input $p
  return ($raw | ConvertFrom-Json)
}

function BaseControls([bool]$verifier,[bool]$receipt,[bool]$rollback,[bool]$dry_run,[bool]$human_review){
  return @{ verifier=$verifier; receipt=$receipt; rollback=$rollback; dry_run=$dry_run; human_review=$human_review }
}

$results = @()
$results += Invoke-Case -Name "agent_unverified_execution" -Payload @{ domain="agent"; source="Agent"; action="execute tool"; risk_level="HIGH"; signals=@("execution","unsafe_claim"); controls=(BaseControls $false $true $false $true $false); requested_execution=$true }
$results += Invoke-Case -Name "wallet_signature_funds_at_risk" -Payload @{ domain="wallet"; source="WalletGuard"; action="sign tx"; risk_level="HIGH"; signals=@("signature","funds_at_risk"); controls=(BaseControls $true $true $true $true $false); requested_execution=$false }
$results += Invoke-Case -Name "security_buzzshield_flagged" -Payload @{ domain="security"; source="BuzzShield"; action="flagged finding"; risk_level="HIGH"; signals=@("flagged","exploit"); controls=(BaseControls $true $true $true $true $true); requested_execution=$false }
$results += Invoke-Case -Name "trading_no_dry_run" -Payload @{ domain="trading"; source="Manual"; action="place order"; risk_level="MEDIUM"; signals=@("execution"); controls=(BaseControls $true $true $true $false $true); requested_execution=$true }
$results += Invoke-Case -Name "quantum_missing_verifier" -Payload @{ domain="quantum"; source="AION"; action="run quantum routine"; risk_level="MEDIUM"; signals=@("execution"); controls=(BaseControls $false $true $true $true $true); requested_execution=$true }
$results += Invoke-Case -Name "physical_ai_no_human_review" -Payload @{ domain="physical_ai"; source="Manual"; action="move actuator"; risk_level="HIGH"; signals=@("execution"); controls=(BaseControls $true $true $true $true $false); requested_execution=$true }
$results += Invoke-Case -Name "unknown_domain" -Payload @{ domain="unknown"; source="Manual"; action="unknown action"; risk_level="UNKNOWN"; signals=@(); controls=(BaseControls $true $true $true $true $true); requested_execution=$false }

$releasePath = Join-Path $Repo "release\AION_DOMAIN_GOVERNORS_V1_DEMO_RESULT.json"
$reportPath = Join-Path $Repo "reports\AION_DOMAIN_GOVERNORS_V1_DEMO_REPORT.md"

@{ generated_at_utc=(Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"); engine="AION_DOMAIN_GOVERNORS_V1"; scenarios=$results } | ConvertTo-Json -Depth 20 | Set-Content -Path $releasePath -Encoding UTF8

$lines = @("# AION Domain Governors V1 Demo Report","","Generated at UTC: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))","","## Scenarios")
foreach($r in $results){
  $lines += "- governor: $($r.selected_governor)"
  $lines += "  - decision: $($r.governance_decision)"
  $lines += "  - risk: $($r.risk_level)"
}
$lines += ""
$lines += "Marker: AION_DOMAIN_GOVERNORS_V1_DEMO_OK"
$lines -join "`r`n" | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "AION_DOMAIN_GOVERNORS_V1_DEMO_OK"
