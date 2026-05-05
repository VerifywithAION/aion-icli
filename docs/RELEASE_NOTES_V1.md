# AION ICLI Release Notes V1

## Release

AION ICLI Public Release V1

## Validated Head

    4ad03d7 Refine AION ICLI README banner and capabilities

## What this release includes

- Public AION ICLI command-line interface
- Windows launcher
- PowerShell launcher
- POSIX launcher
- Installer preview scripts
- Blue AION ICLI README banner
- README guided tour
- User capability examples
- Local receipt generation
- Public-safe verifier
- Local governance proxy demo
- Governance request and response examples
- Governance receipt schema
- Release lock verifier
- Fresh clone cleanliness behavior

## What users can do

Users can:

- Clone the repository from GitHub
- Run the installer preview
- Ask AION what it is
- Confirm local-only mode
- Confirm no network use by default
- Confirm no mutation by default
- Produce a local receipt
- Run a deterministic governance proxy demo
- Generate ALLOW and BLOCK example responses
- Verify the public release lock
- Confirm generated outputs do not dirty Git

## Verified public flow

    git clone https://github.com/VerifywithAION/aion-icli.git
    cd aion-icli
    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_LOCAL_GOVERNANCE_PROXY_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_RELEASE_LOCK_V1.ps1

## Acceptance markers

    AION_ICLI_INSTALL_PREVIEW_OK
    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_LOCAL_GOVERNANCE_PROXY_V1_DEMO_OK
    AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK
    AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK
    AION_ICLI_FINAL_PUBLIC_ACCEPTANCE_TEST_V1_PASS
    AION_ICLI_PUBLIC_REPO_HEAD_4AD03D7_CONFIRMED

## Public safety posture

This release is local-first and offline-capable by default.

It does not require cloud keys, model credentials, external APIs, or background services for the validated public flow.

Runtime-generated outputs are written to ignored folders so verification does not dirty the repository.

## Status

LOCKED as Public Release V1.
