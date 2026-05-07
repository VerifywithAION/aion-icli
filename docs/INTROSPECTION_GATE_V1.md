# AION ICLI Introspection Gate V1

Introspection Gate V1 is a local self-audit layer that checks answers before output.

It prevents overclaims, enforces boundary-safe phrasing, and repairs weak/unsafe responses.

## Core checks

- has_proof_footer in normal mode
- no diagnostics leak in normal mode
- no live provider claims
- no execution/autonomy claims
- no consciousness claims
- no release overclaim
- artifact-safety claims require artifact inspection
- evidence claims require Evidence Engine
- proof claims require receipt/verifier grounding
- missing artifact prompts must ask for artifact path
- local boundary preserved

## Repair behavior

When checks fail, answers are rewritten to safe grounded forms, for example:
- "No artifact, no judgment."
- "ROADMAP_WIRED, not RELEASE_PACKAGED."
- "No live provider call executes here by default."

## Diagnostics

With diagnostics ON, output shows:
- Introspection gate used
- Introspection passed
- Findings
- Repairs applied
- Risk level

## Receipt fields

- introspection_used
- introspection_passed
- introspection_findings
- introspection_repairs_applied
- introspection_risk_level

Relationship: Evidence Engine V1 + Living Proof Graph V1 + Memory Scar Engine V1.

Expected marker:

AION_INTROSPECTION_GATE_V1_VERIFY_OK
