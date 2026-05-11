# AION Self-Repair Planner V1

AION Self-Repair Planner V1 creates governed repair plans for missing controls, contradictions, incomplete evidence, and proof gaps.

## What it does

- Produces bounded, plan-only remediation steps.
- Explains how to move from blocked/review-only state to admissibility recheck.
- Writes local receipts under `receipts/self_repair/`.

## What it refuses to do

- It does not execute target actions.
- It does not patch target artifacts directly.
- It does not claim readiness without verifier-backed proof.

## Input schema (V1)

```json
{
  "source": "PreflightGate|Sentinel|Introspection|EvaluateAPI|Manual",
  "problem_type": "missing_controls|contradiction|incomplete_evidence|missing_proof_surface|receipt_failure|unknown",
  "governance_decision": "BLOCK|WARN|REVIEW_ONLY|ALLOW",
  "risk_level": "HIGH|MEDIUM|LOW|UNKNOWN",
  "missing_controls": ["verifier", "rollback", "dry_run"],
  "contradictions": ["ready_to_ship_without_verifier"],
  "missing_artifacts": ["docs/example.md", "scripts/VERIFY_EXAMPLE.ps1"],
  "context": "public-safe summary"
}
```

## Output schema (V1)

- `planner`: `AION_SELF_REPAIR_PLANNER_V1`
- `repair_status`: `PLAN_ONLY`
- `repair_plan`: ordered steps with rationale and verification markers
- `required_human_review`: true for high-risk or blocked/review-only contexts
- `admissibility_after_repair`: `RECHECK_REQUIRED`
- `forbidden_actions`: safety guardrails
- boundary/network/mutation/execution posture
- receipt metadata: `receipt_path`, `receipt_abs_path`, `receipt_written`, `receipt_sha256`, `repo_root`

## Repair logic highlights

- Missing verifier -> propose verifier script + marker.
- Missing rollback -> propose rollback procedure.
- Missing dry-run -> propose dry-run path.
- Contradiction -> propose claim downgrade + evidence requirement.
- Incomplete evidence -> propose evidence capture path.
- Missing proof surface -> propose docs/report/release/verifier additions.
- Receipt failure -> propose root-anchored atomic receipt + sha256 hardening.

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_SELF_REPAIR_PLANNER_V1_DEMO.ps1
```

Expected marker:

- `AION_SELF_REPAIR_PLANNER_V1_DEMO_OK`

## Verifier

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_SELF_REPAIR_PLANNER_V1.ps1
```

Expected marker:

- `AION_SELF_REPAIR_PLANNER_V1_VERIFY_OK`

## Public-safe posture

- Local-only
- No provider calls
- No external network calls
- No action execution
- No mutation of target artifacts
- Receipts only for planning operations
