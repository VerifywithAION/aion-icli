# Local Governance Proxy V1

## Purpose

Provide a deterministic, offline, file-mode governance proxy for integration testing.

The proxy reads public-safe JSON request files and writes governed response files plus receipt records.

## Security

- no network calls
- no API keys
- no server
- no external model calls
- no private engine dependency
- deterministic output

## Usage

Input folder:

- examples/governance/sdk_request_*.json

Output folder:

- examples/governance/sdk_response_*.json
- examples/governance/receipts.ndjson

Run:

powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_LOCAL_GOVERNANCE_PROXY_DEMO_V1.ps1

## Behavior

- risk_hint=low produces ALLOW
- risk_hint=high produces BLOCK
- missing risk_hint produces WARN

## Status

Public-safe offline adapter foundation. This is not a live API connector.
