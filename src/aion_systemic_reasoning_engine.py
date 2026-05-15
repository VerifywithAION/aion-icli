from typing import Any, Dict, List

ENGINE = "AION_SYSTEMIC_REASONING_ENGINE_V1"


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _family(payload: Dict[str, Any], evaluation: Dict[str, Any]) -> str:
    summary = _text(payload.get("summary")).lower()
    patterns = [str(x).lower() for x in (payload.get("patterns") or [])]
    reason = _text(evaluation.get("reason")).lower()
    hay = " ".join([summary, reason] + patterns)

    if any(x in hay for x in ["state_transition_bypass", "state transition bypass", "state_machine", "state machine"]):
        return "state_machine"
    if any(x in hay for x in ["single eoa", "single_eoa", "admin key", "admin_key", "no timelock", "timelock missing"]):
        return "admin_key"
    if any(x in hay for x in ["uups", "upgradeability", "upgradeable", "implementation slot"]):
        return "upgradeability"
    if any(x in hay for x in ["oracle", "price feed", "stale price", "twap"]):
        return "oracle"
    if any(x in hay for x in ["bridge", "cross-chain", "cross chain", "replay"]):
        return "bridge"
    if any(x in hay for x in ["authorization_bypass", "role bypass", "role_bypass", "access control"]):
        return "authorization"
    if any(x in hay for x in ["strategy address", "strategy_address", "whitelist bypass", "whitelist_bypass"]):
        return "delegation"
    if any(x in hay for x in ["autonomy", "agent", "delegation boundary", "robot mode switching"]):
        return "ai_autonomy"
    return "generic"


