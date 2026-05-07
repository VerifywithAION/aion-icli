# AION ICLI Evidence Engine V1

Evidence Engine V1 classifies proof strength for each layer.

## Evidence levels

- MISSING
- CLAIM_ONLY
- DOC_ONLY
- RECEIPT_ONLY
- VERIFIER_PRESENT
- VERIFIER_MARKER_PRESENT
- ROADMAP_WIRED
- RELEASE_PACKAGED
- FRESH_CLONE_PROVEN
- ADMISSIBLE

It separates claims from admissible proof. Example outcomes:
- "This layer has docs and verifier, but no rebuilt public ZIP proof."
- "This claim is ROADMAP_WIRED, not RELEASE_PACKAGED."

## Sources
- docs/*.md
- scripts/VERIFY_*.ps1
- README.md
- docs/USER_GUIDE_V1.md
- .aion_public/roadmap/roadmap_state_v1.json
- .aion_public/wiring/system_wiring_v1.json
- .aion_public/proof_graph/*
- .aion_public/scars/scars_seed.jsonl
- .aion_public/evolution/evolution_ledger_seed.jsonl
- reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md
- packaging/public-install/public_install_package_v1.manifest.json
- dist/aion-icli-public-install-package-v1.zip (if present)
- receipts/local/aion_cli_receipt_v1.json (if present)

## Safety constraints
- local-only
- no network
- no mutation
- no execution
- no dependency installs

## Diagnostics fields
- Evidence engine used
- Evidence items evaluated
- Highest level
- Weakest layers
- Evidence paths

## Receipt fields
- evidence_engine_used
- evidence_items_evaluated
- evidence_index_path
- evidence_summary_out
- strongest_evidence_level
- weakest_layers

Related layers: Living Proof Graph V1 + roadmap/wiring verifiers.

Expected marker:

AION_EVIDENCE_ENGINE_V1_VERIFY_OK
