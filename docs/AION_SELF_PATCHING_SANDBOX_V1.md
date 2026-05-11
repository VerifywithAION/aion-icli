# AION Self-Patching Sandbox V1

AION Self-Patching Sandbox V1 creates patch proposals and proof artifacts in a bounded sandbox without mutating production targets.

## What it does

- Validates patch input and target path safety.
- Rejects absolute paths and path traversal.
- Rejects forbidden target path parts (`.git`, `.env`, `secrets`, `private`, `node_modules`, `__pycache__`).
- Writes sandbox files only under `release_runtime/sandbox/<sandbox_id>/`.
- Produces rollback and dry-run proof via hash validation.

## What it refuses to do

- No direct patching of production target files.
- No provider/network calls.
- No execution of target actions.

## Input schema (V1)

```json
{
  "source": "SelfRepairPlanner|Manual",
  "target_file": "relative/path/to/file.txt",
  "original_content": "public-safe original content",
  "proposed_content": "public-safe proposed replacement content",
  "reason": "why patch is proposed",
  "verification_marker": "AION_EXAMPLE_PATCH_OK"
}
```

## Output schema (V1)

- `sandbox`: `AION_SELF_PATCHING_SANDBOX_V1`
- `patch_status`: `SANDBOXED_ONLY|REJECTED`
- `production_mutation`: `NOT_PERFORMED`
- `sandbox_mutation`: `PERFORMED|NOT_PERFORMED`
- `rollback_available`, `dry_run_verified`
- hash block for original/proposed/rollback
- sandbox path block
- forbidden action block
- receipt fields (`receipt_path`, `receipt_abs_path`, `receipt_written`, `receipt_sha256`)

## Rollback + dry-run proof

- `rollback.txt` is written from `original_content`.
- `rollback_sha256` must equal `original_sha256`.
- `dry_run_verified=true` only when `original.txt`, `proposed.txt`, and rollback hash checks all pass.

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_SELF_PATCHING_SANDBOX_V1_DEMO.ps1
```

Expected marker:

- `AION_SELF_PATCHING_SANDBOX_V1_DEMO_OK`

## Verifier

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_SELF_PATCHING_SANDBOX_V1.ps1
```

Expected marker:

- `AION_SELF_PATCHING_SANDBOX_V1_VERIFY_OK`

## Public-safe posture

- Local-only
- Sandbox-only mutation
- Production mutation blocked
- Runtime receipts only under `receipts/sandbox/`
