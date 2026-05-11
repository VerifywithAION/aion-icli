# AION Sentinel + Contradiction V1

AION Sentinel + Contradiction Engine V1 checks whether a claim is consistent with local evidence, controls, and risk posture before trust is granted.

## What it does

- Detects claim/evidence mismatches such as `ready_to_ship` without verifier/receipt.
- Produces a governed consistency outcome: `CONTRADICTION`, `INCOMPLETE_EVIDENCE`, or `CONSISTENT`.
- Maps consistency severity to governance decision: `BLOCK`, `REVIEW_ONLY`, or `ALLOW`.
- Writes local receipt output under `receipts/sentinel/` with repo-root anchored paths.

## Input schema (V1)

```json
{
  "claim": "ready_to_ship|safe_to_execute|allowed|clean|unknown",
  "artifact": "path-or-summary",
  "evidence": {
    "verifier": false,
    "receipt": false,
    "rollback": false,
    "dry_run": false,
    "human_review": false
  },
  "risk": {
    "risk_level": "HIGH|MEDIUM|LOW|UNKNOWN",
    "decision": "BLOCK|WARN|ALLOW|REVIEW_ONLY",
    "missing_controls": ["verifier", "rollback"]
  },
  "context": "short public-safe context"
}
```

## Output schema (V1)

- `engine`: `AION_SENTINEL_CONTRADICTION_V1`
- `consistency_status`: `CONTRADICTION|INCOMPLETE_EVIDENCE|CONSISTENT`
- `severity`: `HIGH|MEDIUM|LOW|UNKNOWN`
- `contradictions`: array of matched contradiction rules
- `required_next_step`: repair guidance
- `governance_decision`: `BLOCK|WARN|ALLOW|REVIEW_ONLY`
- `boundary/network/mutation/execution`: fixed public-safe posture
- receipt fields: `receipt_id`, `receipt_path`, `receipt_abs_path`, `receipt_written`, `receipt_sha256`, `repo_root`

## Core contradiction rules

- `ready_to_ship` + `verifier=false` => `CONTRADICTION/HIGH`
- `ready_to_ship` + `receipt=false` => `CONTRADICTION/HIGH`
- `safe_to_execute` + `risk.decision=BLOCK` => `CONTRADICTION/HIGH`
- `allowed` + `risk.decision=REVIEW_ONLY` => `CONTRADICTION/MEDIUM`
- `risk_level=HIGH` + `claim=clean` => `CONTRADICTION/HIGH`
- `missing_controls` non-empty + `claim=ready_to_ship` => `CONTRADICTION/HIGH`
- no contradiction but incomplete evidence => `INCOMPLETE_EVIDENCE/MEDIUM`
- aligned claim + low risk => `CONSISTENT/LOW`

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_SENTINEL_CONTRADICTION_V1_DEMO.ps1
```

Expected marker:

- `AION_SENTINEL_CONTRADICTION_V1_DEMO_OK`

## Verifier

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_SENTINEL_CONTRADICTION_V1.ps1
```

Expected marker:

- `AION_SENTINEL_CONTRADICTION_V1_VERIFY_OK`

## Safety posture

- Local-only evaluation (`LOCAL_ONLY`)
- No provider calls
- No external network calls
- No execution of proposed actions
- Mutation limited to local receipt files
