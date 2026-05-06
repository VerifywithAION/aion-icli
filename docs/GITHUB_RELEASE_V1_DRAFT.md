# AION ICLI Public Release V1

## Release title

AION ICLI Public Release V1 — Governed Command Line Intelligence

## Suggested tag

v1.0.0-public-icli

## Target commit

2fea528 Rebuild public install package with user guide

## Release asset

dist/aion-icli-public-install-package-v1.zip

## SHA256

8B99C3C7161F2911212E7D57A4F3A3782700DBBCE404288D1E4AD6A671D7D746

## Summary

AION ICLI is a local-first command-line interface for governed AI and system actions.

It helps users evaluate actions before trust by making boundaries, network use, mutation behavior, receipts, and verification visible.

AION ICLI is not another chatbot. It is a governed execution surface for AI/tool/system workflows.

## What is included

- local CLI
- Windows CMD launcher
- PowerShell launcher
- POSIX shell launcher
- blue terminal banner
- local receipts
- public-safe verifier
- connector policy verifier
- public install package verifier
- User Guide V1
- local governance proxy
- safe API dry-run examples
- safe model dry-run examples
- SDK-style request examples
- governed vs ungoverned proof
- connector stack acceptance report
- public install package ZIP

## What is not included

- standalone Windows .exe
- signed installer
- provider keys
- private credentials
- live API execution by default
- live model/provider calls by default
- hidden integrations
- internal/private AION systems

## Quick start from ZIP

1. Download `aion-icli-public-install-package-v1.zip`.
2. Extract it.
3. Open PowerShell inside the extracted folder.
4. Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

Expected boundary output:

    Boundary > LOCAL_ONLY
    Network  > NOT_USED
    Mutation > NOT_PERFORMED
    Receipt  > receipts\local\aion_cli_receipt_v1.json

## Verify the release

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_POLICY_V2.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_USER_GUIDE_V1.ps1

Expected markers:

    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_CONNECTOR_POLICY_V2_VERIFY_OK
    AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK
    AION_USER_GUIDE_V1_VERIFY_OK

## Proof markers already confirmed

    AION_USER_GUIDE_ACCEPTANCE_TEST_V1_FINAL_PASS
    AION_USER_GUIDE_ZIP_SHA256_CONFIRMED
    AION_USER_GUIDE_PACKAGE_HEAD_2FEA528_CONFIRMED

## Product principle

Governance should be felt, not seen.

AION ICLI should feel like a careful operator that helps users act with proof, receipts, and boundaries.

## Status

Ready for GitHub Release V1 draft.
