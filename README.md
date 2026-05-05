# ⚡ AION ICLI — Governed Command Line Intelligence

<p align="center">
  <strong>Governed Execution · Receipts · Offline Replay</strong>
</p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/build-passing-brightgreen">
  <img alt="Release" src="https://img.shields.io/badge/release-public%20v1-blue">
  <img alt="Mode" src="https://img.shields.io/badge/mode-local--first-purple">
  <img alt="Network" src="https://img.shields.io/badge/network-off%20by%20default-orange">
  <img alt="Receipts" src="https://img.shields.io/badge/receipts-enabled-00aaff">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-lightgrey">
</p>

<p align="center">
  <a href="#quick-start---windows">Quick Start</a> ·
  <a href="#guided-tour">Guided Tour</a> ·
  <a href="#local-governance-proxy">Governance Proxy</a> ·
  <a href="#public-safety-boundary">Safety Boundary</a> ·
  <a href="docs/PUBLIC_RELEASE_LOCK_V1.md">Release Lock</a>
</p>

<p align="center">
  <img src="assets/aion-icli-blue-banner.svg" alt="AION ICLI blue terminal banner" width="900">
</p>
---

**AION ICLI** is a local-first command-line interface for governed AI and system actions.

It helps users evaluate requests, expose boundaries, and produce receipts before trust is granted.

If you want a CLI that makes AI/system actions more inspectable, constrained, and replayable, this is the front door.

---

## What you can do with AION ICLI

AION ICLI gives users a simple way to place a governance layer in front of AI or system actions.

At this public stage, it runs locally and proves the pattern without requiring cloud keys, model credentials, or background services.

### 1. Ask AION what it is

    .\bin\aion.cmd "Who are you, AION?"

Example result:

    Boundary > LOCAL_ONLY
    Network  > NOT_USED
    Mutation > NOT_PERFORMED
    Receipt  > receipts\local\aion_cli_receipt_v1.json

Use this to confirm AION is running in local governed mode.

### 2. Check an action before trusting it

Instead of accepting an AI or automation suggestion blindly, AION ICLI shows the boundary around the action.

Example use case:

    A script wants to run.
    A user wants to know if it was evaluated locally.
    AION shows whether network, mutation, or external calls were used.

### 3. Produce a receipt

AION ICLI writes a local receipt for basic interactions.

Receipts help answer:

- what was requested
- what boundary was active
- whether a network was used
- whether mutation was performed
- where the evidence was written

### 4. Run an offline governance proxy demo

AION ICLI includes a deterministic SDK/governance proxy example.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_LOCAL_GOVERNANCE_PROXY_V1.ps1

Example behavior:

    risk_hint=low  -> ALLOW
    risk_hint=high -> BLOCK
    missing hint   -> WARN

This demonstrates how future SDK, API, or model-mediated workflows can be checked before execution.

### 5. Keep generated outputs clean

Runtime outputs are written to:

    examples/governance/generated/

That folder is ignored by Git, so verification does not dirty the repository.

### 6. Verify the release

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_RELEASE_LOCK_V1.ps1

Expected marker:

    AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK

---
## What AION ICLI is

AION ICLI is a governed command-line interface designed to make execution safer, clearer, and more verifiable.

It is built around a simple operating rule:

    Do not trust an action just because it was suggested.
    Evaluate it, expose boundaries, produce a receipt, and make the proof visible.

AION ICLI can be used as a local governance surface for:

- AI assistants
- agent workflows
- SDK requests
- API actions
- automation previews
- local policy checks
- proof-oriented demos

By default, it runs locally and does not call external APIs.

---

## What AION ICLI is not

AION ICLI is not:

- a cloud AI provider
- a general-purpose AI model
- a live model provider
- a cloud AI service
- an autonomous agent
- a bounty engine
- a background automation service
- a replacement for independent security review

This repo contains the interface, examples, docs, schemas, and deterministic local governance demo needed to run AION ICLI.

---

## Why it exists

Modern AI systems often produce outputs without showing enough execution context.

AION ICLI demonstrates a different pattern:

    request -> boundary check -> decision -> receipt -> replayable proof

The goal is not to make the user blindly trust the interface.

The goal is to make the interface show:

- what it did
- what it did not do
- whether it used a network
- whether it mutated anything
- what receipt was created
- what boundary was enforced

---

## Quick Start - Windows

    git clone https://github.com/VerifywithAION/aion-icli.git
    cd aion-icli
    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

