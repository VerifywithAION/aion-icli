# AION Companion Runtime V1

## Public Name
- Primary: **AION Companion Runtime**
- Vision label: **Humanoid by AION**
- Alternative: **AION Symbiotic Runtime**

## Purpose
AION Companion Runtime V1 is the human-facing delegation layer above the governance stack.  
It translates natural human intent into safe delegation guidance while preserving trust, continuity, and clear boundaries.

## Human-First Output Model
The runtime centers user experience on:
- trust
- continuity
- protection
- one question that matters
- safe next step

Governance machinery remains available as backend trace, not primary emotional UX.

## Prompt Routing Surface
Routed from CLI when prompt starts with:
- `companion`
- `humanoid`
- `trusted companion`
- `protect my`
- `help me delegate`
- `keep me safe`
- `mirror`
- `symbiosis`

## Backend Modules Used
- Dynamic Cognition Engine
- Living Intelligence Kernel
- Domain Governors
- Creativity + Intuition
- Memory Scars
- Preflight Gate
- Sentinel Contradiction

## Safety Posture
- `boundary: LOCAL_ONLY`
- `network: NOT_USED`
- `mutation: NOT_PERFORMED`
- `execution: NOT_PERFORMED`
- No external APIs
- No autonomous execution

## Receipt Behavior
Companion runtime writes receipts to:
- `receipts/companion/*.json`

Each result includes:
- `receipt_id`
- `receipt_path`
- `receipt_abs_path`
- `receipt_written`
- `receipt_sha256`
- `repo_root`

## Run + Verify
- Demo: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_COMPANION_RUNTIME_V1_DEMO.ps1`
- Verify: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_COMPANION_RUNTIME_V1.ps1`

Expected markers:
- `AION_COMPANION_RUNTIME_V1_DEMO_OK`
- `AION_COMPANION_RUNTIME_V1_VERIFY_OK`
