# AION Living Intelligence Kernel V1

AION Living Intelligence Kernel V1 wires continuity-driven cognitive governance behavior into the public-safe CLI runtime.

## What this kernel does

Given a deep-investigation style prompt, the kernel produces structured living-intelligence output:

1. `direct_truth`
2. `detected_intent`
3. `hidden_assumptions`
4. `contradictions_or_uncertainties`
5. `root_cause_hypothesis`
6. `counterfactuals`
7. `next_best_question`
8. `dynamic_theory_update`
9. `governed_answer`
10. `next_admissible_move`

## Runtime integration

`src/aion_cli_entry.py` routes prompts starting with:

- `ask aion`
- `think`
- `investigate`
- `what is the core truth`
- `what am i missing`
- `what is the next best question`
- `analyze this deeply`

to `aion_living_intelligence_kernel.analyze_living_request(prompt)`.

## Public-safe guarantees

- `LOCAL_ONLY`
- `network=NOT_USED`
- `mutation=NOT_PERFORMED`
- `execution=NOT_PERFORMED`
- no external APIs
- no autonomous execution
- no production mutation

## Receipts

Kernel receipts are written under:

- `receipts/living_intelligence/`

and include:

- `receipt_written`
- `receipt_abs_path`
- `receipt_sha256`
- `repo_root`

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_LIVING_INTELLIGENCE_KERNEL_V1_DEMO.ps1
```

Expected marker:

- `AION_LIVING_INTELLIGENCE_KERNEL_V1_DEMO_OK`

## Verifier

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_LIVING_INTELLIGENCE_KERNEL_V1.ps1
```

Expected marker:

- `AION_LIVING_INTELLIGENCE_KERNEL_V1_VERIFY_OK`
