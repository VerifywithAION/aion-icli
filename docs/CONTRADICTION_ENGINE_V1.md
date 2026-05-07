# AION ICLI Contradiction Engine V1

Contradiction Engine V1 detects mismatch between claims and local evidence.

## What it checks

- roadmap completion vs verifier presence
- roadmap completion vs docs presence
- wiring PASS vs evidence layer presence
- evidence overclaim (RELEASE_PACKAGED/FRESH_CLONE_PROVEN without proof)
- release package stale relative to main (accepted caveat)
- receipt engine-used flags vs state file existence

## Severity
- INFO
- LOW
- MEDIUM
- HIGH
- CRITICAL

## Status
- OPEN
- ACCEPTED_CAVEAT
- RESOLVED
- NEEDS_REVIEW

## Key accepted caveat

`release_package_stale_relative_to_main` can be valid while main advances faster than public ZIP refresh.

## Diagnostics

When diagnostics is ON and contradiction engine is used:
- Contradiction engine used
- Contradictions found
- Open contradictions
- Accepted caveats
- Highest severity
- Contradiction paths

## Receipt fields

- contradiction_engine_used
- contradictions_found
- open_contradictions
- accepted_caveats
- highest_severity
- contradiction_index_path
- contradiction_summary

Related layers: Introspection Gate V1, Evidence Engine V1, Living Proof Graph V1.

Expected marker:

AION_CONTRADICTION_ENGINE_V1_VERIFY_OK
