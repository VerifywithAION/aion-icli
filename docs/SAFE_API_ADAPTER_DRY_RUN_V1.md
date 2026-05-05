# AION ICLI Safe API Adapter Dry-Run V1

## Purpose

Safe API Adapter Dry-Run V1 demonstrates how an external API client can ask AION ICLI for a governance review before any real API call is made.

This release does not perform live network calls.

It only simulates the governance envelope for API actions.

## Public model

    External API client
        -> AION connector request
        -> Safe API Adapter Dry-Run
        -> local review result
        -> receipt

## What this proves

- API actions can be reviewed before execution
- network use can stay off by default
- mutation can stay off by default
- execution can remain dry-run
- receipts can be generated locally
- generated outputs can remain ignored by Git

## What this does not do

- it does not call real APIs
- it does not require provider keys
- it does not store credentials
- it does not execute remote actions
- it does not expose non-public implementation details

## User-facing principle

Governance should be felt, not seen.

The adapter should sound like a careful operator:

    I checked this locally first.
    I did not use the network.
    I did not execute the API call.
    I wrote a receipt for review.

## Run

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_SAFE_API_ADAPTER_DRY_RUN_V1.ps1

## Expected marker

    AION_SAFE_API_ADAPTER_DRY_RUN_V1_OK

## Status

LOCKED as safe dry-run API adapter proof.
