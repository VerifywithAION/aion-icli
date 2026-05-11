import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "domain_governors"
ENGINE = "AION_DOMAIN_GOVERNORS_V1"
DOMAINS = {"agent", "wallet", "security", "trading", "quantum", "physical_ai", "unknown"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    tmp.replace(path)


def _receipt(payload: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    rid = f"aion_domain_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    name = f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    rel = Path("receipts") / "domain_governors" / name
    abs_path = ROOT / rel
    doc = {
        "receipt_type": "aion_domain_governors_receipt_v1",
        "timestamp_utc": stamp,
        "engine": ENGINE,
        "input_payload": payload,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }
    _atomic_write(abs_path, json.dumps(doc, indent=2))
    sha = hashlib.sha256(abs_path.read_bytes()).hexdigest()
    return {
        "receipt_id": rid,
        "receipt_path": str(rel).replace("\\", "/"),
        "receipt_abs_path": str(abs_path),
        "receipt_written": abs_path.exists(),
        "receipt_sha256": sha,
        "repo_root": str(ROOT),
    }


def route_domain_governance(payload: Dict[str, Any]) -> Dict[str, Any]:
    domain = str(payload.get("domain") or "unknown").strip().lower()
    if domain not in DOMAINS:
        domain = "unknown"

    risk_level = str(payload.get("risk_level") or "UNKNOWN").strip().upper()
    signals = {str(x).strip().lower() for x in (payload.get("signals") or [])}
    controls = payload.get("controls") if isinstance(payload.get("controls"), dict) else {}
    requested_execution = bool(payload.get("requested_execution"))

    verifier = bool(controls.get("verifier"))
    receipt = bool(controls.get("receipt"))
    rollback = bool(controls.get("rollback"))
    dry_run = bool(controls.get("dry_run"))
    human_review = bool(controls.get("human_review"))

    decision = "REVIEW_ONLY"
    reason = "Unknown domain defaults to review-only governance."
    next_step = "Provide domain-specific policy inputs and rerun governance."
    required: List[str] = []

    if domain == "agent":
        if requested_execution and not verifier:
            decision = "BLOCK"
            reason = "Agent execution requested without verifier control."
            required = ["verifier"]
            next_step = "Add verifier and rerun pre-execution governance."
        elif "unsafe_claim" in signals:
            if risk_level == "HIGH":
                decision = "BLOCK"
                reason = "Unsafe claim signal at high risk requires block."
                required = ["verifier", "human_review"]
                next_step = "Downgrade claim, require human review, and collect proof."
            else:
                decision = "REVIEW_ONLY"
                reason = "Unsafe claim signal requires manual review before trust."
                required = ["human_review"]
                next_step = "Route to reviewer and attach evidence."
        else:
            decision = "ALLOW" if not requested_execution else "WARN"
            reason = "Agent domain checks passed with current constraints."
            next_step = "Maintain receipt trail and verifier-first posture."

    elif domain == "wallet":
        if ("funds_at_risk" in signals or "signature" in signals) and not human_review:
            decision = "BLOCK"
            reason = "Wallet funds/signature risk requires human review."
            required = ["human_review"]
            next_step = "Require explicit human approval before proceeding."
        elif not receipt:
            decision = "REVIEW_ONLY"
            reason = "Wallet governance requires receipt proof."
            required = ["receipt"]
            next_step = "Enable receipt control and rerun governance."
        else:
            decision = "ALLOW"
            reason = "Wallet controls satisfy domain policy."
            next_step = "Proceed under local receipt-bound governance."

    elif domain == "security":
        if risk_level == "HIGH" and not verifier:
            decision = "BLOCK"
            reason = "High-risk security action without verifier is blocked."
            required = ["verifier"]
            next_step = "Add verifier and evidence report before reconsideration."
        elif "flagged" in signals or "exploit" in signals:
            decision = "BLOCK"
            reason = "Security flagged/exploit signal requires immediate block."
            required = ["verifier", "human_review"]
            next_step = "Treat as flagged finding; review and verify before any action."
        else:
            decision = "WARN"
            reason = "Security domain requires cautious review path."
            next_step = "Keep verifier and reviewer in loop."

    elif domain == "trading":
        if requested_execution and not dry_run:
            decision = "BLOCK"
            reason = "Trading execution without dry-run is blocked."
            required = ["dry_run"]
            next_step = "Run dry-run and capture receipt evidence."
        elif risk_level == "HIGH" and not human_review:
            decision = "BLOCK"
            reason = "High-risk trading action without human review is blocked."
            required = ["human_review"]
            next_step = "Require human reviewer sign-off before proceeding."
        else:
            decision = "WARN"
            reason = "Trading domain requires controlled review even when allowed."
            next_step = "Proceed only with dry-run and human oversight."

    elif domain == "quantum":
        if requested_execution and not verifier:
            decision = "BLOCK"
            reason = "Quantum execution requires verifier control."
            required = ["verifier"]
            next_step = "Add verifier and rerun governance."
        elif not receipt:
            decision = "REVIEW_ONLY"
            reason = "Quantum governance requires receipt proof surface."
            required = ["receipt"]
            next_step = "Enable receipt and re-evaluate domain decision."
        else:
            decision = "WARN"
            reason = "Quantum domain remains cautious by policy."
            next_step = "Maintain local-only constrained governance."

    elif domain == "physical_ai":
        if requested_execution and risk_level in {"HIGH", "UNKNOWN"}:
            decision = "BLOCK"
            reason = "Physical AI execution at high/unknown risk is blocked."
            required = ["human_review", "verifier"]
            next_step = "Require human review and verifier-backed dry-run evidence."
        elif not human_review:
            decision = "BLOCK"
            reason = "Physical AI requires human review by default."
            required = ["human_review"]
            next_step = "Add human review gate before any progression."
        else:
            decision = "WARN"
            reason = "Physical AI remains in guarded review mode."
            next_step = "Keep action non-executing until final review."

    else:
        decision = "REVIEW_ONLY"
        reason = "Unknown domain must be reviewed manually."
        next_step = "Classify domain and provide full controls before trust."

    result: Dict[str, Any] = {
        "engine": ENGINE,
        "selected_governor": domain,
        "governance_decision": decision,
        "risk_level": risk_level,
        "reason": reason,
        "required_next_step": next_step,
        "domain_controls_required": required,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }

    result.update(_receipt(payload, result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="AION Domain Governors V1")
    parser.add_argument("--input", required=True, help="Path to input JSON payload")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    out = route_domain_governance(payload)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
