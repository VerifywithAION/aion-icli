# AION ICLI Public Install Package V1 Report

## Status

PASS

## Package

    dist/aion-icli-public-install-package-v1.zip

## SHA256

    1F87C275AE088EBE5CCF6CCC5E14BF909ED6F379FC99B91617EF0D95B9DDED04

## Verified public head

    8a21185 Verify public install package from ZIP contents

## Package contents

- launchers
- docs
- examples
- schemas
- scripts
- reports
- Python CLI entrypoint
- ZIP-content verifier

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
    AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK

## Status

LOCKED as Public Install Package V1 rebuilt from current verifier-corrected repo state.
