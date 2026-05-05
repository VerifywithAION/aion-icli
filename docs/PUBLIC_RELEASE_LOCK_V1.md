# AION ICLI Public Release Lock V1

## Purpose

Lock the public-safe release state of AION ICLI.

## Release Properties

- Cloneable from GitHub
- Runnable on Windows through bin/aion.cmd
- Runnable through PowerShell via bin/aion.ps1
- POSIX launcher present at bin/aion
- Offline-capable by design
- No external APIs by default
- Local receipt generation
- Offline local governance proxy
- Generated proxy outputs ignored by Git
- No private AION internals exposed

## Verified Markers

- AION_ICLI_INSTALL_PREVIEW_OK
- AION_ICLI_PUBLIC_SAFE_VERIFY_OK
- AION_LOCAL_GOVERNANCE_PROXY_V1_DEMO_OK
- AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK
- AION_ICLI_FRESH_CLONE_CLEANLINESS_TEST_V3_PASS

## Public Boundary

This repository exposes only the public AION ICLI interface, documentation, examples, local deterministic governance proxy, and public-safe receipts/schema material.

It does not expose AION runtimes, confidential documents, proprietary routing logic, private model adapters, secrets, credentials, or live API integrations.

## Status

LOCKED as public-safe release baseline.

