$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$root = Join-Path $Repo 'demo\agent-claim-proof-gate'
$claimsDir = Join-Path $root 'claims'
$outDir = Join-Path $root 'output'
New-Item -ItemType Directory -Path $outDir -Force | Out-Null

$results = @()
$claimFiles = Get-ChildItem -LiteralPath $claimsDir -Filter *.json | Sort-Object Name

foreach($cf in $claimFiles){
  $claim = Get-Content -LiteralPath $cf.FullName -Raw | ConvertFrom-Json
  $artifactRel = [string]$claim.artifact_path
  $artifactPath = Join-Path $Repo $artifactRel
  $exists = Test-Path -LiteralPath $artifactPath

  $decision = 'WARN'
  $evidence = 'DOC_ONLY'
  $reasons = @()
  $next = 'Add verifier marker and proof evidence.'

  if(-not $exists){
    $decision = 'BLOCK'
    $evidence = 'MISSING_ARTIFACT'
    $reasons += 'artifact_missing'
    $next = 'Provide artifact path and regenerate claim with evidence.'
  }
  else {
    $text = Get-Content -LiteralPath $artifactPath -Raw
    $hasProof = ($text -match 'AION_[A-Z0-9_]+_VERIFY_OK|Proof marker|Verifier:')
    if($hasProof){
      $decision = 'PASS'
      $evidence = 'ADMISSIBLE'
      $reasons += 'artifact_present_with_proof_marker'
      $next = 'Maintain verifier linkage.'
    }
    else {
      $decision = 'WARN'
      $evidence = 'DOC_ONLY'
      $reasons += 'artifact_present_without_verifier_marker'
      $next = 'Add verifier marker and rerun proof gate.'
    }
  }

  $results += [pscustomobject]@{
    claim_id = [string]$claim.claim_id
    claim_text = [string]$claim.claim_text
    artifact_path = $artifactRel
    artifact_exists = $exists
    evidence_level = $evidence
    decision = $decision
    reasons = $reasons
    recommended_next_step = $next
    receipt_like_summary = "LOCAL_ONLY|NOT_USED|NOT_PERFORMED|NOT_PERFORMED"
  }
}

$payload = [pscustomobject]@{
  demo = 'agent_claim_proof_gate_v1'
  generated_at_utc = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
  scenarios = $results
}

$jsonOut = Join-Path $outDir 'agent_claim_proof_gate_results_v1.json'
$mdOut = Join-Path $outDir 'agent_claim_proof_gate_results_v1.md'

$payload | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonOut -Encoding UTF8

$lines = @()
$lines += '# Agent Claim vs AION Proof Gate V1 Results'
$lines += ''
$lines += 'Your agent said it was done. AION proved whether it was admissible.'
$lines += ''
$lines += '| claim_id | artifact_exists | evidence_level | decision |'
$lines += '|---|---:|---|---|'
foreach($r in $results){
  $lines += "| $($r.claim_id) | $($r.artifact_exists) | $($r.evidence_level) | $($r.decision) |"
}
$lines += ''
$lines += 'PASS / WARN / BLOCK are all represented.'
$lines | Set-Content -LiteralPath $mdOut -Encoding UTF8

Write-Host 'AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_OK'
