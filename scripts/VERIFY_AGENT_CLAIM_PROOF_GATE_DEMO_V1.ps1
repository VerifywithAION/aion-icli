$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1

$jsonOut = 'demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.json'
$mdOut = 'demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.md'

if(-not (Test-Path -LiteralPath $jsonOut)){ throw 'Missing demo JSON output' }
if(-not (Test-Path -LiteralPath $mdOut)){ throw 'Missing demo markdown output' }

$data = Get-Content -LiteralPath $jsonOut -Raw | ConvertFrom-Json
$scenarios = @($data.scenarios)
if($scenarios.Count -ne 3){ throw 'Expected 3 scenarios' }

$pass = $scenarios | Where-Object { $_.claim_id -eq 'claim_pass' } | Select-Object -First 1
$warn = $scenarios | Where-Object { $_.claim_id -eq 'claim_warn' } | Select-Object -First 1
$block = $scenarios | Where-Object { $_.claim_id -eq 'claim_block' } | Select-Object -First 1

if(-not $pass -or $pass.decision -notin @('PASS','ADMISSIBLE')){ throw 'PASS scenario invalid' }
if(-not $warn -or $warn.decision -notin @('WARN','REVIEW_ONLY')){ throw 'WARN scenario invalid' }
if(-not $block -or $block.decision -notin @('BLOCK','NOT_ADMISSIBLE')){ throw 'BLOCK scenario invalid' }
if($block.artifact_exists -ne $false){ throw 'Missing artifact scenario not detected' }

$md = Get-Content -LiteralPath $mdOut -Raw
foreach($k in @('Your agent said it was done','AION proved','PASS','WARN','BLOCK')){
  if($md -notmatch [regex]::Escape($k)){ throw "Markdown missing: $k" }
}

$cliOut = cmd.exe /d /c ".\bin\aion.cmd \"agent claim proof gate\"" 2>&1 | Out-String
if($cliOut -notmatch 'local|offline|PASS|WARN|BLOCK|proof gate'){ throw 'CLI did not mention proof gate behavior' }

Write-Host 'AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_VERIFY_OK'
