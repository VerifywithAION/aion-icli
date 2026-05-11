import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "intuition"
ENGINE = "AION_CREATIVITY_INTUITION_V1"

HIGH_RISK_SIGNALS = {"funds_at_risk", "signature", "execution", "exploit", "actuator"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with open(temp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    temp.replace(path)


def _classify(score: int) -> str:
    if score <= 24:
        return "LOW_SIGNAL"
    if score <= 49:
        return "WATCH"
    if score <= 74:
        return "STRONG_SIGNAL"
    return "CRITICAL_SIGNAL"


def _add_action(actions: List[Dict[str, str]], title: str, why: str, boundary: str) -> None:
    actions.append(
        {
            "action_id": f"creative_{len(actions)+1:03d}",
            "title": title,
            "why": why,
            "safe_boundary": boundary,
        }
    )


def _receipt(payload: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    rid = f"aion_intuition_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    name = f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    rel = Path("receipts") / "intuition" / name
    abs_path = ROOT / rel
    body = {
        "receipt_type": "aion_creativity_intuition_receipt_v1",
        "timestamp_utc": stamp,
        "engine": ENGINE,
        "input_payload": payload,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }
    _atomic_write(abs_path, json.dumps(body, indent=2))
    return {
        "receipt_id": rid,
        "receipt_path": str(rel).replace("\\", "/"),
        "receipt_abs_path": str(abs_path),
        "receipt_written": abs_path.exists(),
        "receipt_sha256": hashlib.sha256(abs_path.read_bytes()).hexdigest(),
        "repo_root": str(ROOT),
    }


def analyze_intuition(payload: Dict[str, Any]) -> Dict[str, Any]:
    s = payload.get("signals") if isinstance(payload.get("signals"), dict) else {}
    contradictions = int(s.get("contradictions") or 0)
    memory_matches = int(s.get("memory_matches") or 0)
    missing_controls = [str(x).lower() for x in (s.get("missing_controls") or [])]
    risk_signals = {str(x).lower() for x in (s.get("risk_signals") or [])}
    domain = str(s.get("domain") or "unknown").lower()
    governance_decision = str(s.get("governance_decision") or "UNKNOWN").upper()
    evidence_complete = bool(s.get("evidence_complete"))
    proof_graph_missing_count = int(s.get("proof_graph_missing_count") or 0)

    score = 0
    if contradictions > 0:
        score += 30
    if memory_matches > 0:
        score += 20
    score += min(len(missing_controls) * 10, 30)
    if governance_decision == "BLOCK":
        score += 20
    elif governance_decision == "REVIEW_ONLY":
        score += 10
    if not evidence_complete:
        score += 20
    if risk_signals.intersection(HIGH_RISK_SIGNALS):
        score += 15
    if proof_graph_missing_count > 0:
        score += 10
    score = min(score, 100)

    intuition_class = _classify(score)

    actions: List[Dict[str, str]] = []
    if "verifier" in missing_controls:
        _add_action(actions, "Design verifier for missing control", "Missing verifier blocks admissibility; add deterministic verification marker.", "VERIFY_FIRST")
    if "rollback" in missing_controls:
        _add_action(actions, "Draft rollback plan", "Rollback gap increases consequence risk for mutation paths.", "PLAN_ONLY")
    if contradictions > 0:
        _add_action(actions, "Downgrade claim and align evidence", "Contradictions indicate claim/evidence mismatch; downgrade to review path.", "REVIEW_ONLY")
    if memory_matches > 0:
        _add_action(actions, "Check memory future_rule", "Prior scars matched; enforce stored future_rule before reconsideration.", "VERIFY_FIRST")
    if not evidence_complete:
        _add_action(actions, "Capture missing evidence", "Evidence incomplete; produce report+receipt+verifier linkage.", "VERIFY_FIRST")
    if domain == "wallet" and risk_signals.intersection({"funds_at_risk", "signature"}):
        _add_action(actions, "Enable wallet human-review gate", "Funds/signature risk requires explicit human approval.", "REVIEW_ONLY")
    if domain == "physical_ai" and risk_signals.intersection({"actuator", "execution"}):
        _add_action(actions, "Apply hard block + human review", "Physical AI action with actuator/execution risk requires block until reviewed.", "REVIEW_ONLY")
    if proof_graph_missing_count > 0:
        _add_action(actions, "Run introspection repair plan", "Proof graph gaps indicate missing proof surfaces needing repair.", "PLAN_ONLY")

    _add_action(actions, "Recheck after repair", "Intuition output is heuristic; rerun governance after controls/evidence repair.", "VERIFY_FIRST")

    result: Dict[str, Any] = {
        "engine": ENGINE,
        "intuition_score": score,
        "intuition_class": intuition_class,
        "heuristic_not_truth": True,
        "reason": "Heuristic signal from contradictions, memory, controls, risk, evidence, and proof-gap surfaces.",
        "creative_next_actions": actions,
        "forbidden_actions": [
            "do_not_treat_intuition_as_proof",
            "do_not_execute_without_verifier",
            "do_not_skip_receipts",
        ],
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }

    result.update(_receipt(payload, result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="AION Creativity + Intuition V1")
    parser.add_argument("--input", required=True, help="Path to input JSON payload")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    print(json.dumps(analyze_intuition(payload), indent=2))


if __name__ == "__main__":
    main()
