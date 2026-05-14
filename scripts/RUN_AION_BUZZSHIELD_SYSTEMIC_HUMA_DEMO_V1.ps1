param()
$ErrorActionPreference = "Stop"
$repo = "C:\Lab_Research\aion-icli-main"
Set-Location $repo

$server = Start-Process -FilePath "python" -ArgumentList ".\src\aion_evaluate_api.py" -PassThru -WindowStyle Hidden
try {
  $healthOk = $false
  for ($i = 0; $i -lt 30; $i++) {
    try {
      $h = Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8765/health" -TimeoutSec 2
      if ($h.status -eq "ok") { $healthOk = $true; break }
    } catch {}
    Start-Sleep -Milliseconds 300
  }
  if (-not $healthOk) { throw "Evaluate API health check failed" }

  $payload = [ordered]@{
    chain = "ethereum"
    contract_address = "0xHumaExample"
    confidence = 0.93
    recommended_action = "block"
    buzzshield_score = 21
    buzzshield_verdict = "FLAGGED"
    detected_patterns = @("state_transition_bypass", "authorization_bypass")
    finding_summary = "Huma state-transition bypass: state mutation accepted as legitimacy without validating causal authorization continuity."
  }

  $result = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8765/evaluate" -ContentType "application/json" -Body ($payload | ConvertTo-Json -Depth 8)
  if ($result.governance_decision -ne "BLOCK") { throw "Expected BLOCK decision" }
  if ($result.risk_level -ne "HIGH") { throw "Expected HIGH risk level" }
  if (-not $result.systemic_reasoning) { throw "Missing systemic_reasoning output" }
  if (-not $result.receipt_written) { throw "receipt_written not true" }

  $out = [ordered]@{
    demo = "AION_BUZZSHIELD_SYSTEMIC_HUMA_DEMO_V1"
    generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    raw_payload = $payload
    response = $result
  }
  $out | ConvertTo-Json -Depth 12 | Set-Content -Path ".\release\AION_BUZZSHIELD_SYSTEMIC_HUMA_RESULT_V1.json" -Encoding UTF8

  @(
    "# AION BuzzShield Systemic Huma Report V1",
    "",
    "Decision: $($result.governance_decision)",
    "Risk: $($result.risk_level)",
    "Systemic summary: $($result.systemic_reasoning.systemic_summary)",
    "Trust boundary collapse: $($result.systemic_reasoning.trust_boundary_collapse)",
    "Violated invariant: $($result.systemic_reasoning.violated_invariant)",
    "Next governance question: $($result.systemic_reasoning.next_governance_question)",
    "",
    "Marker: AION_BUZZSHIELD_SYSTEMIC_HUMA_DEMO_OK"
  ) -join "`n" | Set-Content -Path ".\reports\AION_BUZZSHIELD_SYSTEMIC_HUMA_REPORT_V1.md" -Encoding UTF8

  Write-Host "AION_BUZZSHIELD_SYSTEMIC_HUMA_DEMO_OK"
}
finally {
  if ($server -and -not $server.HasExited) {
    Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
  }
}
