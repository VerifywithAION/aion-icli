# AION Cross-Platform Packaging V1

## Purpose

AION Cross-Platform Packaging V1 makes the public GitHub launch surface credible across Windows, macOS, and Linux.

This milestone does not add cloud services, external APIs, autonomous execution, or avatar behavior. It only proves that the local AION ICLI root channel has OS-appropriate launchers.

## Launcher Matrix

| OS / Shell | Launcher | Expected path |
|---|---|---|
| Windows CMD | `bin\aion.cmd` | CMD delegates to PowerShell launcher |
| Windows PowerShell | `bin\aion.ps1` | Shows AION ICLI and delegates to root launcher |
| macOS/Linux sh | `bin/aion` | Uses `pwsh`/`powershell` when available, then Python fallback |

## Public GitHub Rule

A public user should be able to clone the repo and see obvious launchers:

    Windows:
      bin\aion.cmd

    PowerShell:
      powershell -NoProfile -ExecutionPolicy Bypass -File bin\aion.ps1

    macOS/Linux:
      sh bin/aion

## Customer Surface

The launcher stack must preserve:

- AION ICLI
- Interactive Command Line Intelligence
- Governed Local Mode
- Offline-capable by design
- No external APIs by default

## Boundaries

- offline_mode=true
- network_used=false
- external_api_called=false
- external_connector_used=false
- autonomous_execution_performed=false
- self_mutation_performed=false
- policy_mutation_performed=false
- code_mutation_performed=false
- local_receipts_only=true

## Expected Markers

- AION_CROSS_PLATFORM_PACKAGING_V1_VERIFY_OK
- AION_CROSS_PLATFORM_PACKAGING_V1_TEST_PASS