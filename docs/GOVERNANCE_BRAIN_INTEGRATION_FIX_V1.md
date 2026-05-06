# AION Governance Brain Integration Fix V1

Expected marker: `AION_GOVERNANCE_BRAIN_INTEGRATION_FIX_V1_VERIFY_OK`

## What was inconsistent

Governance Brain Adapter V1 could answer release questions in normal mode, but diagnostics mode could bypass governance-brain evidence and show fallback cortex output.

## What is fixed

- Release-state questions now use governance brain in both normal and diagnostics mode.
- Diagnostics now accurately reports:
  - `Governance brain used > true`
  - `Artifacts consulted > ...`
  - `Evidence summary > ...`
- Legacy direct command behavior remains for explicit command-style prompts.

## Release metadata parsing

The release answer now parses local evidence from:

- `packaging/public-install/public_install_package_v1.manifest.json`
- `reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md`
- `docs/GITHUB_RELEASE_V1_DRAFT.md`
- `reports/GITHUB_RELEASE_V1_CHECKLIST.md`

Extracted when available:

- release tag
- package zip path
- package SHA256
- package target head
- release docs head (if present)

If JSON parse is unavailable, markdown regex fallback is used.

## Safety boundary

- local-only evidence reads
- no network calls
- no provider calls
- no autonomous execution
- no canonical mutation execution

## Receipt behavior

When governance brain is used, receipt includes:

- `governance_brain_used: true`
- `artifacts_consulted: [...]`
- `evidence_summary: ...`
