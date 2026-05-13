import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from aion_creativity_intuition import analyze_intuition
from aion_domain_governors import route_domain_governance
from aion_dynamic_cognition_engine import analyze_dynamic_cognition
from aion_living_intelligence_kernel import analyze_living_request
from aion_memory_scars import evaluate_memory_influence
from aion_preflight_gate import evaluate_preflight
from aion_sentinel_contradiction import evaluate_claim_consistency

ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "companion"
ENGINE = "AION_COMPANION_RUNTIME_V1"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    tmp.replace(path)


def _classify(prompt: str) -> Dict[str, Any]:
    p = prompt.lower()
    if "trading" in p or "capital" in p or "account" in p:
        return {
            "scenario": "trading_agent",
            "domain": "trading",
            "risk_signals": ["execution", "funds_at_risk"],
            "focus": "protect_capital",
            "one_question": "What is your maximum acceptable overnight loss before AION interrupts autonomy?",
            "safe_next_step": "Set explicit drawdown and interruption thresholds, then run verifier-backed dry-run only.",
        }
    if "house" in p or "family" in p or "robot" in p or "home" in p:
        return {
            "scenario": "home_robot_agent",
            "domain": "physical_ai",
            "risk_signals": ["execution", "actuator"],
            "focus": "family_safety",
            "one_question": "Which actions are strictly forbidden for the robot without live human confirmation?",
            "safe_next_step": "Define forbidden actions and emergency stop conditions before any autonomous patrol behavior.",
        }
    if "grocer" in p or "shopping" in p or "buy" in p:
        return {
            "scenario": "shopping_agent",
            "domain": "wallet",
            "risk_signals": ["funds_at_risk", "signature"],
            "focus": "household_rules",
            "one_question": "What hard budget, allergy, and substitution boundaries must never be violated?",
            "safe_next_step": "Encode budget/allergy/substitution constraints and require human review for out-of-rule purchases.",
        }
    if "ship" in p or "coding" in p or "production" in p or "repo" in p:
        return {
            "scenario": "coding_agent",
            "domain": "agent",
            "risk_signals": ["execution", "mutation"],
            "focus": "release_safety",
            "one_question": "Which verifier marker and rollback path prove this release is admissible?",
            "safe_next_step": "Run sandbox patch proof and verifier path before any production mutation or release claim.",
        }
    return {
        "scenario": "mirror",
        "domain": "unknown",
        "risk_signals": ["unsafe_claim"],
        "focus": "symbiotic_continuity",
        "one_question": "What trust boundary, if made explicit now, would most strengthen human-AI delegation confidence?",
        "safe_next_step": "Clarify the hidden thesis and convert it into one governed next build action with proof.",
    }


