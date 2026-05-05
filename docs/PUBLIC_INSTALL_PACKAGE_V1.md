# AION ICLI Public Install Package V1

## Status

Release-package-ready baseline.

## Purpose

This package is a GitHub-release-ready ZIP distribution of AION ICLI.

It lets users download or clone AION ICLI and run it locally with included launchers.

## What is included

- Windows CMD launcher
- PowerShell launcher
- POSIX shell launcher
- Python CLI entrypoint
- installer preview scripts
- public docs
- public examples
- public schemas
- public verifiers
- connector stack reports

## What is not included

- standalone Windows .exe
- signed installer
- private credentials
- provider keys
- internal/private AION systems
- hidden API integrations

## Run from source clone

    git clone https://github.com/VerifywithAION/aion-icli.git
    cd aion-icli
    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

## Run from ZIP

1. Download and extract the ZIP.
2. Open PowerShell inside the extracted folder.
3. Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

## Verify

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_RELEASE_LOCK_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.ps1

## Expected markers

    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK
    AION_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1_VERIFY_OK

## Current verified public head

    b761e87 Make public-safe verifier PowerShell 5.1 compatible

## Status

LOCKED as Public Install Package V1.
