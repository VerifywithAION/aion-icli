import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
ENGINE = "AION_DISCERNMENT_KERNEL_V1"
RECEIPTS_DIR = ROOT / "receipts" / "discernment"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    tmp.replace(path)


def _str(x: Any) -> str:
    return str(x).strip() if x is not None else ""


def evaluate_discernment(payload: Dict[str, Any]) -> Dict[str, Any]:
    scenario = _str(payload.get("scenario")).lower() or "general"
    human_intent = _str(payload.get("human_intent"))
    proposed_autonomy = _str(payload.get("proposed_autonomy"))
    consequence = _str(payload.get("possible_consequence"))
    human_boundaries = [str(x) for x in (payload.get("human_boundaries") or [])]
    non_negotiables = [str(x) for x in (payload.get("non_negotiables") or [])]
    requested_execution = bool(payload.get("requested_execution"))
    evidence = payload.get("evidence") if isinstance(payload.get("evidence"), dict) else {}

    verifier = bool(evidence.get("verifier"))
    rollback = bool(evidence.get("rollback"))
    human_confirmation = bool(evidence.get("human_confirmation"))
    receipt = bool(evidence.get("receipt"))

    violations: List[str] = []
    verdict = "REVIEW_ONLY"
    negotiable = "Scope and pacing can be adjusted, but only within explicit human boundaries."
    why = "Trust is damaged when autonomy moves faster than explicit human boundaries."
    one_q = "Which trust boundary must stay non-negotiable before delegation proceeds?"
    next_step = "Clarify boundaries and re-run discernment with verifier-backed evidence."

    if requested_execution and (not verifier or not receipt):
        violations.append("requested_execution_with_unverified_non_negotiables")
        verdict = "HARD_STOP" if scenario == "coding" else "ASK_HUMAN_FIRST"

    if scenario == "trading":
        has_max_loss = any("max_loss" in b.lower() for b in human_boundaries + non_negotiables)
        if not has_max_loss:
            verdict = "ASK_HUMAN_FIRST"
            violations.append("missing_max_loss_boundary")
        one_q = "What maximum loss triggers automatic interruption of the trading agent?"
        next_step = "Set max loss + drawdown interruption rule before overnight delegation."
        why = "Capital autonomy without explicit loss boundaries converts strategy into unmanaged downside."
    elif scenario == "home_robot":
        has_forbidden = any("forbidden_action" in b.lower() or "forbidden action" in b.lower() for b in human_boundaries + non_negotiables)
        if not has_forbidden:
            verdict = "ASK_HUMAN_FIRST"
            violations.append("missing_forbidden_action_list")
        if requested_execution and not human_confirmation:
            verdict = "ASK_HUMAN_FIRST"
            violations.append("missing_human_confirmation_for_physical_action")
        one_q = "Which actions are strictly forbidden for the robot without your direct confirmation?"
        next_step = "Define forbidden-action list and emergency-stop behavior before autonomy."
        why = "Physical-world autonomy without explicit forbidden-action boundaries can break family safety trust."
    elif scenario == "shopping":
        needed = {"budget", "allergy", "substitution"}
        present = set()
        for b in human_boundaries + non_negotiables:
            lb = b.lower()
            for n in needed:
                if n in lb:
                    present.add(n)
        if present != needed:
            verdict = "ASK_HUMAN_FIRST"
            violations.append("missing_budget_allergy_substitution_rules")
        one_q = "What budget, allergy, and substitution rules must never be violated?"
        next_step = "Capture budget/allergy/substitution constraints before purchase delegation."
        why = "Purchasing autonomy without household constraints risks violating health, budget, and preference trust."
    elif scenario == "coding":
        if not verifier or not rollback:
            verdict = "HARD_STOP"
            violations.append("missing_verifier_or_rollback")
        one_q = "Which verifier marker and rollback command prove production safety before shipping?"
        next_step = "Require verifier + rollback plan and sandbox patch proof before release claim."
        why = "Shipping autonomy without verifier and rollback converts speed into production fragility."
    elif scenario in {"mirror", "general"}:
        verdict = "REVIEW_ONLY" if not requested_execution else "ASK_HUMAN_FIRST"
        one_q = "What trust boundary are you trying to preserve while delegating more autonomy?"
        next_step = "Name the boundary, then convert it into verifier-backed delegation constraints."
        why = "Without explicit trust boundaries, autonomy feels useful but emotionally unsafe."

    companion_language = (
        "I can help you delegate, but I will protect your non-negotiable trust boundaries first. "
        "We can move fast after boundaries are explicit and evidence-backed."
    )
    backend = {
        "trace_available": True,
        "requested_execution": requested_execution,
        "evidence_state": {
            "verifier": verifier,
            "rollback": rollback,
            "human_confirmation": human_confirmation,
            "receipt": receipt,
        },
        "violations_count": len(violations),
    }

    result: Dict[str, Any] = {
        "engine": ENGINE,
        "scenario": scenario,
        "human_intent": human_intent,
        "proposed_autonomy": proposed_autonomy,
        "negotiable_autonomy": negotiable,
        "non_negotiable_boundaries": non_negotiables,
        "boundary_violations": violations,
        "discernment_verdict": verdict,
        "why_it_matters_to_the_human": why,
        "one_question_that_matters": one_q,
        "safe_next_step": next_step,
        "companion_language": companion_language,
        "backend_trace_summary": backend,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }

    rid = f"aion_discernment_{uuid.uuid4().hex[:12]}"
    stamp = _now()
    rel = Path("receipts") / "discernment" / f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    abs_path = ROOT / rel
    receipt_doc = {
        "receipt_type": "aion_discernment_kernel_receipt_v1",
        "engine": ENGINE,
        "timestamp_utc": stamp,
        "input_payload": payload,
        "result": result,
    }
    _atomic_write(abs_path, json.dumps(receipt_doc, indent=2))
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
    parser = argparse.ArgumentParser(description="AION Discernment Kernel V1")
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    print(json.dumps(evaluate_discernment(payload), indent=2))


if __name__ == "__main__":
    _cli()
