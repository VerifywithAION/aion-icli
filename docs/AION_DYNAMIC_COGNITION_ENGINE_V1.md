# AION Dynamic Cognition Engine V1

## Purpose
AION Dynamic Cognition Engine V1 upgrades living responses from repetitive templates into structured recursive cognition. It keeps truth constraints and governance posture while generating prompt-specific strategic analysis.

## Callable Surface
- `analyze_dynamic_cognition(prompt: str, context: dict | None = None) -> dict`
- CLI: `python .\src\aion_dynamic_cognition_engine.py --input .\path\to\payload.json`

## Required Output Fields
- `engine`
- `detected_surface_question`
- `inferred_hidden_goal`
- `hidden_assumptions`
- `competing_theories`
- `strongest_theory`
- `rejected_theories`
- `contradiction_pressure`
- `nonobvious_insight`
- `dynamic_reframe`
- `next_best_question`
- `governed_answer`
- `continuity_update`
- `boundary`, `network`, `mutation`, `execution`
- receipt metadata: `receipt_id`, `receipt_path`, `receipt_abs_path`, `receipt_written`, `receipt_sha256`, `repo_root`

## Behavior Model
1. Generate at least three competing theories for each prompt.
2. Rank by plausibility and usefulness.
3. Reject weaker theories with explicit reasons.
4. Produce a non-obvious insight and dynamic reframe tied to the prompt.
5. Produce a specific next-best-question and continuity update.
6. Preserve local governance posture:
   - `LOCAL_ONLY`
   - `NOT_USED`
   - `NOT_PERFORMED`

## Safety
- No external APIs.
- No network calls.
- No autonomous execution.
- No production mutation.
- Receipt-only mutation under `receipts/dynamic_cognition/`.

## Integration
`src/aion_living_intelligence_kernel.py` uses the Dynamic Cognition Engine for living prompts and composes the CLI-facing answer from:
- strongest theory / direct truth
- hidden assumptions
- non-obvious insight
- dynamic reframe
- next-best-question
- governed answer
- next admissible move

## Run
- Verify: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_DYNAMIC_COGNITION_ENGINE_V1.ps1`
- Demo: `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_DYNAMIC_COGNITION_ENGINE_V1_DEMO.ps1`
