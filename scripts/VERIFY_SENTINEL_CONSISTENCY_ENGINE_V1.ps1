$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

Write-Host "AION Sentinel Consistency Engine V1 verifier"

$required = @(
  ".aion_public/sentinel/sentinel_state_v1.json",
  ".aion_public/sentinel/sentinel_summary_v1.md",
  ".aion_public/sentinel/sentinel_latest_v1.json",
  "docs/SENTINEL_CONSISTENCY_ENGINE_V1.md",
  "src/aion_cli_entry.py"
)
foreach($p in $required){ if(-not (Test-Path -LiteralPath $p)){ throw "Missing required artifact: $p" } }

python -m py_compile src/aion_cli_entry.py

$state = Get-Content .aion_public/sentinel/sentinel_state_v1.json -Raw | ConvertFrom-Json
$latest = Get-Content .aion_public/sentinel/sentinel_latest_v1.json -Raw | ConvertFrom-Json
if($state.sentinel_state -notin @('HEALTHY','DEGRADED_ACCEPTED_CAVEAT','DEGRADED_NEEDS_REPAIR','INCONSISTENT','BLOCKED','UNKNOWN')){
  throw 'Invalid sentinel_state'
}
if(-not $state.next_required_action){ throw 'Missing next_required_action' }
if($state.sentinel_state -eq 'BLOCKED' -and ([int]$state.critical_contradictions -le 0)){ throw 'False BLOCKED sentinel state' }

$inputs = @(
  'sentinel state',
  'is AION healthy?',
  'is AION blocked?',
  'what is the current status?',
  'what is the next required action?',
  'diagnostics on',
  'sentinel state',
  'diagnostics off',
  'exit'
) -join "`n"

$out = $inputs | python src/aion_cli_entry.py
$outText = ($out | Out-String)

if($outText -notmatch 'AION_SENTINEL_STATE|sentinel state|Sentinel'){ throw 'Missing sentinel normal output' }
if($outText -notmatch 'Proof:'){ throw 'Missing proof footer in normal output' }
if($outText -notmatch 'next action|Next action|next required action'){ throw 'Missing next action output' }
if($outText -notmatch 'Sentinel used'){ throw 'Missing diagnostics sentinel section' }
if($outText -notmatch 'Sentinel state'){ throw 'Missing diagnostics sentinel state' }
if($outText -notmatch 'Blocking'){ throw 'Missing diagnostics blocking field' }
if($outText -notmatch 'Accepted caveats'){ throw 'Missing diagnostics accepted caveats field' }
if($outText -notmatch 'Open contradictions'){ throw 'Missing diagnostics open contradictions field' }
if($outText -notmatch 'Repair items'){ throw 'Missing diagnostics repair items field' }
if($outText -notmatch 'State path'){ throw 'Missing diagnostics state path field' }

if(-not (Test-Path -LiteralPath 'receipts/local/aion_cli_receipt_v1.json')){ throw 'Missing receipt after sentinel prompts' }
$receipt = Get-Content receipts/local/aion_cli_receipt_v1.json -Raw | ConvertFrom-Json
if(-not $receipt.sentinel_used){ throw 'receipt.sentinel_used not true' }
if(-not $receipt.sentinel_state){ throw 'receipt.sentinel_state missing' }
if(-not $receipt.recommended_next_action){ throw 'receipt.recommended_next_action missing' }
if($receipt.boundary -ne 'LOCAL_ONLY'){ throw 'receipt boundary mismatch' }
if($receipt.network -ne 'NOT_USED'){ throw 'receipt network mismatch' }
if($receipt.mutation -ne 'NOT_PERFORMED'){ throw 'receipt mutation mismatch' }
if($receipt.execution -ne 'NOT_PERFORMED'){ throw 'receipt execution mismatch' }

Write-Host 'AION_SENTINEL_CONSISTENCY_ENGINE_V1_VERIFY_OK'
