# AION Creativity + Intuition V1

AION Creativity + Intuition V1 turns weak governance signals into bounded, safe next-action suggestions.

## Intuition in AION

Intuition is a **heuristic signal**, not truth. It combines contradictions, memory matches, missing controls, risk signals, governance state, evidence completeness, and proof-gap data.

## Creativity in AION

Creativity is constrained generation of safer next steps (repair ideas, verifier prompts, evidence capture, and recheck plans). It never authorizes execution.

## Input schema (V1)

```json
{
  "source": "Preflight|Sentinel|Memory|DomainGovernor|Introspection|Manual",
  "context": "public-safe summary",
  "signals": {
    "contradictions": 1,
    "memory_matches": 2,
    "missing_controls": ["verifier", "rollback"],
    "risk_signals": ["execution", "funds_at_risk"],
    "domain": "wallet",
    "governance_decision": "BLOCK",
    "evidence_complete": false,
    "proof_graph_missing_count": 0
  }
}
```

## Output schema (V1)

- `engine`: `AION_CREATIVITY_INTUITION_V1`
- `intuition_score` + `intuition_class`
- `heuristic_not_truth: true`
- `creative_next_actions[]` (bounded non-execution suggestions)
- `forbidden_actions` guardrails
- local posture + receipt metadata

## Scoring logic (V1)

- +30 if contradictions > 0
- +20 if memory_matches > 0
- +10 per missing control (max +30)
- +20 if governance_decision = BLOCK
- +10 if governance_decision = REVIEW_ONLY
- +20 if evidence_complete = false
- +15 if high-risk signal present (`funds_at_risk|signature|execution|exploit|actuator`)
- +10 if proof_graph_missing_count > 0
- score capped at 100

Classes:

- `0-24`: `LOW_SIGNAL`
- `25-49`: `WATCH`
- `50-74`: `STRONG_SIGNAL`
- `75-100`: `CRITICAL_SIGNAL`

## Safe next-action generation

Generates bounded suggestions such as:

- design verifier
- add rollback plan
- claim downgrade + evidence alignment
- apply memory future-rule check
- capture missing evidence
- domain-specific human-review gates
- introspection proof-gap repair
- always recheck after repair

## Forbidden actions

- `do_not_treat_intuition_as_proof`
- `do_not_execute_without_verifier`
- `do_not_skip_receipts`

## Demo

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\RUN_AION_CREATIVITY_INTUITION_V1_DEMO.ps1
```

Expected marker:

- `AION_CREATIVITY_INTUITION_V1_DEMO_OK`

## Verifier

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\VERIFY_AION_CREATIVITY_INTUITION_V1.ps1
```

Expected marker:

- `AION_CREATIVITY_INTUITION_V1_VERIFY_OK`

## Public-safe posture

- No external network/provider calls
- No governed action execution
- No production mutation
- Runtime receipts only under `receipts/intuition/`