Expected markers:

    AION_ICLI_INSTALL_PREVIEW_OK
    AION ICLI
    Boundary > LOCAL_ONLY
    Network  > NOT_USED
    Mutation > NOT_PERFORMED

---

## Quick Start - macOS/Linux

    git clone https://github.com/VerifywithAION/aion-icli.git
    cd aion-icli
    sh ./install.sh
    sh ./bin/aion "Who are you, AION?"

---

## Guided Tour

### Step 1 - Run the CLI

Windows:

    .\bin\aion.cmd "Who are you, AION?"

PowerShell:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\bin\aion.ps1 "Who are you, AION?"

macOS/Linux:

    sh ./bin/aion "Who are you, AION?"

---

### Step 2 - Read the banner

You should see:

    AION ICLI
    Interactive Command Line Intelligence
    Governed Local Mode
    Offline-capable by design
    No external APIs by default

This means the public interface is running in local governed mode.

---

### Step 3 - Observe the offline capability block

AION ICLI should show:

    What I can do offline:
    - Answer from local rules and local project context
    - Evaluate actions before execution
    - Produce receipts and proof traces
    - Block unsafe or unproven operations
    - Preserve evidence for replay and audit

---

### Step 4 - Inspect the boundary output

Every basic interaction should expose the boundary:

    Boundary > LOCAL_ONLY
    Network  > NOT_USED
    Mutation > NOT_PERFORMED
    Receipt  > receipts\local\aion_cli_receipt_v1.json

This is the central behavior: AION ICLI tells you what happened and what did not happen.

---

### Step 5 - Run the public safety verifier

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1

Expected marker:

    AION_ICLI_PUBLIC_SAFE_VERIFY_OK

---

### Step 6 - Run the local governance proxy demo

AION ICLI includes a deterministic offline SDK/governance proxy example.

It reads request JSON files and writes generated response/receipt outputs.

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_LOCAL_GOVERNANCE_PROXY_V1.ps1

Expected markers:

    AION_LOCAL_GOVERNANCE_PROXY_V1_DEMO_OK
    AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK

Generated outputs are written to:

    examples/governance/generated/

That folder is ignored by Git so runtime verification does not dirty the repo.

---

### Step 7 - Verify the release lock

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_RELEASE_LOCK_V1.ps1

Expected marker:

    AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK

---

## Local Governance Proxy

The Local Governance Proxy V1 is the public-safe foundation for future SDK/API/model adapter governance.

It does not call external services.

It uses deterministic example request files:

    examples/governance/sdk_request_allow.json
    examples/governance/sdk_request_block.json

It generates responses and receipts into:

    examples/governance/generated/

The demo behavior is intentionally simple:

    risk_hint=low  -> ALLOW
    risk_hint=high -> BLOCK
    missing hint   -> WARN

This proves the governance pattern using a transparent public demo.

---

## Public Safety Boundary

This repository may contain:

- CLI launchers
- local CLI entrypoint
- guided docs
- public schemas
- public examples
- deterministic offline governance proxy
- public-safe verification scripts
- sample receipts

This repository must not contain:

- unrelated backend service code
- confidential documents
- hidden automatic execution logic
- undocumented decision behavior
- live model routing logic
- real provider API keys
- secrets or tokens
- secrets, tokens, or credentials
- exploit automation

---

## Current release status

Latest locked public release:

    f9ce424 Lock AION ICLI Public Release v1

Validated stack:

    3b13c25 Initial public-safe AION ICLI release
    0420c7e Add AION ICLI Local Governance Proxy v1
    2002b85 Keep governance proxy outputs generated and untracked
    f9ce424 Lock AION ICLI Public Release v1

Fresh clone validation proved:

    AION_ICLI_INSTALL_PREVIEW_OK
    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_LOCAL_GOVERNANCE_PROXY_V1_DEMO_OK
    AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK
    AION_ICLI_FRESH_CLONE_CLEANLINESS_TEST_V3_PASS

---

## Future direction

AION ICLI is designed to become a universal governance surface for AI systems, API actions, SDK calls, and model-mediated workflows.

Future connector layers must remain:

- explicit opt-in
- provider-neutral
- no secrets committed
- receipt-bound
- locally verifiable
- governed before execution
- safe by default

---

## Read next

Start here:

    docs/PUBLIC_BOUNDARY.md
    docs/HARDENING_NOTE_V1.md
    docs/REPO_GUIDED_TOUR_V1.md
    docs/CONNECTOR_SDK_CONTRACT_V1.md
    docs/LOCAL_GOVERNANCE_PROXY_V1.md
    docs/PUBLIC_RELEASE_LOCK_V1.md