def reason_systemically(payload: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
    family = _family(payload, evaluation)

    if family == "state_machine":
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
    if family == "admin_key":
        return {
            "systemic_summary": "Single-admin authority concentrated upgrade and operational control into one compromise path.",
            "trust_boundary_collapse": "Multi-party governance assurance collapsed into single-key liveness and integrity assumptions.",
            "violated_invariant": "Critical state transitions require distributed authorization and delay guarantees.",
            "hidden_governance_assumption": "Assumed key holder integrity is equivalent to protocol governance integrity.",
            "generalized_fragility_law": "Systems with single-point admin authority convert key compromise into full-system consequence.",
            "adjacent_risk_domains": ["dao_governance", "treasury_management", "custody_controls", "ai_agent_admin_panels"],
            "autonomy_implication": "Autonomous operations must never inherit unrestricted admin privilege without distributed checks.",
            "humanoid_implication": "Human-facing autonomous assistants must treat single-actor override paths as unsafe by default.",
            "non_obvious_insight": "Admin-key exploits are trust-topology failures before they are software failures.",
            "next_governance_question": "Which control split and timelock path removes single-key consequence dominance?",
        }
    if family == "upgradeability":
        return {
            "systemic_summary": "Upgrade path integrity allowed code-trust to shift without sufficiently constrained governance continuity.",
            "trust_boundary_collapse": "Protocol trust anchored to mutable logic without strong pre-upgrade legitimacy gates.",
            "violated_invariant": "No upgrade should alter consequence surface without delayed, reviewable, multi-party authorization.",
            "hidden_governance_assumption": "Assumed upgrade authority behavior is permanently aligned with user trust.",
            "generalized_fragility_law": "Mutable systems without hardened upgrade governance can silently convert maintenance into takeover.",
            "adjacent_risk_domains": ["wallet_firmware_updates", "robot_control_firmware", "agent_policy_hot_swap", "infra_rollout_controls"],
            "autonomy_implication": "Autonomy layers need immutable trust anchors around upgrade initiation and activation boundaries.",
            "humanoid_implication": "Companion AI must not normalize silent control-plane upgrades as routine trust-preserving events.",
            "non_obvious_insight": "Upgradeability risk is governance-latency risk: harm happens between authority and visibility.",
            "next_governance_question": "What mandatory pre-activation checks prove an upgrade preserves prior trust invariants?",
        }
    if family == "oracle":
        return {
            "systemic_summary": "Decisioning consumed manipulable or stale external truth, allowing state to follow false reality.",
            "trust_boundary_collapse": "Reality verification boundary collapsed between data integrity and action legitimacy.",
            "violated_invariant": "No critical action should execute from a single unvalidated external truth source.",
            "hidden_governance_assumption": "Assumed feed correctness at action time without adversarial context checks.",
            "generalized_fragility_law": "Any system that binds consequence to unverified input reality can be coerced by signal distortion.",
            "adjacent_risk_domains": ["liquidation_engines", "autonomous_trading", "robot_sensor_fusion", "pricing_automation"],
            "autonomy_implication": "Autonomous agents need independent consensus and sanity bounds before committing reality-driven actions.",
            "humanoid_implication": "Human-facing AI must disclose uncertainty when action depends on contested or low-integrity external signals.",
            "non_obvious_insight": "Oracle failures are epistemic-governance failures: wrong facts become legitimate actions.",
            "next_governance_question": "Which secondary validation path must confirm this oracle state before any irreversible action?",
        }
    if family == "bridge":
        return {
            "systemic_summary": "Cross-domain message legitimacy was accepted without robust replay and origin continuity guarantees.",
            "trust_boundary_collapse": "Chain boundary assurance collapsed when message presence was treated as message authority.",
            "violated_invariant": "No cross-domain consequence without replay resistance and origin-finality verification.",
            "hidden_governance_assumption": "Assumed bridged state import equals trusted state lineage.",
            "generalized_fragility_law": "Cross-domain systems that validate delivery but not provenance convert transport into exploit surface.",
            "adjacent_risk_domains": ["l2_settlement", "cross_system_identities", "agent_to_agent_protocols", "iot_handoff_control"],
            "autonomy_implication": "Autonomous cross-system actions must validate source chain finality and message uniqueness before execution.",
            "humanoid_implication": "Companion autonomy must treat inter-system state handoff as high-risk unless provenance is explicit and verifiable.",
            "non_obvious_insight": "Bridge exploits weaponize assumption gaps between origin truth and destination action.",
            "next_governance_question": "What provenance and replay-proof checks are mandatory before honoring this cross-domain transition?",
        }
    if family == "authorization":
        return {
            "systemic_summary": "Role or permission boundaries were bypassed, decoupling action authority from declared governance policy.",
            "trust_boundary_collapse": "Declared authorization model diverged from executable authorization path.",
            "violated_invariant": "No privileged action without role-bound, context-bound authorization validation.",
            "hidden_governance_assumption": "Assumed role declaration guarantees role enforcement.",
            "generalized_fragility_law": "Systems that separate policy declaration from enforcement allow policy theater with exploitable execution reality.",
            "adjacent_risk_domains": ["wallet_permissions", "enterprise_access_control", "robot_safety_modes", "agent_tool_permissions"],
            "autonomy_implication": "Autonomous agents must treat authorization failures as boundary collapse events, not recoverable warnings.",
            "humanoid_implication": "Human trust is broken when AI can act outside declared permissions despite visible policy constraints.",
            "non_obvious_insight": "Authorization exploits are credibility exploits against the governance narrative itself.",
            "next_governance_question": "Which enforcement checkpoint proves this action cannot bypass role constraints at runtime?",
        }
    if family == "delegation":
        return {
            "systemic_summary": "Delegated strategy or whitelist boundary was bypassed, allowing autonomy to exceed delegated scope.",
            "trust_boundary_collapse": "Delegation intent collapsed because target constraints were treated as optional routing hints.",
            "violated_invariant": "Delegated autonomy must remain constrained to explicitly authorized targets and strategies.",
            "hidden_governance_assumption": "Assumed delegation metadata enforces itself under adversarial paths.",
            "generalized_fragility_law": "Delegation systems without hard target constraints convert convenience routing into consequence escalation.",
            "adjacent_risk_domains": ["portfolio_rebalancing", "api_allowlists", "shopping_purchase_controls", "workflow_delegation"],
            "autonomy_implication": "Agent delegation must include immutable scope fences and deny-by-default target validation.",
            "humanoid_implication": "Companion AI must preserve the human’s delegated scope exactly; interpretation drift is a trust violation.",
            "non_obvious_insight": "Delegation failures are often scope-integrity failures, not intent-understanding failures.",
            "next_governance_question": "Which immutable scope check prevents autonomy from selecting non-authorized strategy targets?",
        }
    if family == "ai_autonomy":
        return {
            "systemic_summary": "Autonomous action planning exceeded explicit human delegation boundaries under weak pre-execution gating.",
            "trust_boundary_collapse": "Human intent continuity collapsed between stated preference and executed autonomy behavior.",
            "violated_invariant": "No autonomous escalation without explicit, current, verifiable human boundary confirmation.",
            "hidden_governance_assumption": "Assumed prior consent persists across changed risk context.",
            "generalized_fragility_law": "Autonomy systems that treat historical intent as ongoing authorization convert assistance into overreach.",
            "adjacent_risk_domains": ["robotics", "financial_agents", "devops_agents", "health_assistant_workflows"],
            "autonomy_implication": "Autonomous systems need live boundary reconciliation before risk-class changes.",
            "humanoid_implication": "Human-centered AI must ask before crossing risk thresholds, even when technically capable of proceeding.",
            "non_obvious_insight": "The critical exploit surface in autonomy is often consent continuity, not model capability.",
            "next_governance_question": "What boundary reconfirmation must occur before this autonomy path is allowed to escalate?",
        }

    domains: List[str] = ["api_security", "workflow_automation", "agent_execution_controls"]
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
