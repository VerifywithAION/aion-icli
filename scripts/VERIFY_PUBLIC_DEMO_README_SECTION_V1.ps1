$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$readme = Get-Content README.md -Raw
foreach($m in @(
  'Demo: Your agent said it was done. AION proved whether it was admissible.',
  'RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1',
  'PASS',
  'WARN',
  'BLOCK',
  'agent_claim_proof_gate_results_v1.json',
  'agent_claim_proof_gate_results_v1.md',
  'VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1',
  'AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_VERIFY_OK'
)){ if($readme -notmatch [regex]::Escape($m)){ throw "README missing: $m" } }

if(-not (Test-Path docs/PUBLIC_DEMO_README_SECTION_V1.md)){ throw 'Missing docs/PUBLIC_DEMO_README_SECTION_V1.md' }
if(-not (Test-Path reports/PUBLIC_DEMO_PACKAGE_V1_REPORT.md)){ throw 'Missing reports/PUBLIC_DEMO_PACKAGE_V1_REPORT.md' }

$doc = Get-Content docs/PUBLIC_DEMO_README_SECTION_V1.md -Raw
$rep = Get-Content reports/PUBLIC_DEMO_PACKAGE_V1_REPORT.md -Raw
foreach($m in @('local','offline','no network','no mutation','no execution','enterprise','agent governance')){
  if(($doc -notmatch $m) -and ($rep -notmatch $m)){ throw "Doc/report missing: $m" }
}

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1

Write-Host 'AION_PUBLIC_DEMO_README_SECTION_V1_VERIFY_OK'
