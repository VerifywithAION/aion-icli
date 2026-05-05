# AION ICLI SDK Examples V1

## Purpose

SDK Examples V1 shows how a developer can connect an application-style request to AION ICLI governance without exposing AION internals.

The examples are local, deterministic, and dry-run only.

## Public developer model

    Developer app
        -> SDK-style request JSON
        -> AION local review runner
        -> human-friendly governance result
        -> receipt

## What this proves

- developers can submit structured requests to AION governance
- AION can review SDK-style actions before execution
- AION can return a helpful result without exposing internal implementation
- receipts can be generated locally
- generated outputs stay ignored by Git

## What this does not do

- it does not expose internal AION source
- it does not call live APIs
- it does not call model providers
- it does not require secrets
- it does not mutate files outside generated output folders
- it does not execute real user actions

## Example request types

- safe local read request
- review-first write request
- model request envelope
- API request envelope

## Run

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_SDK_EXAMPLES_V1.ps1

## Verify

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SDK_EXAMPLES_V1.ps1

## Expected markers

    AION_SDK_EXAMPLES_V1_OK
    AION_SDK_EXAMPLES_V1_VERIFY_OK

## Status

LOCKED as public SDK examples baseline.
