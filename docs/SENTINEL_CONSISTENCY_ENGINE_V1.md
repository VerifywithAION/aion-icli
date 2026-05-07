# Sentinel Consistency Engine V1

AION Sentinel Consistency Engine V1 is the local health monitor for the full public-safe organism.

It does not repair automatically. It reports current consistency state and next required action.

## Health states

- HEALTHY
- DEGRADED_ACCEPTED_CAVEAT
- DEGRADED_NEEDS_REPAIR
- INCONSISTENT
- BLOCKED
- UNKNOWN

## Monitored surfaces

- Roadmap state
- Wiring state
- Contradiction state
- Evidence state
- Self-repair plan
- Living proof graph
- Memory scars
- Verifier presence

## Accepted caveat vs blocking failure

Accepted caveats are tracked degradation, not hard failure.
A blocking failure requires critical contradiction severity.

## Diagnostics

When `diagnostics on` is active and Sentinel is used, AION shows:

- Sentinel used
- Sentinel state
- Blocking
- Highest severity
- Accepted caveats
- Open contradictions
- Repair items
- Next required action
- State path

## Receipt fields

Sentinel writes receipt fields:

- `sentinel_used`
- `sentinel_state`
- `blocking`
- `highest_severity`
- `accepted_caveats`
- `open_contradictions`
- `critical_contradictions`
- `repair_items`
- `next_required_action`
- `sentinel_state_path`

Boundary remains local-only:

- `boundary = LOCAL_ONLY`
- `network = NOT_USED`
- `mutation = NOT_PERFORMED`
- `execution = NOT_PERFORMED`

Expected marker:

`AION_SENTINEL_CONSISTENCY_ENGINE_V1_VERIFY_OK`
