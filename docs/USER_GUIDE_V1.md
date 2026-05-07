# AION ICLI User Guide V1

## What is AION ICLI?

AION ICLI means Interactive Command Line Intelligence.

It is a local-first command-line interface for governed AI and system actions.

AION ICLI helps users evaluate actions before trust by making the important parts visible:

- what was requested
- whether the action stayed local
- whether the network was used
- whether files were changed
- whether execution happened
- whether a receipt was written
- whether the result can be reviewed later

AION ICLI is not another chatbot.

AION ICLI is a governed execution surface.

Its purpose is to make AI, tools, APIs, SDKs, scripts, and model request flows more inspectable, more constrained, more receipt-backed, and easier to verify.

## Core idea

Most AI tools answer.

AION ICLI answers with governance context.

The basic pattern is:

    request -> local review -> visible boundaries -> receipt -> verification

The principle is:

    Governance should be felt, not seen.

That means AION should help like a careful operator, not interrupt like a noisy firewall.

## Quick start from ZIP

1. Download or extract the public ZIP package.
2. Open PowerShell inside the extracted folder.
3. Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1

4. Ask AION:

    .\bin\aion.cmd "Who are you, AION?"

Expected result:

    Boundary > LOCAL_ONLY
    Network  > NOT_USED
    Mutation > NOT_PERFORMED
    Receipt  > receipts\local\aion_cli_receipt_v1.json

## Quick start from GitHub clone

    git clone https://github.com/VerifywithAION/aion-icli.git
    cd aion-icli
    powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
    .\bin\aion.cmd "Who are you, AION?"

## What AION ICLI can do today

### 1. Run locally from the command line

AION ICLI can run from included launchers:

- Windows CMD: `bin\aion.cmd`
- PowerShell: `bin\aion.ps1`
- root PowerShell launcher: `aion.ps1`
- POSIX shell launcher: `bin/aion`

Example:

    .\bin\aion.cmd "Who are you, AION?"

### 2. Answer with visible boundaries

AION ICLI shows the operational boundary of the answer.

Example output:

    Boundary > LOCAL_ONLY
    Network  > NOT_USED
    Mutation > NOT_PERFORMED
    Receipt  > receipts\local\aion_cli_receipt_v1.json

This tells the user that the answer stayed local, did not use the network, did not mutate files, and wrote a receipt.

### 3. Write local receipts

AION ICLI writes a local receipt after CLI use.

Receipt path:

    receipts\local\aion_cli_receipt_v1.json

The receipt records:

- receipt type
- UTC timestamp
- prompt
- response
- boundary
- network status
- mutation status
- execution status
- governance tone

Example receipt fields:

    boundary: LOCAL_ONLY
    network: NOT_USED
    mutation: NOT_PERFORMED
    execution: NOT_PERFORMED
    governance_tone: felt_not_seen

### 4. Verify public safety

AION ICLI includes a public-safe verifier.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1

Expected marker:

    AION_ICLI_PUBLIC_SAFE_VERIFY_OK

This checks the public CLI surface, launchers, visible boundaries, and local receipt behavior.

### 5. Verify release lock

AION ICLI includes a release lock verifier.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_RELEASE_LOCK_V1.ps1

Expected marker:

    AION_PUBLIC_RELEASE_LOCK_V1_VERIFY_OK

This confirms the release baseline still satisfies the public lock conditions.

### 6. Use the local governance proxy

AION ICLI includes a local governance proxy demo.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_LOCAL_GOVERNANCE_PROXY_V1.ps1

Expected marker:

    AION_LOCAL_GOVERNANCE_PROXY_V1_VERIFY_OK

This demonstrates how structured requests can be reviewed locally and produce governed outputs.

### 7. Use Connector Policy V2

AION ICLI includes connector policy documents and examples.

Read:

- [Connector Policy V2](CONNECTOR_POLICY_V2.md)
- [Connector SDK Contract V1](CONNECTOR_SDK_CONTRACT_V1.md)

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_POLICY_V2.ps1

Expected marker:

    AION_CONNECTOR_POLICY_V2_VERIFY_OK

This shows how apps, SDKs, APIs, and model request envelopes can connect to AION through public-safe request contracts.

### 8. Review API request envelopes without live API calls

AION ICLI can model API-style requests in dry-run mode.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_API_ADAPTER_DRY_RUN_V1.ps1

Expected marker:

    AION_SAFE_API_ADAPTER_DRY_RUN_V1_VERIFY_OK

