# AION ICLI Safe Model Adapter Dry-Run V1

## Purpose

Safe Model Adapter Dry-Run V1 demonstrates how an AI/model request can be reviewed by AION ICLI before any provider call is made.

This release does not call OpenAI, Anthropic, Gemini, Ollama, local models, hosted models, or any external provider.

It only simulates the governance envelope for model-mediated actions.

## Public model

    App or AI tool
        -> model request envelope
        -> AION connector request
        -> Safe Model Adapter Dry-Run
        -> local review result
        -> receipt

## What this proves

- model requests can be reviewed before execution
- provider use can remain off by default
- network use can remain off by default
- model calls can remain dry-run
- receipts can be generated locally
- generated outputs can remain ignored by Git

## What this does not do

- it does not call real model providers
- it does not require provider keys
- it does not store credentials
- it does not run a local LLM
- it does not perform hidden routing
- it does not expose non-public implementation details

## User-facing principle

Governance should be felt, not seen.

The adapter should sound like a careful operator:

    I checked the model request locally first.
    I did not call a provider.
    I did not use the network.
    I wrote a receipt for review.

## Run

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1

## Expected marker

    AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_OK

## Status

LOCKED as safe dry-run model adapter proof.
