# AION Evaluate API Adapter V1

## What this adapter does

AION Evaluate API Adapter V1 exposes a local HTTP governance endpoint for machine-to-machine risk review.

Flow:

- BuzzShield detects.
- AION governs.
- Receipt proves.

## Endpoints

- `GET http://127.0.0.1:8765/health`
- `POST http://127.0.0.1:8765/evaluate`

Localhost-only binding: `127.0.0.1:8765`

## Request schema (V1)

```json
{
  "source": "BuzzShield",
  "chain": "ethereum",
  "contract_address": "0x...",
  "score": 32,
  "verdict": "FLAGGED",
  "patterns": ["example_pattern"],
  "summary": "Finding summary",
  "confidence": 0.91,
  "recommended_action": "block"
}
```

## Response schema (V1)

```json
{
  "adapter": "AION_EVALUATE_API_V1",
  "governance_decision": "BLOCK",
  "risk_level": "HIGH",
  "reason": "Threat signal is flagged or score is below 50.",
  "missing_controls": [],
  "boundary": "LOCAL_ONLY",
  "network": "NOT_USED",
  "mutation": "NOT_PERFORMED",
  "execution": "NOT_PERFORMED",
  "receipt_id": "aion_eval_xxxxxxxx",
  "receipt_path": "receipts/evaluate/...",
  "receipt_abs_path": "C:/.../receipts/evaluate/....json",
  "receipt_written": true,
  "receipt_sha256": "hexsha256",
  "repo_root": "C:/.../aion-live-demo",
  "input_summary": {}
}
```

## Decision logic (V1)

- `verdict=FLAGGED` or `score<50` -> `BLOCK/HIGH`
- `verdict=WATCH` or `50<=score<=69` -> `WARN/MEDIUM`
- `verdict=CLEAN` and `score>=70` -> `ALLOW/LOW`
- missing required fields -> `REVIEW_ONLY/UNKNOWN`
- unknown verdict -> `REVIEW_ONLY/MEDIUM`
- high-risk patterns (`private_key`, `seed`, `credential`, `drain`, `exploit`, `authorization_bypass`, `proxy_admin`, `replay`) -> `BLOCK/HIGH`

## Safety boundary

- local server only (`127.0.0.1`)
- no external provider/API calls
- no external network dependency
- no execution of user artifacts

## Receipt behavior

Each evaluate request writes a receipt under:

- `receipts/evaluate/*.json`

Receipt includes:

- UTC timestamp
- request payload
- governance output
- boundary/network/mutation/execution posture
- receipt id and adapter name
- absolute receipt path (`receipt_abs_path`)
- receipt persistence flag (`receipt_written`)
- receipt file hash (`receipt_sha256`)

Runtime receipts are local artifacts and are not committed.

## Run

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_EVALUATE_API_V1.ps1
```

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_EVALUATE_API_V1_DEMO.ps1
```

Expected marker:

- `AION_EVALUATE_API_V1_DEMO_OK`

## Verify

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_EVALUATE_API_V1.ps1
```

Expected marker:

- `AION_EVALUATE_API_V1_VERIFY_OK`
