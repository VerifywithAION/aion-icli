# Public Demo Fresh Clone Acceptance V1

## Purpose

Prove a brand-new user can fresh-clone the public repo and run the Agent Claim vs AION Proof Gate demo offline with deterministic PASS/WARN/BLOCK outputs.

## Fresh-clone test path

`C:\Lab_Research\aion-icli-public-demo-fresh-clone-test`

## Commands tested

```powershell
git clone https://github.com/VerifywithAION/aion-icli.git C:\Lab_Research\aion-icli-public-demo-fresh-clone-test
cd C:\Lab_Research\aion-icli-public-demo-fresh-clone-test
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
.\bin\aion.cmd "agent claim proof gate"
.\bin\aion.cmd "sentinel state"
```

## Expected outputs

- `demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.json`
- `demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.md`
- PASS/WARN/BLOCK decisions present in JSON.

## Expected marker

- `AION_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1_PASS`

## Why this matters

This confirms that a new user can clone the repo and reproduce the public wedge demo without hidden setup, provider calls, or network-dependent execution paths.
