# AION ICLI Self-Repair Planner V1

Self-Repair Planner V1 is review-only.

It proposes governed local repair plans from contradictions/evidence/roadmap/wiring gaps and does not automatically modify files.

## Source inputs
- contradiction index
- evidence index
- roadmap state
- wiring state

## Repair item schema
- repair_id
- source_type
- severity
- status
- affected_layer
- problem
- why_it_matters
- recommended_steps
- forbidden_steps
- verification_steps
- rollback_notes
- expected_marker
- public_safe

## Stale package repair
Includes a canonical repair item:
`rebuild_public_offline_bundle_v1_1_0`.

Key constraints:
- do not overwrite v1.0.0
- do not claim fresh-clone proof before running it
- keep provider calls disabled

## Diagnostics
- Self-repair planner used
- Repair items
- Highest severity
- Ready for review
- Blocked
- Plan path

## Receipt fields
- self_repair_planner_used
- repair_plan_path
- repair_items
- highest_severity
- ready_for_review
- blocked
- recommended_next_action

Expected marker:

AION_SELF_REPAIR_PLANNER_V1_VERIFY_OK
