# AION ICLI REALITY / NO-DRIFT SCAN V1

## Git

Branch: main
HEAD: 6cb3968

## Git Log

6cb3968 (HEAD -> main, origin/main) Add AION ICLI proof demo pack v1 49b27b5 Add AION ICLI release evidence index v1 ad7037b Fix offline bundle verifier historical head mode 77d9a4f Add AION public demo release pack v1 a4117e6 Add public demo fresh clone acceptance v1 f06d7af Add public demo README section v1 f04f6f6 Add AION agent claim proof gate demo v1 fdff15a (tag: v1.1.0-offline-icli) Package AION ICLI offline bundle v1.1.0 5532ae2 Lock regenerated Sentinel V1 state outputs 3368809 Wire AION ICLI sentinel consistency engine v1 1a9f7ab Wire AION ICLI self-repair planner v1 705d5d8 Wire AION ICLI contradiction engine v1 4148449 Wire AION ICLI introspection gate v1 e8e0ccd Wire AION ICLI evidence engine v1 0cf30c0 Wire AION ICLI living proof graph v1 bcd5e2b Wire AION ICLI artifact inspection runner v1 df4ffaa Sync AION ICLI roadmap and wiring after memory scar engine v1 8183fc6 Seed AION ICLI memory scar engine v1 be6254c Fix AION ICLI governance brain integration v1 5fe1c5d Wire AION ICLI governance brain adapter v1

## Git Status

 M release/AION_ICLI_RELEASE_EVIDENCE_INDEX_V1.json  M reports/AION_ICLI_RELEASE_EVIDENCE_INDEX_V1_REPORT.md  M src/aion_cli_entry.py ?? scripts/VERIFY_AION_ICLI_REAL_RUNTIME_V1.ps1

## File Presence

[FOUND] README.md
[FOUND] src\aion_cli_entry.py
[FOUND] bin\aion.cmd
[FOUND] docs\USER_GUIDE_V1.md
[FOUND] docs\CAPABILITY_ROUTER_V1.md
[FOUND] docs\VOICE_LAYER_V1.md
[FOUND] docs\ADAPTIVE_REASONING_LAYER_V1.md
[FOUND] docs\GOVERNANCE_BRAIN_ADAPTER_V1.md
[FOUND] docs\GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.md
[FOUND] docs\MEMORY_SCAR_ENGINE_V1.md
[FOUND] docs\ARTIFACT_INSPECTION_RUNNER_V1.md
[FOUND] docs\AION_ICLI_ROADMAP_STATE_V1.md
[FOUND] docs\AION_ICLI_SYSTEM_WIRING_REPORT_V1.md
[FOUND] .aion_public\roadmap\roadmap_state_v1.json
[FOUND] .aion_public\wiring\system_wiring_v1.json

## Verifier Presence

[FOUND] scripts\VERIFY_CAPABILITY_ROUTER_V1.ps1
[FOUND] scripts\VERIFY_VOICE_LAYER_V1.ps1
[FOUND] scripts\VERIFY_ADAPTIVE_REASONING_LAYER_V1.ps1
[FOUND] scripts\VERIFY_GOVERNANCE_BRAIN_ADAPTER_V1.ps1
[FOUND] scripts\VERIFY_GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.ps1
[FOUND] scripts\VERIFY_MEMORY_SCAR_ENGINE_V1.ps1
[FOUND] scripts\VERIFY_ARTIFACT_INSPECTION_RUNNER_V1.ps1
[FOUND] scripts\VERIFY_AION_ICLI_ROADMAP_AND_WIRING_V1.ps1
[FOUND] scripts\VERIFY_LIVING_PROOF_GRAPH_V1.ps1
[FOUND] scripts\VERIFY_EVIDENCE_ENGINE_V1.ps1
[FOUND] scripts\VERIFY_INTROSPECTION_GATE_V1.ps1
[FOUND] scripts\VERIFY_CONTRADICTION_ENGINE_V1.ps1
[FOUND] scripts\VERIFY_SELF_REPAIR_PLANNER_V1.ps1
[FOUND] scripts\VERIFY_SENTINEL_CONSISTENCY_ENGINE_V1.ps1

## Runtime Wiring Signals in src/aion_cli_entry.py

[RUNTIME_HAS] Governance Brain
[RUNTIME_HAS] governance_brain
[RUNTIME_HAS] Memory Scar
[RUNTIME_HAS] memory_scar
[RUNTIME_HAS] Artifact Inspection
[RUNTIME_HAS] artifact_inspection
[RUNTIME_HAS] Living Proof Graph
[RUNTIME_HAS] diagnostics
[RUNTIME_HAS] No artifact
[RUNTIME_MISSING] Capability Router

