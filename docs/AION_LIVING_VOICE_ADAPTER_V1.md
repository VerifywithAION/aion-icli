# AION Living Voice Adapter V1

AION Living Voice Adapter V1 ports continuity-driven conversational intelligence behavior into the public CLI runtime without changing governance boundaries.

## Architecture

- Runtime adapter: `src/aion_living_voice_adapter.py`
- Minimal CLI wiring: `src/aion_cli_entry.py`
- Uses continuity + framing + truth guard logic from recovered behavior patterns.
- No external APIs, no hidden network behavior, no autonomous execution.

## What it does

- Selects adaptive framing style from prompt signals (`direct`, `reframe`, `builder`, `nonobvious`, `plain`).
- Applies continuity shaping from recent turns.
- Enforces truth-preserving bounded language (no fake certainty).
- Produces grounded strategic tone while keeping governance posture.

## What it does not do

- Does not invent a new personality system.
- Does not claim certainty without evidence.
- Does not mutate system state beyond normal CLI receipt behavior.
- Does not execute actions.

## Governance and safety posture

- `LOCAL_ONLY`
- `NOT_USED` network
- `NOT_PERFORMED` mutation/execution
- Existing receipt chain remains active via `receipts/local/aion_cli_receipt_v1.json`

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_LIVING_VOICE_ADAPTER_V1_DEMO.ps1
```

Expected marker:

- `AION_LIVING_VOICE_ADAPTER_V1_DEMO_OK`

## Verifier

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_LIVING_VOICE_ADAPTER_V1.ps1
```

Expected marker:

- `AION_LIVING_VOICE_ADAPTER_V1_VERIFY_OK`
