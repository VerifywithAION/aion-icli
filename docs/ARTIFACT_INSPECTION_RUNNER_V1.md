# AION Artifact Inspection Runner V1

Expected marker: `AION_ARTIFACT_INSPECTION_RUNNER_V1_VERIFY_OK`

Artifact Inspection Runner V1 adds read-only local inspection before trust.

## Scope

- local-only
- read-only
- no execution
- no network
- no mutation

## Allowed file types

`.ps1 .py .js .ts .tsx .json .md .txt .yaml .yml .cmd .bat .sh`

## Forbidden paths

- `.git`
- `.env`
- `secrets`
- `private`
- `node_modules`
- `__pycache__`
- `.venv` / `venv`
- `dist/*.zip` binary contents
- any path outside repo root

## Risk classification

Outputs include:
- decision: `SAFE_TO_READ | REVIEW_ONLY | BLOCK_EXECUTION | NEEDS_MANUAL_REVIEW`
- risk_level: `LOW | MEDIUM | HIGH`
- reasons
- missing_controls
- detected_patterns
- recommended_next_step

## Diagnostics

When inspection is used:
- Artifact inspection used
- Artifact path
- Decision
- Risk level
- Detected patterns
- Missing controls

## Receipt fields

- `artifact_inspection_used`
- `artifact_path`
- `artifact_size_bytes`
- `file_type`
- `decision`
- `risk_level`
- `detected_patterns`
- `missing_controls`
- `reasons`
- `recommended_next_step`

Boundary invariants remain:
- `boundary = LOCAL_ONLY`
- `network = NOT_USED`
- `mutation = NOT_PERFORMED`
- `execution = NOT_PERFORMED`

## Relationship to scars and proof-before-trust

If no artifact path is provided, AION keeps scar-derived discipline: no artifact, no judgment.
If risky patterns appear without rollback/dry-run/verifier controls, AION escalates to review/block guidance.
