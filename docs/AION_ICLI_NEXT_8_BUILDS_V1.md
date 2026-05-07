# AION ICLI Next 8 Builds V1

## 1) Artifact Inspection Runner V1
- Purpose: inspect repo artifacts with deterministic local checks.
- Why: grounds decisions in visible evidence.
- Expected files: src/aion_artifact_inspection_runner_v1.py, verifier script, docs, receipt seed.
- Verifier marker: AION_ARTIFACT_INSPECTION_RUNNER_V1_VERIFY_OK
- Safety: local-only, no provider calls, no mutation execution.
- Wiring: feeds evidence into governance brain and receipts.

## 2) Living Proof Graph V1
- Purpose: connect proofs, verifiers, receipts, and scars in one local graph.
- Why: supports causal recall and contradiction checks.
- Expected files: graph seed/update runtime + proof graph docs.
- Verifier marker: AION_LIVING_PROOF_GRAPH_V1_VERIFY_OK
- Safety: local-only graph state.
- Wiring: memory scar + governance brain + release evidence join.

## 3) Evidence Engine V1
- Purpose: normalize artifact evidence into reusable evidence packets.
- Why: reduces ad-hoc parsing across features.
- Expected files: evidence schema/runtime/verifier/docs.
- Verifier marker: AION_EVIDENCE_ENGINE_V1_VERIFY_OK
- Safety: no external fetch, strict path policy.
- Wiring: upstream of governance brain + contradiction engine.

## 4) Introspection Gate V1
- Purpose: self-check claims against evidence before output.
- Why: prevent false confidence.
- Expected files: introspection gate runtime/verifier/docs.
- Verifier marker: AION_INTROSPECTION_GATE_V1_VERIFY_OK
- Safety: local-only guardrail.
- Wiring: wraps response path before final output.

## 5) Contradiction Engine V1
- Purpose: detect contradiction between claim/evidence/receipt.
- Why: route warnings and blocks deterministically.
- Expected files: contradiction engine runtime/verifier/docs.
- Verifier marker: AION_CONTRADICTION_ENGINE_V1_VERIFY_OK
- Safety: no execution side effects.
- Wiring: feeds diagnostics and scar updates.

## 6) Self-Repair Planner V1
- Purpose: propose repair plans for recurring scar patterns.
- Why: convert failures into governed remediation steps.
- Expected files: planner runtime/verifier/docs.
- Verifier marker: AION_SELF_REPAIR_PLANNER_V1_VERIFY_OK
- Safety: plan-only, no autonomous patching.
- Wiring: consumes scars + contradiction outputs.

## 7) Sentinel Consistency Engine V1
- Purpose: enforce cross-surface consistency (docs/verifiers/runtime claims).
- Why: detect roadmap drift early.
- Expected files: sentinel runtime/verifier/docs.
- Verifier marker: AION_SENTINEL_CONSISTENCY_ENGINE_V1_VERIFY_OK
- Safety: local static checks only.
- Wiring: guards release readiness.

## 8) Offline AION CLI Bundle V1 / v1.1.0 package
- Purpose: rebuild public package with integrated intelligence stack.
- Why: ship verified capability set as one offline bundle.
- Expected files: packaging manifest/report/release docs.
- Verifier marker: AION_OFFLINE_CLI_BUNDLE_V1_VERIFY_OK
- Safety: no provider dependencies required.
- Wiring: final delivery proof layer.
