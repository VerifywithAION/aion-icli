# Public Demo Fresh Clone Acceptance V1 Report

Current HEAD: f06d7af

## Markers

- Demo verifier marker: AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_VERIFY_OK
- Fresh clone marker: AION_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1_PASS

## Demo command

`powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
`

## Fresh-clone verifier command

`powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1.ps1
`

## PASS/WARN/BLOCK summary

The demo proves all three outcomes from local evidence checks:

- PASS for claim backed by present artifact and admissible evidence.
- WARN for claim with documentation but incomplete proof/verifier strength.
- BLOCK for claim referencing a missing artifact.

## Output paths

- demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.json
- demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.md

## Boundary

- local/offline execution path only
- no provider/API calls
- no network execution in demo logic
- no mutation or autonomous execution claims
