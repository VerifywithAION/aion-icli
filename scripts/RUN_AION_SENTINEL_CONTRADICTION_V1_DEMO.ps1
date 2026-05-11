param()

$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"

$tempDir = Join-Path $Repo "release\_runtime\sentinel_demo"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Scenario {
  param(
    [string]$Name,
    [hashtable]$Payload
  )
  $inputPath = Join-Path $tempDir ("{0}.json" -f $Name)
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $inputPath -Encoding UTF8
  $raw = & $Py (Join-Path $Repo "src\aion_sentinel_contradiction.py") --input $inputPath
  return ($raw | ConvertFrom-Json)
}

$results = @()

$results += Invoke-Scenario -Name "ready_to_ship_without_proof" -Payload @{
  claim = "ready_to_ship"
  artifact = "scripts/deploy.ps1"
  evidence = @{ verifier = $false; receipt = $false; rollback = $false; dry_run = $false; human_review = $false }
  risk = @{ risk_level = "HIGH"; decision = "REVIEW_ONLY"; missing_controls = @("verifier", "rollback", "dry_run") }
  context = "Claim says ready_to_ship but proof controls are absent"
}

$results += Invoke-Scenario -Name "safe_to_execute_but_blocked" -Payload @{
  claim = "safe_to_execute"
  artifact = "scripts/execute.ps1"
  evidence = @{ verifier = $true; receipt = $true; rollback = $true; dry_run = $true; human_review = $true }
  risk = @{ risk_level = "HIGH"; decision = "BLOCK"; missing_controls = @() }
  context = "Claim says safe_to_execute while decision is BLOCK"
}

$results += Invoke-Scenario -Name "consistent_low_risk" -Payload @{
  claim = "allowed"
  artifact = "docs/policy.md"
  evidence = @{ verifier = $true; receipt = $true; rollback = $true; dry_run = $true; human_review = $true }
  risk = @{ risk_level = "LOW"; decision = "ALLOW"; missing_controls = @() }
  context = "Claim aligns with low-risk evidence"
}

$releasePath = Join-Path $Repo "release\AION_SENTINEL_CONTRADICTION_V1_DEMO_RESULT.json"
$reportPath = Join-Path $Repo "reports\AION_SENTINEL_CONTRADICTION_V1_DEMO_REPORT.md"

@{
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  engine = "AION_SENTINEL_CONTRADICTION_V1"
  scenarios = $results
} | ConvertTo-Json -Depth 15 | Set-Content -Path $releasePath -Encoding UTF8

$md = @(
  "# AION Sentinel + Contradiction V1 Demo Report"
  ""
  "Generated at UTC: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))"
  ""
  "## Scenarios"
)

foreach ($r in $results) {
  $md += "- claim: $($r.input_summary.claim)"
  $md += "  - consistency_status: $($r.consistency_status)"
  $md += "  - severity: $($r.severity)"
  $md += "  - governance_decision: $($r.governance_decision)"
  $md += "  - contradictions: $((@($r.contradictions) -join ', '))"
}

$md += ""
$md += "Marker: AION_SENTINEL_CONTRADICTION_V1_DEMO_OK"
$md -join "`r`n" | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "AION_SENTINEL_CONTRADICTION_V1_DEMO_OK"