This proves:

- API request envelopes can be reviewed before execution
- no live API call is made
- no network is used by default
- receipts are generated locally
- generated outputs stay outside the committed public surface

### 9. Review model request envelopes without provider calls

AION ICLI can model AI/model-provider requests in dry-run mode.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1

Expected marker:

    AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_VERIFY_OK

This proves:

- model request envelopes can be reviewed before provider execution
- no OpenAI, Anthropic, Gemini, Ollama, or other provider call is made
- no provider key is required
- no network is used by default
- receipts are generated locally

### 10. Use SDK-style request examples

AION ICLI includes SDK-style JSON examples.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SDK_EXAMPLES_V1.ps1

Expected marker:

    AION_SDK_EXAMPLES_V1_VERIFY_OK

This proves:

- developers can submit SDK-style request JSON
- AION can review it locally
- AION can return a human-friendly governance result
- AION can write a receipt
- AION does not need to expose internal implementation to provide governance

### 11. Compare governed vs ungoverned behavior

AION ICLI includes a governed-vs-ungoverned CLI proof.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1.ps1

Expected marker:

    AION_GOVERNED_VS_UNGOVERNED_CLI_PROOF_V1_OK

The proof compares:

- ungoverned output, where trust details are invisible
- governed AION output, where boundary, network use, mutation behavior, receipt, and replay evidence are visible

### 12. Verify the connector stack acceptance report

AION ICLI includes a public proof report.

Read:

- [Connector Stack Acceptance Report V1](../reports/CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md)

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.ps1

Expected marker:

    AION_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1_VERIFY_OK

This report proves the public connector stack works from the public repo.

### 13. Verify the public install package

AION ICLI includes a ZIP package verifier.

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1

Expected marker:

    AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK

This verifier works in two modes:

- source repository mode
- extracted ZIP mode

It confirms the package has required files, excludes forbidden paths, and supports runtime-generated receipts and generated output folders after use.

### 14. Run from public ZIP package

AION ICLI can be distributed as a ZIP package.

Current package path in repo:

    dist/aion-icli-public-install-package-v1.zip

The ZIP includes:

- launchers
- CLI source entrypoint
- docs
- examples
- schemas
- scripts
- reports
- verifiers

The ZIP does not include:

- standalone Windows `.exe`
- signed installer
- private credentials
- provider keys
- hidden integrations
- internal/private AION systems

## Public install package

Current public install package:

    dist/aion-icli-public-install-package-v1.zip

Latest verified package SHA256:

    29142EDA65003AB91F4BC3AE7C580C9821576AF595409C770913A2B5FF52E0C1

Use the latest report for current package metadata:

- [Public Install Package V1 Report](../reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md)

## What AION ICLI does not do by default

AION ICLI does not:

- call external APIs by default
- call model providers by default
- require provider keys
- use network by default
- mutate files by default
- execute live user actions by default
- ship private credentials
- ship hidden integrations
- expose internal/private AION implementation details
- act as a standalone Windows `.exe` yet

## What AION ICLI is for

AION ICLI is for users and developers who want a public, local-first governance layer around AI and system actions.

It is useful when you want to ask:

- What is this action trying to do?
- Did it stay local?
- Did it use the network?
- Did it mutate files?
- Did it call a model?
- Did it call an API?
- Was a receipt written?
- Can this be reviewed later?
- Can this request be connected through a safe public contract?

## Developer connection model

Developers can think of AION ICLI as a governance interface.

The basic pattern:

    app/tool/agent -> request JSON -> AION review -> result -> receipt

The public connector surface is designed for:

- SDK clients
- API clients
- model request envelopes
- automation tools
- local CLI workflows
- review-first execution flows

## Example developer request flow

1. Create a structured request JSON.
2. Submit it through a public connector pattern.
3. Let AION review the request locally.
4. Inspect the result.
5. Inspect the receipt.
6. Only then decide whether a real system should execute.

## Example: API request envelope

Read:

    examples\api-adapter\api_request_read_dryrun_v1.json

Verify:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_API_ADAPTER_DRY_RUN_V1.ps1

## Example: model request envelope

Read:

    examples\model-adapter\model_request_safe_dryrun_v1.json

Verify:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1

## Example: SDK request envelope

Read:

    examples\sdk\sdk_request_safe_read_v1.json

Verify:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SDK_EXAMPLES_V1.ps1

## How to inspect a receipt

After running AION:

    Get-Content -Raw .\receipts\local\aion_cli_receipt_v1.json

