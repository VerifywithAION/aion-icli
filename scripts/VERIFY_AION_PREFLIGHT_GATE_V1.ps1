$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$src = ".\src\aion_preflight_gate.py"
if(-not (Test-Path -LiteralPath $src)){ throw "Missing $src" }

python -m py_compile $src
if($LASTEXITCODE -ne 0){ throw "Python compile failed for $src" }

$runner = @'
import json
from src.aion_preflight_gate import evaluate_preflight

cases = [
  {
    "scenario": "unsafe_script_execute",
    "expected": "BLOCK",
    "payload": {
      "source": "AgentOrSystemName",
      "action_type": "script",
      "target": "scripts/deploy.ps1",
      "intent": "execute deployment script now",
      "risk_signals": ["mutation", "execution"],
      "controls": {"rollback": False, "dry_run": False, "verifier": False, "receipt_expected": True, "human_review": False},
      "boundary": "LOCAL_ONLY",
      "requested_execution": True
    }
  },
  {
    "scenario": "api_call_dry_run_missing",
    "expected": "WARN",
    "payload": {
      "source": "AgentOrSystemName",
      "action_type": "api_call",
      "target": "local api request",
      "intent": "stage api call without execute",
      "risk_signals": ["network"],
      "controls": {"rollback": True, "dry_run": False, "verifier": True, "receipt_expected": True, "human_review": False},
      "boundary": "LOCAL_ONLY",
      "requested_execution": False
    }
  },
  {
    "scenario": "safe_dry_run_verified",
    "expected": "ALLOW",
    "payload": {
      "source": "AgentOrSystemName",
      "action_type": "script",
      "target": "scripts/check.ps1",
      "intent": "review and dry-run only",
      "risk_signals": [],
      "controls": {"rollback": True, "dry_run": True, "verifier": True, "receipt_expected": True, "human_review": True},
      "boundary": "LOCAL_ONLY",
      "requested_execution": False
    }
  }
]

results = []
for case in cases:
  out = evaluate_preflight(case["payload"])
  out["scenario"] = case["scenario"]
  out["expected"] = case["expected"]
  results.append(out)
print(json.dumps(results, indent=2))
'@

$results = (($runner | python -) | Out-String) | ConvertFrom-Json

foreach($r in $results){
  if($r.boundary -ne "LOCAL_ONLY"){ throw "boundary mismatch in $($r.scenario)" }
  if($r.network -ne "NOT_USED"){ throw "network mismatch in $($r.scenario)" }
  if($r.mutation -ne "NOT_PERFORMED"){ throw "mutation mismatch in $($r.scenario)" }
  if($r.execution -ne "NOT_PERFORMED"){ throw "execution mismatch in $($r.scenario)" }
  if(-not $r.receipt_path){ throw "receipt_path missing in $($r.scenario)" }
  if(-not $r.receipt_abs_path){ throw "receipt_abs_path missing in $($r.scenario)" }
  if($r.receipt_written -ne $true){ throw "receipt_written false in $($r.scenario)" }
  if(-not $r.receipt_sha256){ throw "receipt_sha256 missing in $($r.scenario)" }
  if(-not (Test-Path -LiteralPath (Join-Path $Repo ($r.receipt_path -replace '/', '\')))){ throw "receipt_path file missing in $($r.scenario)" }
  if(-not (Test-Path -LiteralPath ([string]$r.receipt_abs_path))){ throw "receipt_abs_path file missing in $($r.scenario)" }
}

$unsafe = $results | Where-Object { $_.scenario -eq 'unsafe_script_execute' } | Select-Object -First 1
$api = $results | Where-Object { $_.scenario -eq 'api_call_dry_run_missing' } | Select-Object -First 1
$safe = $results | Where-Object { $_.scenario -eq 'safe_dry_run_verified' } | Select-Object -First 1

if(-not $unsafe -or $unsafe.governance_decision -ne "BLOCK"){ throw "unsafe_script_execute must BLOCK" }
if(-not $api -or $api.governance_decision -ne "WARN"){ throw "api_call_dry_run_missing must WARN" }
if(-not $safe -or $safe.governance_decision -ne "ALLOW"){ throw "safe_dry_run_verified must ALLOW" }

if(Test-Path -LiteralPath (Join-Path $Repo "receipts\preflight")){
  Remove-Item -LiteralPath (Join-Path $Repo "receipts\preflight") -Recurse -Force
}

Write-Host "AION_PREFLIGHT_GATE_V1_VERIFY_OK"
