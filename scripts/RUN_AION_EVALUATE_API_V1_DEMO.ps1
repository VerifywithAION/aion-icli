$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$uri = "http://127.0.0.1:8765/evaluate"
$releaseOut = Join-Path $Repo "release\AION_EVALUATE_API_V1_DEMO_RESULT.json"
$reportOut = Join-Path $Repo "reports\AION_EVALUATE_API_V1_DEMO_REPORT.md"

$payloads = @(
  @{
    name = "flagged_block"
    body = @{
      source = "BuzzShield"
      chain = "ethereum"
      contract_address = "0x1111111111111111111111111111111111111111"
      score = 32
      verdict = "FLAGGED"
      patterns = @("example_pattern")
      summary = "Critical findings from scan."
      confidence = 0.91
      recommended_action = "block"
    }
    expected = "BLOCK"
  },
  @{
    name = "watch_warn"
    body = @{
      source = "BuzzShield"
      chain = "ethereum"
      contract_address = "0x2222222222222222222222222222222222222222"
      score = 61
      verdict = "WATCH"
      patterns = @("suspicious_proxy")
      summary = "Medium risk patterns require watch."
      confidence = 0.77
      recommended_action = "watch"
    }
    expected = "WARN"
  },
  @{
    name = "clean_allow"
    body = @{
      source = "BuzzShield"
      chain = "ethereum"
      contract_address = "0x3333333333333333333333333333333333333333"
      score = 88
      verdict = "CLEAN"
      patterns = @("none")
      summary = "No critical issues."
      confidence = 0.95
      recommended_action = "allow"
    }
    expected = "ALLOW"
  }
)

$results = @()
foreach($p in $payloads){
  $json = $p.body | ConvertTo-Json -Depth 8
  $response = Invoke-RestMethod -Uri $uri -Method Post -Body $json -ContentType "application/json"
  $results += [pscustomobject]@{
    scenario = $p.name
    expected = $p.expected
    governance_decision = $response.governance_decision
    risk_level = $response.risk_level
    receipt_path = $response.receipt_path
    boundary = $response.boundary
    network = $response.network
    mutation = $response.mutation
    execution = $response.execution
    reason = $response.reason
  }
}

$payload = [pscustomobject]@{
  demo = "AION_EVALUATE_API_V1"
  endpoint = $uri
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  results = $results
}

$payload | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $releaseOut

$lines = @()
$lines += "# AION Evaluate API V1 Demo Report"
$lines += ""
$lines += "- Endpoint: ``$uri``"
$lines += "- Generated UTC: " + (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$lines += ""
$lines += "| Scenario | Expected | Actual | Risk | Receipt |"
$lines += "|---|---|---|---|---|"
foreach($r in $results){
  $lines += "| $($r.scenario) | $($r.expected) | $($r.governance_decision) | $($r.risk_level) | $($r.receipt_path) |"
}
$lines -join "`r`n" | Set-Content -LiteralPath $reportOut

Write-Host "AION_EVALUATE_API_V1_DEMO_OK"
