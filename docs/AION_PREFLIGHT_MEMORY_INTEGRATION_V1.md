# AION Preflight + Memory Integration V1

## Why memory is integrated into preflight

Preflight evaluates current payload risk and controls. Memory Scars adds persistent failure lessons so repeated unsafe patterns can raise decisions.

This makes governance both:

- current-state aware (preflight payload)
- history-aware (public-safe scars)

## How memory raises decisions

Preflight now queries memory influence when a memory store exists.

- If memory bias is `BLOCK`, preflight final decision is raised to `BLOCK`.
- If memory bias is `WARN` and preflight was `ALLOW`, final decision is raised to `WARN`.

Reason text is set to:

- `Memory scar raised decision because prior failure rule matched.`

## Public-safe only

Memory scars store public-safe negative knowledge (trigger/harm/repair/future_rule).
No secrets, no private credentials, no external network dependency.

## Not chatbot memory

This is governance memory for control outcomes and repeated failure prevention.
It is not free-form conversational memory.

## Demo command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_PREFLIGHT_MEMORY_INTEGRATION_V1_DEMO.ps1
```

Expected marker:

- `AION_PREFLIGHT_MEMORY_INTEGRATION_V1_DEMO_OK`

## Verifier command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_PREFLIGHT_MEMORY_INTEGRATION_V1.ps1
```

Expected marker:

- `AION_PREFLIGHT_MEMORY_INTEGRATION_V1_VERIFY_OK`

## Receipt behavior

Preflight still writes its own receipt under `receipts/preflight`.
Memory engine writes memory receipts under `receipts/memory`.
Runtime receipts are cleaned by verifiers and are not committed.
