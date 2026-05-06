# AION Adaptive Reasoning Layer V1

## Why Voice Layer alone was not enough

Voice Layer V1 improved tone, but fixed phrasing can still feel pre-scripted.

Adaptive Reasoning Layer V1 adds prompt-signal extraction so responses are composed from what the operator actually asked.

## Extracted signals

The CLI extracts lightweight local signals:

- `subject`
- `urgency`
- `missing_evidence`
- `risk_lens`

These signals shape response composition without any external model call.

## Internal routing vs visible output

- Internal capability routing remains active (preflight/creative/intuition/cortex/connectors/receipts/verify).
- Receipts remain machine-verifiable and keep boundary fields.
- Default visible output remains natural and operator-facing.
- Diagnostics mode reveals routing + extracted signals.

## Diagnostics behavior

Commands:

- `diagnostics on`
- `diagnostics off`
- `diagnostics`

When diagnostics is ON, output includes:

- Capability
- Subject
- Urgency
- Missing evidence
- Risk lens
- Boundary / Network / Mutation / Execution / Receipt

When diagnostics is OFF, these internals are hidden again.

## Safety boundary

- local-only by default
- no network calls
- no external provider calls
- no mutation execution
- receipt-backed proof path

## Public-safe doctrine derivation

This layer follows public-safe AION doctrine patterns:

- proof before trust
- local-first, receipt-bound governance
- preflight before execution
- intuition as risk-sensing
- governance should be felt, not seen

## Verification marker

`AION_ADAPTIVE_REASONING_LAYER_V1_VERIFY_OK`
