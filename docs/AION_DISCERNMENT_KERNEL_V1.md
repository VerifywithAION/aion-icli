# AION Discernment Kernel V1

## Core Thesis
Discernment separates negotiable autonomy from non-negotiable human trust boundaries before action.

## Callable
- `evaluate_discernment(payload: dict) -> dict`

## Input Schema
- `scenario`
- `human_intent`
- `proposed_autonomy`
- `possible_consequence`
- `human_boundaries`
- `non_negotiables`
- `requested_execution`
- `evidence.verifier|rollback|human_confirmation|receipt`

## Output
- `engine: AION_DISCERNMENT_KERNEL_V1`
- `negotiable_autonomy`
- `non_negotiable_boundaries`
- `boundary_violations`
- `discernment_verdict: SAFE_TO_DELEGATE|ASK_HUMAN_FIRST|HARD_STOP|REVIEW_ONLY`
- `one_question_that_matters`
- `safe_next_step`
- `companion_language`
- backend and receipt trace fields

## Core Rules
- Execution + unverified non-negotiables => `HARD_STOP` or `ASK_HUMAN_FIRST`
- Trading without max loss => `ASK_HUMAN_FIRST`
- Home/robot without forbidden actions => `ASK_HUMAN_FIRST`
- Shopping without budget/allergy/substitution => `ASK_HUMAN_FIRST`
- Coding without verifier/rollback => `HARD_STOP`
- Mirror/general => trust-boundary clarification

## Posture
- `LOCAL_ONLY`
- `NOT_USED`
- `NOT_PERFORMED`

## Run
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_DISCERNMENT_KERNEL_V1_DEMO.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_DISCERNMENT_KERNEL_V1.ps1`
