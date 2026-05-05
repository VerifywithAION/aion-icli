# Connector SDK Contract V1

## Purpose

Define the minimal public-safe SDK request and response contract used by AION ICLI local governance proxy examples.

## Request

Example files:

- examples/governance/sdk_request_allow.json
- examples/governance/sdk_request_block.json

Fields:

- agent: string
- claim_id: string
- claim_type: string
- target: object
- policy_id: optional string
- risk_hint: optional string, allowed demo values: low, high

## Response

Fields:

- decision: ALLOW | WARN | BLOCK
- reason_code: string
- receipt: object

## Receipt Expectations

- receipt_fingerprint
- timestamp
- agent
- claim_id
- claim_type
- decision
- reason_code
- runtime boundaries

## Boundary

This contract is intentionally minimal. It does not include real provider credentials, private routing, API keys, model configuration, or private AION internals.
