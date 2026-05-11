# AION Memory Scars V1

## What memory scars are

Memory Scars V1 is persistent public-safe governance memory for failure lessons:

- trigger -> harm -> repair -> future_rule

It stores negative knowledge that biases future governance decisions away from repeated mistakes.

## Not chatbot memory

This is not conversational memory and not user profiling.
It stores only public-safe governance scars and control lessons.

## Scar schema (V1)

```json
{
  "scar_id": "unique_id",
  "trigger": "unsafe action pattern",
  "harm": "what could go wrong",
  "repair": "what control fixes it",
  "future_rule": "governance rule to apply next time",
  "severity": "LOW|MEDIUM|HIGH",
  "tags": ["network", "mutation", "verifier_missing"],
  "public_safe": true
}
```

## Storage

- Memory store: `.aion_public/memory/memory_scars_v1.jsonl`
- Runtime receipts: `receipts/memory/`

## Public-safe rule

- `public_safe` must be true for accepted scars.
- No secrets, private credentials, or raw sensitive payloads.

## Memory influence behavior

Input event is matched against scar tags, action type, and summary context.

- HIGH scar match -> `recommended_decision_bias=BLOCK`
- MEDIUM scar match -> `recommended_decision_bias=WARN`
- no match -> `recommended_decision_bias=NONE`

## Receipt behavior

Add/evaluate operations write local receipts with:

- `receipt_path`
- `receipt_abs_path`
- `receipt_written`
- `receipt_sha256`
- `repo_root`

Runtime receipts are local and not committed.

## Demo command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_MEMORY_SCARS_V1_DEMO.ps1
```

Expected marker:

- `AION_MEMORY_SCARS_V1_DEMO_OK`

## Verifier command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_MEMORY_SCARS_V1.ps1
```

Expected marker:

- `AION_MEMORY_SCARS_V1_VERIFY_OK`
