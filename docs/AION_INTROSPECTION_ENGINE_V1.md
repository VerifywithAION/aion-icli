# AION Introspection Engine V1

AION Introspection Engine V1 builds a local living proof graph of what is proven, what is missing, and what the next build pointer is.

## What this layer does

- Collects capability proof state from local docs, reports, release artifacts, and verifier scripts.
- Produces a machine-readable proof graph (`release/AION_LIVING_PROOF_GRAPH_V1.json`).
- Produces a human-readable proof report (`reports/AION_LIVING_PROOF_GRAPH_V1.md`).
- Records local-only introspection receipts under `receipts/introspection/`.

## Evidence engine role

In this phase, the evidence engine function is to classify each tracked capability as:

- `PROVEN`
- `MISSING_VERIFIER`
- `MISSING_DOC`
- `MISSING_REPORT`

This is a local proof-state lens, not a cloud service.

## Living proof graph role

The living proof graph tracks:

- `proven_capabilities` with verifier marker expectations
- `core_locked_markers`
- `known_receipt_domains`
- `missing_or_partial`
- `next_build_pointer`
- summary counts (`proven_count`, `missing_count`)

It complements runtime receipts by showing current repo proof posture at build time.

## How this differs from runtime receipts

- Runtime receipts prove specific operation events.
- Living proof graph proves current capability wiring/evidence state.

Both are local and public-safe, but they answer different governance questions.

## Commands

Build graph:

```powershell
python .\src\aion_introspection_engine.py build
```

Show current status:

```powershell
python .\src\aion_introspection_engine.py status
```

Run demo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_INTROSPECTION_ENGINE_V1_DEMO.ps1
```

Run verifier:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_INTROSPECTION_ENGINE_V1.ps1
```

Expected markers:

- `AION_INTROSPECTION_ENGINE_V1_VERIFY_OK`
- `AION_INTROSPECTION_ENGINE_V1_DEMO_OK`

## Public-safe posture

- Local-only file inspection
- No provider/API calls
- No external network calls
- No action execution
- Mutation limited to approved release/report/receipt outputs
