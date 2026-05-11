# AION Sentinel + Contradiction V1 Demo Report

Generated at UTC: 2026-05-11T20:38:31Z

## Scenarios
- claim: ready_to_ship
  - consistency_status: CONTRADICTION
  - severity: HIGH
  - governance_decision: BLOCK
  - contradictions: claim_ready_to_ship_without_verifier, claim_ready_to_ship_without_receipt, claim_ready_to_ship_with_missing_controls
- claim: safe_to_execute
  - consistency_status: CONTRADICTION
  - severity: HIGH
  - governance_decision: BLOCK
  - contradictions: claim_safe_to_execute_but_decision_block
- claim: allowed
  - consistency_status: CONSISTENT
  - severity: LOW
  - governance_decision: ALLOW
  - contradictions: 

Marker: AION_SENTINEL_CONTRADICTION_V1_DEMO_OK
