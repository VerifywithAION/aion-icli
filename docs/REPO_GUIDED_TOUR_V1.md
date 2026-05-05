# Repo Guided Tour V2

Use this guide to understand the public AION ICLI repository in the right order.

## Fast path

1. [README](../README.md)
2. [Public Boundary](PUBLIC_BOUNDARY.md)
3. [Repo Guided Tour](REPO_GUIDED_TOUR_V1.md)
4. [Release Notes V1](RELEASE_NOTES_V1.md)
5. [Connector Stack Acceptance Report V1](../reports/CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md)

---

## 1. Start with the README

- [README](../README.md)

The README is the main public entry point.

It explains:

- what AION ICLI is
- what users can do
- how to run it locally
- how developers can connect through governed request examples
- where to find the connector stack docs

---

## 2. Understand the public boundary

- [Public Boundary](PUBLIC_BOUNDARY.md)
- [Hardening Note V1](HARDENING_NOTE_V1.md)

These documents explain the public safety posture.

The public repo is designed for users and developers to connect to AION governance, not to expose unrelated backend systems or implementation-cloning material.

---

## 3. Run the CLI locally

- [Basic Usage Example](../examples/basic_usage.txt)
- [AION ICLI Customer Experience V1](AION_ICLI_CUSTOMER_EXPERIENCE_V1.md)
- [AION Cross-Platform Packaging V1](AION_CROSS_PLATFORM_PACKAGING_V1.md)

Windows:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

PowerShell launcher:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\bin\aion.ps1 "Who are you, AION?"

macOS/Linux:

    sh ./install.sh
    sh ./bin/aion "Who are you, AION?"

Expected behavior:

- AION runs locally
- no external API is used by default
- no mutation is performed by default
- a local receipt is written

---

## 4. Review the release lock

- [Public Release Lock V1](PUBLIC_RELEASE_LOCK_V1.md)
- [Release Notes V1](RELEASE_NOTES_V1.md)

These documents describe the locked public baseline and what the release includes.

---

## 5. Learn the connector model

- [Connector SDK Contract V1](CONNECTOR_SDK_CONTRACT_V1.md)
- [Connector Policy V2](CONNECTOR_POLICY_V2.md)
- [Local Governance Proxy V1](LOCAL_GOVERNANCE_PROXY_V1.md)

The connector model is the public-safe way for apps, SDKs, API clients, model request envelopes, and automation tools to connect to AION governance.

Public connector flow:

    request JSON -> local AION review -> human-friendly result -> receipt

---

## 6. Try the safe API adapter dry-run

- [Safe API Adapter Dry-Run V1](SAFE_API_ADAPTER_DRY_RUN_V1.md)
- [API read dry-run example](../examples/api-adapter/api_request_read_dryrun_v1.json)
- [API write dry-run example](../examples/api-adapter/api_request_write_dryrun_v1.json)

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_API_ADAPTER_DRY_RUN_V1.ps1

Expected marker:

    AION_SAFE_API_ADAPTER_DRY_RUN_V1_VERIFY_OK

This proves API-style requests can be reviewed without live API calls.

---

## 7. Try the safe model adapter dry-run

- [Safe Model Adapter Dry-Run V1](SAFE_MODEL_ADAPTER_DRY_RUN_V1.md)
- [Safe model request example](../examples/model-adapter/model_request_safe_dryrun_v1.json)
- [Review-first model request example](../examples/model-adapter/model_request_review_dryrun_v1.json)

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1

Expected marker:

    AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_VERIFY_OK

This proves model-provider request envelopes can be reviewed without provider calls.

---

## 8. Try the SDK examples

- [SDK Examples V1](SDK_EXAMPLES_V1.md)
- [Safe read SDK example](../examples/sdk/sdk_request_safe_read_v1.json)
- [Review write SDK example](../examples/sdk/sdk_request_review_write_v1.json)
- [Model envelope SDK example](../examples/sdk/sdk_request_model_envelope_v1.json)
- [API envelope SDK example](../examples/sdk/sdk_request_api_envelope_v1.json)

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SDK_EXAMPLES_V1.ps1

Expected marker:

    AION_SDK_EXAMPLES_V1_VERIFY_OK

This proves developers can connect to AION through SDK-style request JSON while staying local and receipt-bound.

---

## 9. Compare governed vs ungoverned output

- [Governed vs Ungoverned CLI Proof V1](GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1.md)

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1.ps1

Expected marker:

    AION_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1_OK

This shows the difference between invisible trust and governed trust.

---

## 10. Read the full acceptance proof

- [Connector Stack Acceptance Report V1](../reports/CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md)

This report records the fresh-clone proof that the public connector stack works from GitHub.

Verified stack:

- CLI
- Local Governance Proxy
- Connector Policy V2
- Safe API Adapter Dry-Run V1
- Safe Model Adapter Dry-Run V1
- SDK Examples V1
- Governed vs Ungoverned CLI Proof V1
- Release Lock

---

## Can users clone and use AION ICLI now?

Yes.

Users can clone the repository and run AION ICLI locally with the included launchers.

Supported public launchers:

- [Windows CMD launcher](../bin/aion.cmd)
- [PowerShell launcher](../bin/aion.ps1)
- [POSIX launcher](../bin/aion)
- [Root PowerShell launcher](../aion.ps1)

Current install path:

    git clone https://github.com/VerifywithAION/aion-icli.git
    cd aion-icli
    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

Current status:

- clone/install/run is validated
- CLI launcher use is validated
- connector stack is validated
- generated outputs remain ignored by Git

Not included yet:

- standalone downloadable Windows .exe
- signed installer
- GitHub Releases binary package

Those should be handled as a future packaging milestone.

---

## Product principle

    Governance should be felt, not seen.

AION ICLI should feel like a careful operator that helps users act with proof, receipts, and boundaries.