Typical receipt:

    {
      "receipt_type": "aion_cli_receipt_v1",
      "boundary": "LOCAL_ONLY",
      "network": "NOT_USED",
      "mutation": "NOT_PERFORMED",
      "execution": "NOT_PERFORMED",
      "governance_tone": "felt_not_seen"
    }

## How to verify everything quickly

Run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_SAFE.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_POLICY_V2.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1

For full connector checks, run:

    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_API_ADAPTER_DRY_RUN_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SAFE_MODEL_ADAPTER_DRY_RUN_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_SDK_EXAMPLES_V1.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.ps1

## Current proof markers

A healthy public install can produce:

    AION_ICLI_INSTALL_PREVIEW_OK
    AION_ICLI_PUBLIC_SAFE_VERIFY_OK
    AION_CONNECTOR_POLICY_V2_VERIFY_OK
    AION_SAFE_API_ADAPTER_DRY_RUN_V1_VERIFY_OK
    AION_SAFE_MODEL_ADAPTER_DRY_RUN_V1_VERIFY_OK
    AION_SDK_EXAMPLES_V1_VERIFY_OK
    AION_CONNECTOR_STACK_ACCEPTANCE_REPORT_V1_VERIFY_OK
    AION_PUBLIC_INSTALL_PACKAGE_V1_VERIFY_OK

## Human explanation

AION ICLI is like a careful operator sitting between intent and execution.

It does not just say:

    Sure, do it.

It says:

    I reviewed this locally.
    I did not use the network.
    I did not mutate files.
    I wrote a receipt.
    You can verify what happened.

That is the difference between helpful-sounding output and governed execution.


## Interactive Mode V1

AION ICLI can also run as a persistent local session.

Start interactive mode:

    .\bin\aion.cmd

Then use commands such as:

    help
    receipt
    boundary
    verify
    exit

Read:

- [Interactive Mode V1](INTERACTIVE_MODE_V1.md)


## Capability Router V1

AION ICLI now exposes public-safe capability commands inside interactive mode:

    capabilities
    preflight
    creative
    intuition
    cortex
    connectors
    receipts
    verify
    next

Each capability remains local-first, no-network by default, no-mutation by default, no-execution by default, and receipt-backed.

Read:

- [Capability Router V1](CAPABILITY_ROUTER_V1.md)

## Voice Layer V1

ICLI now separates internal routing from default visible language:

- Default visible output: natural operator-facing AION response.
- Proof footer remains visible:
  - `Proof: local-only · no network · no mutation · no execution · receipt written`
- Internal capability routing remains in receipts and diagnostics.
- Diagnostics commands:
  - `diagnostics on`
  - `diagnostics off`
  - `diagnostics`

Read:

- [Voice Layer V1](VOICE_LAYER_V1.md)

## Adaptive Reasoning Layer V1

ICLI now adapts responses to what the operator actually wrote.

Extracted local signals:

- subject
- urgency
- missing evidence
- risk lens

Behavior:

- default output stays natural and operator-facing
- proof footer remains visible
- diagnostics mode can reveal internal signals and routing

Read:

- [Adaptive Reasoning Layer V1](ADAPTIVE_REASONING_LAYER_V1.md)

## Roadmap after User Guide V1

Recommended next milestones:

1. Fresh user guide acceptance test
2. Public release tag
3. GitHub Release draft
4. Optional Windows EXE packaging
5. Signed installer later
6. richer connector examples
7. richer receipt viewer
8. optional local model adapter integration

## Status

LOCKED as AION ICLI User Guide V1.



## Governance Brain Adapter V1

AION can answer from local evidence instead of fixed response tables. It inspects public-safe repo artifacts such as docs, reports, schemas, examples, packaging metadata, verifier names, and local receipt state.

See: docs/GOVERNANCE_BRAIN_ADAPTER_V1.md


## Governance Brain Integration Fix V1

This fix ensures release-state answers consistently use local governance evidence in normal and diagnostics modes.

Read: docs/GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.md


## Memory Scar Engine V1

AION now keeps public-safe scar memory for failure patterns and future rules (trigger, harm, repair, future_rule).

Read: docs/MEMORY_SCAR_ENGINE_V1.md


## Roadmap and Wiring State V1

- docs/AION_ICLI_ROADMAP_STATE_V1.md
- docs/AION_ICLI_NEXT_8_BUILDS_V1.md
- docs/AION_ICLI_SYSTEM_WIRING_REPORT_V1.md

