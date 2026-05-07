# AION ICLI System Wiring Report V1

Current head: 5532ae2

Each layer below is checked for runtime/docs/verifier/linkage and public-safe boundaries.

| Layer | Runtime/File | Docs | Verifier | CLI wired | Receipt wired | Public-safe |
|---|---|---|---|---|---|---|
| Public Safe Verifier | scripts/VERIFY_PUBLIC_SAFE.ps1 | docs/PUBLIC_BOUNDARY.md | VERIFY_PUBLIC_SAFE.ps1 | n/a | n/a | true |
| Public Install Package V1 | packaging/public-install/public_install_package_v1.manifest.json | docs/PUBLIC_INSTALL_PACKAGE_V1.md | VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1 | n/a | n/a | true |
| User Guide V1 | docs/USER_GUIDE_V1.md | docs/USER_GUIDE_V1.md | VERIFY_USER_GUIDE_V1.ps1 | n/a | n/a | true |
| Interactive Mode V1 | src/aion_cli_entry.py | docs/INTERACTIVE_MODE_V1.md | VERIFY_INTERACTIVE_MODE_V1.ps1 | true | true | true |
| Capability Router V1 | src/aion_cli_entry.py | docs/CAPABILITY_ROUTER_V1.md | VERIFY_CAPABILITY_ROUTER_V1.ps1 | true | true | true |
| Voice Layer V1 | src/aion_cli_entry.py | docs/VOICE_LAYER_V1.md | VERIFY_VOICE_LAYER_V1.ps1 | true | true | true |
| Adaptive Reasoning Layer V1 | src/aion_cli_entry.py | docs/ADAPTIVE_REASONING_LAYER_V1.md | VERIFY_ADAPTIVE_REASONING_LAYER_V1.ps1 | true | true | true |
| Governance Brain Adapter V1 | src/aion_cli_entry.py | docs/GOVERNANCE_BRAIN_ADAPTER_V1.md | VERIFY_GOVERNANCE_BRAIN_ADAPTER_V1.ps1 | true | true | true |
| Governance Brain Integration Fix V1 | src/aion_cli_entry.py | docs/GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.md | VERIFY_GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.ps1 | true | true | true |
| Memory Scar Engine V1 | src/aion_cli_entry.py + .aion_public/* | docs/MEMORY_SCAR_ENGINE_V1.md | VERIFY_MEMORY_SCAR_ENGINE_V1.ps1 | true | true | true |
| Artifact Inspection Runner V1 | src/aion_cli_entry.py + examples/inspection/* | docs/ARTIFACT_INSPECTION_RUNNER_V1.md | VERIFY_ARTIFACT_INSPECTION_RUNNER_V1.ps1 | true | true | true |
| Living Proof Graph V1 | src/aion_cli_entry.py + .aion_public/proof_graph/* | docs/LIVING_PROOF_GRAPH_V1.md | VERIFY_LIVING_PROOF_GRAPH_V1.ps1 | true | true | true |
| Evidence Engine V1 | src/aion_cli_entry.py + .aion_public/evidence/* | docs/EVIDENCE_ENGINE_V1.md | VERIFY_EVIDENCE_ENGINE_V1.ps1 | true | true | true |
| Introspection Gate V1 | src/aion_cli_entry.py + .aion_public/introspection/* | docs/INTROSPECTION_GATE_V1.md | VERIFY_INTROSPECTION_GATE_V1.ps1 | true | true | true |
| Contradiction Engine V1 | src/aion_cli_entry.py + .aion_public/contradictions/* | docs/CONTRADICTION_ENGINE_V1.md | VERIFY_CONTRADICTION_ENGINE_V1.ps1 | true | true | true |
| Self-Repair Planner V1 | src/aion_cli_entry.py + .aion_public/self_repair/* | docs/SELF_REPAIR_PLANNER_V1.md | VERIFY_SELF_REPAIR_PLANNER_V1.ps1 | true | true | true |
| Sentinel Consistency Engine V1 | src/aion_cli_entry.py + .aion_public/sentinel/* | docs/SENTINEL_CONSISTENCY_ENGINE_V1.md | VERIFY_SENTINEL_CONSISTENCY_ENGINE_V1.ps1 | true | true | true |
| Offline AION CLI Bundle V1.1.0 | dist/aion-icli-offline-bundle-v1.1.0.zip + packaging/offline-bundle-v1.1.0/* | docs/OFFLINE_AION_CLI_BUNDLE_V1_1_0.md | VERIFY_OFFLINE_AION_CLI_BUNDLE_V1_1_0.ps1 + VERIFY_OFFLINE_AION_CLI_BUNDLE_V1_1_0_FRESH_INSTALL.ps1 | true | true | true |

Public-safe boundary remains: LOCAL_ONLY, network NOT_USED, mutation NOT_PERFORMED, execution NOT_PERFORMED.
