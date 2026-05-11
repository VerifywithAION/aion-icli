# AION Preflight Gate V1

## What it does

AION Preflight Gate V1 evaluates proposed actions before execution and returns a governed decision with a local receipt.

This gate is generic and supports script actions, API call intent, wallet actions, security findings, model tool calls, file mutation requests, and unknown action classes.

## Difference from Evaluate API V1

- **Evaluate API V1**: local HTTP adapter for external scan findings (for example BuzzShield).
- **Preflight Gate V1**: local pre-execution governance gate for any proposed action payload before consequence.

## Input schema (V1)

```json
{
  "source": "AgentOrSystemName",
  "action_type": "script|api_call|wallet_action|security_finding|model_tool_call|file_mutation|unknown",
  "target": "path/url/contract/action summary",
  "intent": "what the system wants to do",
  "risk_signals": ["network", "mutation", "execution"],
  "controls": {
    "rollback": false,
    "dry_run": false,
    "verifier": false,
    "receipt_expected": true,
    "human_review": false
  },
  "boundary": "LOCAL_ONLY",
  "requested_execution": true
}
```

## Output schema (V1)

```json
{
  "gate": "AION_PREFLIGHT_GATE_V1",
  "governance_decision": "BLOCK|WARN|ALLOW|REVIEW_ONLY",
  "risk_level": "HIGH|MEDIUM|LOW|UNKNOWN",
  "reason": "...",
  "missing_controls": [],
  "required_next_step": "...",
  "boundary": "LOCAL_ONLY",
  "network": "NOT_USED",
  "mutation": "NOT_PERFORMED",
  "execution": "NOT_PERFORMED",
  "receipt_id": "...",
  "receipt_path": "receipts/preflight/...",
  "receipt_abs_path": "...",
  "receipt_written": true,
  "receipt_sha256": "...",
  "repo_root": "...",
  "input_summary": {}
}
```

## Decision logic summary

- Missing required fields -> `REVIEW_ONLY/UNKNOWN`
- Boundary not `LOCAL_ONLY`:
  - requested execution true -> `BLOCK`
  - requested execution false -> `REVIEW_ONLY`
- Requested execution true with no verifier -> `BLOCK`
- Mutation risk with no rollback -> `BLOCK`
- Execution risk with no verifier -> `BLOCK`
- Network risk with no dry-run:
  - requested execution false -> `WARN`
  - requested execution true -> `BLOCK`
- `receipt_expected=false` -> `REVIEW_ONLY`
- All controls present and low/no risk with no execution request -> `ALLOW`
- Risk with controls present -> `WARN`

## Receipt behavior

- Receipt path is repo-root anchored under `receipts/preflight/`.
- Atomic write (temp file then replace).
- Includes `receipt_abs_path`, `receipt_written`, `receipt_sha256`, and `repo_root`.
- Runtime receipts are local artifacts and are not committed.

## Run demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_PREFLIGHT_GATE_V1_DEMO.ps1
```

Expected marker:

- `AION_PREFLIGHT_GATE_V1_DEMO_OK`

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_PREFLIGHT_GATE_V1.ps1
```

Expected marker:

- `AION_PREFLIGHT_GATE_V1_VERIFY_OK`

## Safety posture

- Local-only governance path
- No external provider/API calls
- No execution of proposed action
- No mutation except local receipt writing