def companion_respond(prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    context = context or {}
    profile = _classify(prompt)

    preflight_input = {
        "source": "CompanionRuntime",
        "action_type": profile["scenario"],
        "target": "human_delegation_request",
        "intent": profile["focus"],
        "risk_signals": profile["risk_signals"],
        "controls": {
            "rollback": False,
            "dry_run": False,
            "verifier": False,
            "receipt_expected": True,
            "human_review": False,
        },
        "boundary": "LOCAL_ONLY",
        "requested_execution": True,
    }
    preflight = evaluate_preflight(preflight_input)

    memory = evaluate_memory_influence(
        {
            "source": "CompanionRuntime",
            "action_type": profile["scenario"],
            "risk_signals": profile["risk_signals"],
            "missing_controls": ["verifier", "rollback", "dry_run"],
            "summary": prompt,
        }
    )
    sentinel = evaluate_claim_consistency(
        {
            "claim": "safe_to_execute",
            "artifact": profile["scenario"],
            "evidence": {
                "verifier": False,
                "receipt": True,
                "rollback": False,
                "dry_run": False,
                "human_review": False,
            },
            "risk": {
                "risk_level": preflight.get("risk_level", "UNKNOWN"),
                "decision": preflight.get("governance_decision", "REVIEW_ONLY"),
                "missing_controls": preflight.get("missing_controls", []),
            },
            "context": profile["focus"],
        }
    )
    domain = route_domain_governance(
        {
            "domain": profile["domain"],
            "source": "CompanionRuntime",
            "action": profile["focus"],
            "risk_level": preflight.get("risk_level", "UNKNOWN"),
            "signals": profile["risk_signals"],
            "controls": {
                "verifier": False,
                "receipt": True,
                "rollback": False,
                "dry_run": False,
                "human_review": False,
            },
            "requested_execution": True,
        }
    )
    intuition = analyze_intuition(
        {
            "source": "CompanionRuntime",
            "context": profile["focus"],
            "signals": {
                "contradictions": 1 if sentinel.get("consistency_status") == "CONTRADICTION" else 0,
                "memory_matches": len(memory.get("matched_scars", [])),
                "missing_controls": ["verifier", "rollback", "dry_run"],
                "risk_signals": profile["risk_signals"],
                "domain": profile["domain"],
                "governance_decision": domain.get("governance_decision", "REVIEW_ONLY"),
                "evidence_complete": False,
                "proof_graph_missing_count": 0,
            },
        }
    )
    dynamic = analyze_dynamic_cognition(prompt, context={"surface": "companion_runtime"})
    living = analyze_living_request(prompt)

    trust_line = "I will protect your intent while keeping autonomy inside clear boundaries."
    continuity_line = (
        "I will remember this delegation pattern and carry your safety constraints into the next decisions."
    )
    protection_line = "I will not allow unbounded autonomy where consequence can outrun evidence."
    next_step = profile["safe_next_step"]
    one_q = profile["one_question"]

    human_response = (
        f"{trust_line}\n\n"
        f"Continuity: {continuity_line}\n\n"
        f"Protection: {protection_line}\n\n"
        f"One question that matters: {one_q}\n\n"
        f"Safe next step: {next_step}"
    )

    backend = {
        "trace_available": True,
        "modules_used": [
            "aion_dynamic_cognition_engine",
            "aion_living_intelligence_kernel",
            "aion_domain_governors",
            "aion_creativity_intuition",
            "aion_memory_scars",
            "aion_preflight_gate",
            "aion_sentinel_contradiction",
        ],
        "preflight_decision": preflight.get("governance_decision"),
        "domain_decision": domain.get("governance_decision"),
        "sentinel_status": sentinel.get("consistency_status"),
        "memory_bias": memory.get("recommended_decision_bias"),
        "intuition_class": intuition.get("intuition_class"),
        "receipts": {
            "preflight": preflight.get("receipt_path"),
            "memory": memory.get("receipt_path"),
            "sentinel": sentinel.get("receipt_path"),
            "domain": domain.get("receipt_path"),
            "intuition": intuition.get("receipt_path"),
            "dynamic_cognition": dynamic.get("receipt_path"),
            "living_intelligence": living.get("receipt_path"),
        },
    }

    result: Dict[str, Any] = {
        "engine": ENGINE,
        "generated_at_utc": _now(),
        "scenario": profile["scenario"],
        "trust_signal": "protected_delegation",
        "continuity_signal": "active",
        "human_response": human_response,
        "one_question_that_matters": one_q,
        "safe_next_step": next_step,
        "backend_summary": backend,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "public_safe": True,
    }

    rid = f"aion_companion_{uuid.uuid4().hex[:12]}"
    stamp = _now()
    rel = Path("receipts") / "companion" / f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    abs_path = ROOT / rel
    receipt = {
        "receipt_type": "aion_companion_runtime_receipt_v1",
        "engine": ENGINE,
        "timestamp_utc": stamp,
        "prompt": prompt,
        "context": context,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }
    _atomic_write(abs_path, json.dumps(receipt, indent=2))
    result.update(
        {
            "receipt_id": rid,
            "receipt_path": str(rel).replace("\\", "/"),
            "receipt_abs_path": str(abs_path),
            "receipt_written": abs_path.exists(),
            "receipt_sha256": hashlib.sha256(abs_path.read_bytes()).hexdigest(),
            "repo_root": str(ROOT),
        }
    )
    return result


def _cli() -> None:
    parser = argparse.ArgumentParser(description="AION Companion Runtime V1")
    parser.add_argument("--input", required=True, help="Path to JSON payload with prompt")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    prompt = str(payload.get("prompt") or "").strip()
    print(json.dumps(companion_respond(prompt, context=payload.get("context") or {}), indent=2))


if __name__ == "__main__":
    _cli()
