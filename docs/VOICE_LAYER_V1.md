# AION ICLI Voice Layer V1

## Purpose

Voice Layer V1 keeps internal capability routing and receipts intact while changing default visible output to natural operator-facing AION language.

Governance should be felt, not seen.

## Internal routing vs visible voice

- Internal: capability routing (`preflight`, `creative`, `intuition`, `cortex`, `connectors`, `receipts`, `verify`) remains active.
- Internal: receipts still store machine-verifiable fields (`mode`, `capability`, `boundary`, `network`, `mutation`, `execution`).
- Visible default: human-facing response + proof footer.
- Visible diagnostics mode: explicit routing lines for debugging.

## Diagnostics mode

Commands:

- `diagnostics on`
- `diagnostics off`
- `diagnostics`

Behavior:

- Diagnostics OFF (default): hide explicit machine routing lines.
- Diagnostics ON: show capability/boundary/network/mutation/execution/receipt lines.

## Proof footer

Default visible proof footer:

`Proof: local-only · no network · no mutation · no execution · receipt written`

## Personality rules (public-safe)

Derived from public-safe doctrine style in prior AION governance docs:

- calm, sharp, protective operator tone
- concise, strategic, and local-first
- no fake execution claims
- no noisy policy wall in default user output
- explicit safety proof remains available

## Before/after examples

Before (diagnostic-heavy default):

- `Capability > PREFLIGHT`

After (default voice):

- “Don’t run it yet. First we make it observable…”
- `Proof: local-only · no network · no mutation · no execution · receipt written`

With diagnostics ON:

- `Capability > PREFLIGHT`
- `Boundary   > LOCAL_ONLY`
- `Network    > NOT_USED`
- `Mutation   > NOT_PERFORMED`
- `Execution  > NOT_PERFORMED`
- `Receipt    > receipts\local\aion_cli_receipt_v1.json`

## Safety boundary

- local-only default
- no network calls
- no external provider execution
- no mutation execution
- receipt-backed replay path

## Verification marker

`AION_VOICE_LAYER_V1_VERIFY_OK`
