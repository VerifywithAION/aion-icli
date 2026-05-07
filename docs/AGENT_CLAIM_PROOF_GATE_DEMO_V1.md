# AGENT CLAIM PROOF GATE DEMO V1

Your agent said it was done. AION proved whether it was admissible.

## Problem

Agents can claim completion without admissible local evidence.

## Scenarios

- PASS: artifact exists and includes proof marker/verifier context.
- WARN: artifact exists but only doc-level evidence is present.
- BLOCK: claimed artifact is missing.

## Run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
```

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
```

## Why this matters

Teams need a local proof gate between claim and trust.

## Safety

- local-only
- no network
- no mutation
- no execution of user artifacts

Expected markers:

- `AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_OK`
- `AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_VERIFY_OK`
