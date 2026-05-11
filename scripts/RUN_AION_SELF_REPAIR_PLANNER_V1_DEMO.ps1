param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Planner = Join-Path $Repo "src\aion_self_repair_planner.py"
$tempDir = Join-Path $Repo "release\_runtime\self_repair_demo"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name, [hashtable]$Payload)
  $path = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $path -Encoding UTF8
  $raw = & $Py $Planner --input $path
  return ($raw | ConvertFrom-Json)
}

$cases = @()
$cases += Invoke-Case -Name "preflight_missing_controls" -Payload @{
  source = "PreflightGate"
  problem_type = "missing_controls"
  governance_decision = "BLOCK"
  risk_level = "HIGH"
  missing_controls = @("verifier","rollback","dry_run")
  contradictions = @()
  missing_artifacts = @()
  context = "preflight blocked due to missing controls"
}
$cases += Invoke-Case -Name "sentinel_contradiction" -Payload @{
  source = "Sentinel"
  problem_type = "contradiction"
  governance_decision = "BLOCK"
  risk_level = "HIGH"
  missing_controls = @()
  contradictions = @("ready_to_ship_without_verifier","ready_to_ship_without_receipt")
  missing_artifacts = @()
  context = "sentinel found claim-evidence contradiction"
}
$cases += Invoke-Case -Name "introspection_missing_proof" -Payload @{
  source = "Introspection"
  problem_type = "missing_proof_surface"
  governance_decision = "REVIEW_ONLY"
  risk_level = "MEDIUM"
  missing_controls = @()
  contradictions = @()
  missing_artifacts = @("docs/AION_EXAMPLE.md","scripts/VERIFY_AION_EXAMPLE.ps1")
  context = "proof surfaces missing"
}

$releasePath = Join-Path $Repo "release\AION_SELF_REPAIR_PLANNER_V1_DEMO_RESULT.json"
$reportPath = Join-Path $Repo "reports\AION_SELF_REPAIR_PLANNER_V1_DEMO_REPORT.md"

@{
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  planner = "AION_SELF_REPAIR_PLANNER_V1"
  scenarios = $cases
} | ConvertTo-Json -Depth 20 | Set-Content -Path $releasePath -Encoding UTF8

$lines = @(
  "# AION Self-Repair Planner V1 Demo Report",
  "",
  "Generated at UTC: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))",
  "",
  "## Scenario results"
)
foreach ($c in $cases) {
  $lines += "- decision: $($c.repair_status) / risk=$($c.risk_level)"
  $lines += "  - steps: $($c.repair_plan.Count)"
  $lines += "  - human_review: $($c.required_human_review)"
}
$lines += ""
$lines += "Marker: AION_SELF_REPAIR_PLANNER_V1_DEMO_OK"
$lines -join "`r`n" | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "AION_SELF_REPAIR_PLANNER_V1_DEMO_OK"
