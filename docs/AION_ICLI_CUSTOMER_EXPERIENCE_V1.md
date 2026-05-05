# AION ICLI Customer Experience V1

## Purpose

AION ICLI Customer Experience V1 locks the human-facing command-line identity of AION before Avatar Presence work begins.

ICLI means **Interactive Command Line Intelligence**.

This milestone proves that AION can present itself through a local operator terminal with:

- the canonical AION block logo
- the AION ICLI name
- governed local mode
- offline-capable by design messaging
- no external APIs by default
- a plain-language offline capability list
- a governed answer surface
- a local smoke-test receipt

## Canonical Banner Text

AION ICLI

Interactive Command Line Intelligence

Governed Local Mode

Offline-capable by design

No external APIs by default

## Offline Capability Block

What I can do offline:

- Answer from local rules and local project context
- Evaluate actions before execution
- Produce receipts and proof traces
- Block unsafe or unproven operations
- Preserve evidence for replay and audit

## Canonical Reply

I am not an LLM. I am a governed execution layer that can talk through this interface. I help evaluate actions, expose boundaries, produce receipts, and make proof visible before trust.

## Launcher Path

The verified launcher path is:

    bin\aion.cmd
    -> bin\aion.ps1
    -> aion.ps1
    -> src\aion_cli_entry.py

The Windows package launcher also routes through this path:

    dist\aion-windows-exe-v1\aion.cmd
    -> bin\aion.cmd

## Boundaries

- offline_mode=true
- llm_required=false
- external_ai_required=false
- network_used=false
- external_api_called=false
- external_connector_used=false
- autonomous_execution_performed=false
- tool_execution_performed=false
- audio_playback_performed=false
- avatar_rendered=false
- self_mutation_performed=false
- policy_mutation_performed=false
- code_mutation_performed=false
- canonical_graph_mutation_performed=false
- local_receipts_only=true

## Expected Markers

- AION_CLI_SMOKE_TEST_V1_PASS
- AION_ICLI_CUSTOMER_EXPERIENCE_V1_VERIFY_OK
- AION_ICLI_CUSTOMER_EXPERIENCE_V1_TEST_PASS

## Design Rule

Avatar Presence V2 must sit on top of this ICLI experience. It must not replace the local CLI root channel.