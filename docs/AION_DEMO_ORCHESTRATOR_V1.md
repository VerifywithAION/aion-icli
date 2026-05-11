# AION Demo Orchestrator V1

AION Demo Orchestrator V1 provides a single deterministic command that proves the full governance chain end-to-end.

## What it proves

1. A claim enters governance.
2. Preflight evaluates before execution.
3. Missing controls and risk are surfaced.
4. Memory scars bias decision toward safer posture.
5. Sentinel detects claim/evidence contradiction.
6. Self-Repair produces plan-only remediation.
7. Self-Patching Sandbox creates rollback-backed patch proof without production mutation.
8. Domain Governors apply domain-specific policy.
9. Creativity + Intuition emits heuristic next actions (not truth).
10. Introspection updates living proof graph.
11. Receipts and reports persist auditable evidence.

## Why no live model/GPU is needed

This demo uses deterministic local modules and governance logic. It does not call external providers or model APIs.

## Public-safe and deterministic boundaries

- Local-only
- No external network/provider calls
- No governed action execution
- No production mutation
- Runtime mutation limited to reports/results/receipts

## Run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_DEMO_ORCHESTRATOR_V1.ps1
```

Expected terminal summary:

- AION DEMO ORCHESTRATOR V1
- Preflight: BLOCK
- Memory: BLOCK
- Sentinel: CONTRADICTION
- Self-Repair: PLAN_ONLY
- Sandbox: SANDBOXED_ONLY
- Domain Governor: BLOCK
- Intuition: CRITICAL_SIGNAL
- Introspection: GRAPH_WRITTEN
- Final: PASS

Expected marker:

- `AION_DEMO_ORCHESTRATOR_V1_OK`

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_DEMO_ORCHESTRATOR_V1.ps1
```

Expected marker:

- `AION_DEMO_ORCHESTRATOR_V1_VERIFY_OK`

## Evidence outputs

- `release/AION_DEMO_ORCHESTRATOR_V1_RESULT.json`
- `reports/AION_DEMO_ORCHESTRATOR_V1_REPORT.md`
- living proof graph updates:
  - `release/AION_LIVING_PROOF_GRAPH_V1.json`
  - `reports/AION_LIVING_PROOF_GRAPH_V1.md`

## Demo recording guidance

1. Start from clean git status.
2. Run orchestrator script and show terminal summary.
3. Show generated JSON + report files.
4. Run verifier and show marker.
5. Show final `git status --short` clean state after receipt/runtime cleanup.
