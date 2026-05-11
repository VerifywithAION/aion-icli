param()
$ErrorActionPreference = "Stop"
$Repo = "C:\Lab_Research\aion-live-demo"
$Py = "python"
$Src = Join-Path $Repo "src\aion_creativity_intuition.py"
$tempDir = Join-Path $Repo "release\_runtime\intuition_demo_inputs"
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

function Invoke-Case {
  param([string]$Name,[hashtable]$Payload)
  $p = Join-Path $tempDir ("$Name.json")
  $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $p -Encoding UTF8
  $raw = & $Py $Src --input $p
  return ($raw | ConvertFrom-Json)
}

$results = @()
$results += Invoke-Case -Name "wallet_funds_at_risk" -Payload @{
  source="DomainGovernor"; context="wallet action with contradictory signals"; signals=@{ contradictions=1; memory_matches=2; missing_controls=@("verifier","rollback"); risk_signals=@("signature","funds_at_risk"); domain="wallet"; governance_decision="BLOCK"; evidence_complete=$false; proof_graph_missing_count=0 }
}
$results += Invoke-Case -Name "agent_claim_weak_evidence" -Payload @{
  source="Sentinel"; context="agent claim with weak evidence"; signals=@{ contradictions=1; memory_matches=1; missing_controls=@("verifier"); risk_signals=@("unsafe_claim"); domain="agent"; governance_decision="REVIEW_ONLY"; evidence_complete=$false; proof_graph_missing_count=0 }
}
$results += Invoke-Case -Name "clean_low_signal" -Payload @{
  source="Manual"; context="clean signal baseline"; signals=@{ contradictions=0; memory_matches=0; missing_controls=@(); risk_signals=@(); domain="unknown"; governance_decision="ALLOW"; evidence_complete=$true; proof_graph_missing_count=0 }
}

$releasePath = Join-Path $Repo "release\AION_CREATIVITY_INTUITION_V1_DEMO_RESULT.json"
$reportPath = Join-Path $Repo "reports\AION_CREATIVITY_INTUITION_V1_DEMO_REPORT.md"

@{ generated_at_utc=(Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"); engine="AION_CREATIVITY_INTUITION_V1"; scenarios=$results } | ConvertTo-Json -Depth 20 | Set-Content -Path $releasePath -Encoding UTF8

$lines = @("# AION Creativity + Intuition V1 Demo Report","","Generated at UTC: $((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))","","## Scenarios")
foreach($r in $results){
  $lines += "- class: $($r.intuition_class)"
  $lines += "  - score: $($r.intuition_score)"
  $lines += "  - heuristic_not_truth: $($r.heuristic_not_truth)"
}
$lines += ""
$lines += "Marker: AION_CREATIVITY_INTUITION_V1_DEMO_OK"
$lines -join "`r`n" | Set-Content -Path $reportPath -Encoding UTF8

Write-Host "AION_CREATIVITY_INTUITION_V1_DEMO_OK"
