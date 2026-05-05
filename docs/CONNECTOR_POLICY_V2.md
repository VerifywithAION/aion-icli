# AION ICLI Connector Policy V2

## Purpose

Connector Policy V2 defines how external apps, SDKs, API clients, AI tools, and automation systems may connect to AION ICLI for governance decisions.

The goal is simple:

    Connect to AION governance.
    Do not expose, bypass, clone, or reconstruct AION internals.

## Public connector model

    External app / SDK / API / AI tool
            -> AION connector request contract
            -> Local governance proxy
            -> ALLOW / WARN / BLOCK
            -> Receipt

## What connectors are allowed to do

Connectors may:

- Submit structured governance requests
- Declare intent
- Declare target action
- Declare risk hint
- Declare requested network behavior
- Declare whether mutation or execution is requested
- Receive ALLOW, WARN, or BLOCK
- Receive a receipt
- Store generated outputs locally
- Run in dry-run mode

## What connectors must not do

Connectors must not:

- Commit secrets, tokens, credentials, or provider keys
- Call external APIs by default
- Execute actions automatically in public mode
- Hide network access
- Hide mutation behavior
- Bypass receipt generation
- Bypass governance decisions
- Depend on undocumented behavior
- Include unrelated backend service code
- Expose non-public implementation details
- Act as an implementation cloning kit

## Required request fields

Every connector request should include:

- request_id
- connector_id
- connector_type
- intent
- target
- risk_hint
- requested_capabilities
- execution_mode
- network_policy
- mutation_policy
- receipt_policy

## Decision contract

AION ICLI returns:

- ALLOW when the request is explicitly permitted
- WARN when the request is incomplete, ambiguous, or needs operator review
- BLOCK when the request violates policy or attempts unsafe behavior

## Default public-mode behavior

In public mode:

- network access is off by default
- mutation is off by default
- execution is dry-run unless explicitly permitted
- generated outputs are written to ignored folders
- receipts are required
- provider adapters are documentation-only or dry-run unless future opt-in support is added

## Provider-neutral design

Connector Policy V2 does not require OpenAI, Anthropic, Gemini, Ollama, local models, cloud APIs, or any specific provider.

A connector may describe a provider target, but the public release must not include real provider secrets or hidden network calls.

## Safe adapter roadmap

Future connector work should proceed in this order:

1. Safe API Adapter Dry-Run V1
2. Safe Model Adapter Dry-Run V1
3. SDK Examples V1
4. Optional opt-in provider adapters

## Status

LOCKED as public connector boundary policy.
