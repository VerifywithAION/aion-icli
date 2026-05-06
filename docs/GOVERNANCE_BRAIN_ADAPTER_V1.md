# AION Governance Brain Adapter V1

Expected marker: `AION_GOVERNANCE_BRAIN_ADAPTER_V1_VERIFY_OK`

## Purpose

AION is not a foundation model. AION is a Governance OS / execution governance layer.

Governance Brain Adapter V1 makes CLI answers evidence-backed by reading public-safe local artifacts instead of relying on canned prose.

## How it works

The CLI keeps capability routing and adaptive reasoning, then attempts a local evidence pass:

- discovers public-safe repo artifacts
- reads bounded local state
- composes short operator answers from evidence
- writes receipt metadata showing whether governance brain was used

## Allowed local reads

- `README.md`
- `docs/*.md`
- `reports/*.md`
- `schemas/*.json`
- `examples/**/*.json`
- `packaging/**/*.json`
- `receipts/local/aion_cli_receipt_v1.json` (if present)
- `scripts/VERIFY_*.ps1` names

## Forbidden reads

- `.git` internals
- `.env`
- `secrets`
- `private`
- `node_modules`
- `.aion`
- `.codara`
- any file larger than 1 MB

## Diagnostics behavior

Normal mode stays human-facing and concise.

Diagnostics mode adds:

- capability
- subject
- urgency
- missing evidence
- risk lens
- governance brain used
- artifacts consulted
- boundary/network/mutation/execution/receipt

## Safety boundary

- local-only
- no network calls
- no mutation execution
- no autonomous execution
- receipt-bound output

## Example prompts

- `what do you know about this release?`
- `what can you verify?`
- `how do connectors work?`
- `where is the proof?`
- `what is wired?`
- `what is missing?`
