$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$clonePath = "C:\Lab_Research\aion-icli-public-demo-fresh-clone-test"
$repoUrl = "https://github.com/VerifywithAION/aion-icli.git"

Write-Host "AION Public Demo Fresh Clone Acceptance V1"

if (Test-Path -LiteralPath $clonePath) {
  Remove-Item -LiteralPath $clonePath -Recurse -Force
}

git clone $repoUrl $clonePath | Out-Null
if ($LASTEXITCODE -ne 0) { throw "git clone failed" }

Push-Location $clonePath
try {
  $head = (git rev-parse HEAD).Trim()
  $originMain = (git rev-parse origin/main).Trim()
  if ([string]::IsNullOrWhiteSpace($head) -or [string]::IsNullOrWhiteSpace($originMain)) {
    throw "Unable to resolve clone HEAD or origin/main"
  }
  if ($head -ne $originMain) {
    throw "Clone HEAD does not match origin/main"
  }

  powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
  if ($LASTEXITCODE -ne 0) { throw "install.ps1 failed" }

  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
  if ($LASTEXITCODE -ne 0) { throw "RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1 failed" }

  powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
  if ($LASTEXITCODE -ne 0) { throw "VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1 failed" }

  $jsonPath = "demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.json"
  $mdPath = "demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.md"
  if (-not (Test-Path -LiteralPath $jsonPath)) { throw "Missing demo output JSON" }
  if (-not (Test-Path -LiteralPath $mdPath)) { throw "Missing demo output markdown" }

  $json = Get-Content -LiteralPath $jsonPath -Raw | ConvertFrom-Json
  $scenarios = @($json.scenarios)
  if ($scenarios.Count -lt 3) { throw "Expected at least 3 scenarios in demo output" }

  $decisions = @($scenarios | ForEach-Object { $_.decision })
  if (-not ($decisions -contains "PASS")) { throw "PASS decision missing" }
  if (-not ($decisions -contains "WARN")) { throw "WARN decision missing" }
  if (-not ($decisions -contains "BLOCK")) { throw "BLOCK decision missing" }

  $aionDemo = & .\bin\aion.cmd "agent claim proof gate"
  if ($LASTEXITCODE -ne 0) { throw "aion.cmd demo prompt failed" }
  $aionSentinel = & .\bin\aion.cmd "sentinel state"
  if ($LASTEXITCODE -ne 0) { throw "aion.cmd sentinel prompt failed" }
  if (($aionDemo -join "`n") -notmatch 'local|offline|PASS|WARN|BLOCK') { throw "Demo prompt output missing expected proof-gate language" }
  if (($aionSentinel -join "`n") -notmatch 'SENTINEL|health|DEGRADED|HEALTHY|BLOCKED|UNKNOWN|INCONSISTENT') { throw "Sentinel output missing expected state language" }

  if (Test-Path -LiteralPath ".\receipts\local") {
    Remove-Item -LiteralPath ".\receipts\local" -Recurse -Force
  }

  $restoreCandidates = @(
    '.aion_public/contradictions/contradiction_index_v1.json',
    '.aion_public/contradictions/contradiction_latest_v1.json',
    '.aion_public/contradictions/contradiction_summary_v1.md',
    '.aion_public/self_repair/self_repair_latest_v1.json',
    '.aion_public/self_repair/self_repair_plan_v1.json',
    '.aion_public/self_repair/self_repair_summary_v1.md',
    '.aion_public/sentinel/sentinel_latest_v1.json',
    '.aion_public/sentinel/sentinel_state_v1.json',
    '.aion_public/sentinel/sentinel_summary_v1.md',
    'demo/agent-claim-proof-gate/output/agent_claim_proof_gate_results_v1.json',
    'demo/agent-claim-proof-gate/output/agent_claim_proof_gate_results_v1.md'
  )
  foreach ($item in $restoreCandidates) {
    if (Test-Path -LiteralPath $item) {
      git restore -- $item | Out-Null
    }
  }

  $cloneStatus = git status --short
  if ($cloneStatus) {
    throw "Clone repo dirty after cleanup:`n$($cloneStatus -join "`n")"
  }

  Write-Host "AION_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1_PASS"
}
finally {
  Pop-Location
}