## Roadmap JSON If Present

{
  "roadmap_type": "aion_icli_public_safe_roadmap_state_v1",
  "generated_at_utc": "2026-05-07T19:18:32Z",
  "current_head": "a4117e6",
  "latest_completed_layer": "Public Demo Release Pack V1",
  "latest_completed_commit": "a4117e6",
  "next_build_pointer": "Public Release v1.2.0 Demo Gate",
  "completed_layers": [
    "Public Release V1",
    "Interactive Mode V1",
    "Capability Router V1",
    "Voice Layer V1",
    "Adaptive Reasoning Layer V1",
    "Governance Brain Adapter V1",
    "Governance Brain Integration Fix V1",
    "Memory Scar Engine V1",
    "Artifact Inspection Runner V1",
    "Living Proof Graph V1",
    "Evidence Engine V1",
    "Introspection Gate V1",
    "Contradiction Engine V1",
    "Self-Repair Planner V1",
    "Sentinel Consistency Engine V1",
    "Offline AION CLI Bundle V1.1.0",
    "Public Demo: Agent Claim vs AION Proof Gate V1",
    "Public Demo Package + README Demo Section V1",
    "Public Demo Fresh Clone Acceptance V1",
    "Public Demo Release Pack V1"
  ],
  "next_builds": [
    "Public Release v1.2.0 Demo Gate"
  ],
  "public_release_caveat": "GitHub Release v1.0.0-public-icli points to an earlier package state; main now contains newer intelligence layers not yet rebuilt into a new ZIP release.",
  "end_to_end_wiring_rule": "A layer is complete only if docs, runtime behavior, verifier coverage, roadmap state, and public-safe boundaries all align.",
  "no_drift_rule": "No drift: no lock claim without executable verifier evidence and synchronized roadmap+wiring artifacts."
}


## README Opening

# ⚡ AION ICLI — Governed Command Line Intelligence

<p align="center">
  <strong>Governed Execution · Receipts · Offline Replay</strong>
</p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/build-passing-brightgreen">
  <img alt="Release" src="https://img.shields.io/badge/release-public%20v1-blue">
  <img alt="Mode" src="https://img.shields.io/badge/mode-local--first-purple">
  <img alt="Network" src="https://img.shields.io/badge/network-off%20by%20default-orange">
  <img alt="Receipts" src="https://img.shields.io/badge/receipts-enabled-00aaff">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-lightgrey">
</p>

<p align="center">
  <a href="#quick-start---windows">Quick Start</a> ·
  <a href="#guided-tour">Guided Tour</a> ·
  <a href="#local-governance-proxy">Governance Proxy</a> ·
  <a href="#public-safety-boundary">Safety Boundary</a> ·
  <a href="docs/PUBLIC_RELEASE_LOCK_V1.md">Release Lock</a>
</p>

<p align="center">
  <img src="assets/aion-icli-blue-banner.svg" alt="AION ICLI blue terminal banner" width="900">
</p>
---

**AION ICLI** is a local-first command-line interface for governed AI and system actions.

It helps users evaluate requests, expose boundaries, and produce receipts before trust is granted.

If you want a CLI that makes AI/system actions more inspectable, constrained, and replayable, this is the front door.

---


## Demo: Your agent said it was done. AION proved whether it was admissible.

Problem: agents can claim completion without admissible local evidence.

AION answer: run a local proof gate that checks claims against artifacts and returns governed decisions.

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
```

Expected decisions:

- PASS
- WARN
- BLOCK

Output paths:

- `demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.json`
- `demo\agent-claim-proof-gate\output\agent_claim_proof_gate_results_v1.md`

Verify:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AGENT_CLAIM_PROOF_GATE_DEMO_V1.ps1
```

Expected marker:

- `AION_AGENT_CLAIM_PROOF_GATE_DEMO_V1_VERIFY_OK`

Fresh-clone acceptance is verified by `scripts\VERIFY_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1.ps1`.


## Public Demo Release Pack

- ZIP: `dist\aion-public-demo-release-pack-v1.zip`
- SHA256: `54FFBD4E701820BEAC261D0043FA67705F90C79EF48AC115B81174535BC7009B`

Verify:


## Interpretation Rule

Do not patch runtime until this report shows what is actually present, what is merely documented, what is verified, and what is wired.
