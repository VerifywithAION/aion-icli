# AION ICLI Living Proof Graph V1

Living Proof Graph V1 is AION ICLI's public-safe local relational proof memory.

It connects artifacts, receipts, decisions, scars, verifiers, docs, roadmap state, wiring state, and release/package evidence.

## Why it exists

Artifact inspection gives local perception. Living Proof Graph gives relationship memory:

- Artifact -> inspects_artifact -> Receipt
- Receipt -> supports_decision -> Decision
- MemoryScar -> constrains_decision -> Decision
- Layer -> documented_by -> Doc
- Layer -> verified_by -> Verifier
- Layer -> wired_by -> WiringReport
- RoadmapState -> points_to_next -> NextBuild
- Release -> contains_package -> Package
- Package -> has_sha256 -> Artifact

## Node types

- Layer
- Doc
- Verifier
- Receipt
- Artifact
- MemoryScar
- RoadmapState
- WiringReport
- Release
- Package
- Decision
- NextBuild

## Edge types

- documented_by
- verified_by
- wired_by
- emits_receipt
- records_scar
- inspects_artifact
- supports_decision
- constrains_decision
- points_to_next
- contains_package
- has_sha256
- supersedes
- depends_on

## Local graph state files

- .aion_public/proof_graph/proof_nodes_v1.json
- .aion_public/proof_graph/proof_edges_v1.json
- .aion_public/proof_graph/proof_graph_summary_v1.md
- .aion_public/proof_graph/proof_graph_latest_v1.json

## Source files inspected

- README.md
- docs/*.md
- scripts/VERIFY_*.ps1
- .aion_public/scars/scars_seed.jsonl
- .aion_public/roadmap/roadmap_state_v1.json
- .aion_public/wiring/system_wiring_v1.json
- .aion_public/evolution/evolution_ledger_seed.jsonl
- packaging/public-install/public_install_package_v1.manifest.json
- reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md
- receipts/local/aion_cli_receipt_v1.json (if present)
- examples/inspection/*

## Safety constraints

- local-only
- no network
- no mutation
- no execution
- no external graph backend
- no Graphiti/mem0 runtime

## Diagnostics fields

When diagnostics is ON and proof graph answers are used:

- Living proof graph used
- Nodes count
- Edges count
- Source files consulted
- Graph path

## Receipt fields

When proof graph answers are used, receipt includes:

- living_proof_graph_used
- proof_graph_paths
- proof_graph_node_count
- proof_graph_edge_count
- graph_summary

Expected marker:

AION_LIVING_PROOF_GRAPH_V1_VERIFY_OK
