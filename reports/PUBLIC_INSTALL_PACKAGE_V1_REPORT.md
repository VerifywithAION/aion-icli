# AION ICLI Public Install Package V1 Report

## Status

PASS

## Package

    dist/aion-icli-public-install-package-v1.zip

## SHA256

    26FEFCD0C8CC24B8A2112894E28A18AED7988B090DCC4251BC23BDA602C7E82F

## Verified public head

    b761e87 Make public-safe verifier PowerShell 5.1 compatible

## Package contents

- launchers
- docs
- examples
- schemas
- scripts
- reports
- Python CLI entrypoint

## Explicit exclusions

- no standalone Windows .exe
- no signed installer
- no private credentials
- no provider keys
- no hidden integrations
- no generated runtime receipts

## Expected local run

    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

## Expected verification

    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK
    AION_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1_VERIFY_OK

## Status

LOCKED as Public Install Package V1.
