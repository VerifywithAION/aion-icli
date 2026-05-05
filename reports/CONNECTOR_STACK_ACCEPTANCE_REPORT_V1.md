# AION ICLI Connector Stack Acceptance Report V1

## Status

PASS

## Verified public repo head

    60b01a4 Add SDK examples v1

## Purpose

This report records the successful fresh-clone acceptance test for the public AION ICLI connector stack.

It proves that a public user can clone the repository from GitHub and run the full governed connector stack without needing internal AION source, provider keys, model credentials, live APIs, or hidden services.

## Public connector claim

Users and developers can connect to AION governance through public request contracts and dry-run examples.

They can:

- run AION ICLI locally
- submit SDK-style request examples
- review API-style request envelopes
- review model-style request envelopes
- run the local governance proxy
- compare governed vs ungoverned CLI behavior
- generate local receipts
- verify the release lock

They cannot:

- access internal AION implementation details
- bypass governance receipts
- trigger hidden network calls
- trigger hidden model/provider calls
- execute live API actions by default
- mutate files outside generated output folders
- reconstruct deeper AION systems from this public repo

## Fresh clone flow verified

    git clone https://github.com/VerifywithAION/aion-icli.git
    cd aion-icli
    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_LOCAL_GOVERNANCE_PROXY_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_RELEASE_LOCK_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_POLICY_V2.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_API_ADAPTER_DRY_RUN_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SDK_EXAMPLES_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1.ps1

## Verified stack

- AION ICLI CLI
- Public-safe verifier
- Local Governance Proxy V1
- Public Release Lock V1
- Connector Policy V2
- Safe API Adapter Dry-Run V1
- Safe Model Adapter Dry-Run V1
- SDK Examples V1
- Governed vs Ungoverned CLI Proof V1

## Acceptance markers

    AION_ICLI_INSTALL_PREVIEW_OK
    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_LOCAL_GOVERNANCE_PROXY_V1_DEMO_OK
    AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK
    AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK
    AION_CONNECTOR_POLICY_V2_VERIFY_OK
    AION_SAFE_API_ADAPTER_DRY_RUN_V1_VERIFY_OK
    AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_VERIFY_OK
    AION_SDK_EXAMPLES_V1_VERIFY_OK
    AION_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1_OK
    AION_ICLI_CONNECTOR_STACK_ACCEPTANCE_TEST_V1_PASS
    AION_ICLI_PUBLIC_REPO_HEAD_60B01A4_CONFIRMED

## Generated output folders verified

- examples/governance/generated
- examples/api-adapter/generated
- examples/model-adapter/generated
- examples/sdk/generated
- examples/proofs/generated

These folders are generated locally and ignored by Git.

## Cleanliness result

Fresh clone remained clean after running the full connector stack.

    [OK] Fresh clone remains clean

## Product principle

    Governance should be felt, not seen.

AION ICLI should feel like a careful operator, not a noisy firewall.

It helps the user by making boundaries, network use, mutation behavior, receipts, and replay evidence visible without exposing internal implementation.

## Public release conclusion

AION ICLI is now publicly demonstrable as a connectable governance surface.

The connector stack proves that apps, SDKs, API clients, model request envelopes, and automation-style requests can be reviewed locally through AION governance while preserving the public safety boundary.

## Status

LOCKED as Connector Stack Acceptance Report V1.
