$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Repo = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $Repo

$releaseOut = Join-Path $Repo "release\AION_PREFLIGHT_GATE_V1_DEMO_RESULT.json"
$reportOut = Join-Path $Repo "reports\AION_PREFLIGHT_GATE_V1_DEMO_REPORT.md"

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
  results.append({
    "scenario": case["scenario"],
    "expected": case["expected"],
    "governance_decision": out["governance_decision"],
    "risk_level": out["risk_level"],
    "reason": out["reason"],
    "receipt_path": out["receipt_path"],
    "receipt_abs_path": out["receipt_abs_path"],
    "receipt_written": out["receipt_written"],
    "receipt_sha256": out["receipt_sha256"],
    "boundary": out["boundary"],
    "network": out["network"],
    "mutation": out["mutation"],
    "execution": out["execution"]
  })

print(json.dumps({"demo":"AION_PREFLIGHT_GATE_V1","results":results}, indent=2))
'@

$demoJson = (($runner | python -) | Out-String)
$demoObj = $demoJson | ConvertFrom-Json
$demoObj | Add-Member -NotePropertyName generated_at_utc -NotePropertyValue ((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"))
$demoObj | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $releaseOut

$lines = @()
$lines += "# AION Preflight Gate V1 Demo Report"
$lines += ""
$lines += "- Generated UTC: " + ((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"))
$lines += ""
$lines += "| Scenario | Expected | Actual | Risk | Receipt |"
$lines += "|---|---|---|---|---|"
foreach($r in $demoObj.results){
  $lines += "| $($r.scenario) | $($r.expected) | $($r.governance_decision) | $($r.risk_level) | $($r.receipt_path) |"
}
$lines -join "`r`n" | Set-Content -LiteralPath $reportOut

Write-Host "AION_PREFLIGHT_GATE_V1_DEMO_OK"
