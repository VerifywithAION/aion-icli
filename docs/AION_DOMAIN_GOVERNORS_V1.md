# AION Domain Governors V1

Mini AION Domain Governors V1 routes governance payloads to domain-specific policy guards while preserving one unified local governance posture.

## Why this layer exists

AION is not only for AI agents. It governs pre-execution risk across autonomous system domains including wallet, security, trading, quantum, and physical AI contexts.

## Supported domains (V1)

- `agent`
- `wallet`
- `security`
- `trading`
- `quantum`
- `physical_ai`
- `unknown`

## Input schema (V1)

```json
{
  "domain": "agent|wallet|security|trading|quantum|physical_ai|unknown",
  "source": "AION|BuzzShield|WalletGuard|Manual|Agent",
  "action": "public-safe summary of proposed action",
  "risk_level": "HIGH|MEDIUM|LOW|UNKNOWN",
  "signals": ["network", "mutation", "signature", "funds_at_risk", "execution", "unsafe_claim"],
  "controls": {
    "verifier": true,
    "receipt": true,
    "rollback": false,
    "dry_run": true,
    "human_review": false
  },
  "requested_execution": false
}
```

## Output schema (V1)

- `engine`: `AION_DOMAIN_GOVERNORS_V1`
- `selected_governor`
- `governance_decision`: `BLOCK|WARN|ALLOW|REVIEW_ONLY`
- `risk_level`, `reason`, `required_next_step`, `domain_controls_required`
- local posture: `boundary=LOCAL_ONLY`, `network=NOT_USED`, `mutation=NOT_PERFORMED`, `execution=NOT_PERFORMED`
- receipt metadata with repo-root anchored path + sha256

## Domain policy highlights (V1)

- **agent**: execution without verifier -> `BLOCK`; unsafe claim -> `REVIEW_ONLY` or `BLOCK` on high risk.
- **wallet**: signature/funds-at-risk without human review -> `BLOCK`; missing receipt -> `REVIEW_ONLY`.
- **security**: high risk without verifier -> `BLOCK`; flagged/exploit signals -> `BLOCK`.
- **trading**: execution without dry-run -> `BLOCK`; high risk without human review -> `BLOCK`.
- **quantum**: execution without verifier -> `BLOCK`; missing receipt -> `REVIEW_ONLY`.
- **physical_ai**: execution with high/unknown risk -> `BLOCK`; missing human review -> `BLOCK`.
- **unknown**: `REVIEW_ONLY` by default.

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_DOMAIN_GOVERNORS_V1_DEMO.ps1
```

Expected marker:

- `AION_DOMAIN_GOVERNORS_V1_DEMO_OK`

## Verifier

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_DOMAIN_GOVERNORS_V1.ps1
```

Expected marker:

- `AION_DOMAIN_GOVERNORS_V1_VERIFY_OK`

## Public-safe posture

- No external network calls
- No provider API calls
- No governed action execution
- Mutation limited to runtime receipts under `receipts/domain_governors/`
