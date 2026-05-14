from typing import Any, Dict, List

ENGINE = "AION_SYSTEMIC_REASONING_ENGINE_V1"


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _is_huma_state_transition_case(payload: Dict[str, Any], evaluation: Dict[str, Any]) -> bool:
    summary = _text(payload.get("summary")).lower()
    patterns = [str(x).lower() for x in (payload.get("patterns") or [])]
    reason = _text(evaluation.get("reason")).lower()
    cues = {
        "huma",
        "state_transition_bypass",
        "state transition bypass",
        "authorization_bypass",
        "causal authorization",
    }
    hay = " ".join([summary, reason] + patterns)
    return any(c in hay for c in cues)


def reason_systemically(payload: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
    decision = _text(evaluation.get("governance_decision")).upper()
    risk = _text(evaluation.get("risk_level")).upper()

    if _is_huma_state_transition_case(payload, evaluation):
        return {
            "systemic_summary": "A state transition path was treated as legitimacy without verifying causal authorization preconditions.",
            "trust_boundary_collapse": "Approval continuity collapsed because state mutation was accepted as permission.",
            "violated_invariant": "No autonomous progression without validated authorization preconditions.",
            "hidden_governance_assumption": "Assumed mutated state implies authorized state.",
            "generalized_fragility_law": "Any autonomous system that allows state progression without precondition validation can convert appearance of legitimacy into unauthorized consequence.",
            "adjacent_risk_domains": [
                "lending",
                "bridges",
                "dao_governance",
                "liquidation_engines",
                "robot_mode_switching",
                "trading_agent_risk_state_escalation",
                "shopping_purchase_authorization",
            ],
            "autonomy_implication": "Autonomy must validate causal authorization lineage before honoring changed state.",
            "humanoid_implication": "Physical and digital AI must not treat changed state as permission unless the causal path into that state is verified.",
            "non_obvious_insight": "The exploit is not only a bug class; it is a trust-transition failure between state and authorization continuity.",
            "next_governance_question": "Which precondition validator must block this state transition before any value-moving consequence occurs?",
        }

    domains: List[str] = ["api_security", "workflow_automation", "agent_execution_controls"]
    if risk == "HIGH":
        domains.extend(["wallet_authorization", "production_release_gates"])
    return {
        "systemic_summary": "Finding indicates governance boundary stress where execution intent can outrun verification controls.",
        "trust_boundary_collapse": "Potential collapse between claimed safety and evidence-backed authorization path.",
        "violated_invariant": "No trust escalation without verifier and receipt continuity.",
        "hidden_governance_assumption": "Assumes confidence signal is equivalent to admissibility.",
        "generalized_fragility_law": "Systems that permit action progression before control validation amplify local defects into systemic risk.",
        "adjacent_risk_domains": domains,
        "autonomy_implication": "Autonomous agents require explicit control gates before action-class escalation.",
        "humanoid_implication": "Human-facing autonomy must preserve emotional control by proving boundary continuity before consequence.",
        "non_obvious_insight": "Most severe failures are continuity failures, not isolated rule failures.",
        "next_governance_question": "Which missing control, if enforced first, would most reduce unauthorized consequence potential?",
    }
