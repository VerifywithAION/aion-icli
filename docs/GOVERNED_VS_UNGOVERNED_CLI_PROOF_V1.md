# AION Governed vs Ungoverned CLI Proof V1

## Purpose

This proof demonstrates why AION ICLI matters.

It compares two responses to the same user request:

1. a normal ungoverned CLI assistant response
2. an AION-governed CLI response

## Core product principle

    Governance should be felt, not seen.

AION should not feel like a cold firewall.

AION should feel like a careful operator that helps the user while quietly preserving boundaries, receipts, and replay evidence.

## What the proof shows

Ungoverned output may sound helpful, but it does not show:

- boundary
- network use
- mutation behavior
- execution behavior
- receipt
- replay evidence

AION-governed output shows:

- local-only boundary
- no network by default
- no mutation by default
- no execution by default
- receipt path
- evidence for later review

## Public-safe boundary

This proof does not expose internal AION implementation details.

It only demonstrates the public user experience difference between invisible trust and governed trust.

## Run

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1.ps1

## Expected marker

    AION_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1_OK
