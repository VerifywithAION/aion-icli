# PUBLIC DEMO README SECTION V1

This demo proves that an agent claim is not trusted by default.
AION checks claim-to-artifact evidence and classifies admissibility as PASS, WARN, or BLOCK.

## Run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
```

## Interpret decisions

- PASS: claim has admissible local evidence.
- WARN: claim has partial/doc-only evidence and needs proof hardening.
- BLOCK: claim references missing/non-admissible evidence.

## Enterprise mapping

This maps to enterprise agent governance: claimed completion must be backed by local auditable proof before trust or release.

## Why local/offline matters

Local/offline proof avoids dependency on provider reachability and preserves deterministic admissibility checks.

## What it does NOT claim

- no autonomous execution
- no provider intelligence claim
- no production completion claim

## Boundaries

- no network
- no mutation
- no execution of user artifacts

Expected marker:

`AION_PUBLIC_DEMO_README_SECTION_V1_VERIFY_OK`
