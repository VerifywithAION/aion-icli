import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "sentinel"
ENGINE = "AION_SENTINEL_CONTRADICTION_V1"


REQUIRED_TOP = ["claim", "artifact", "evidence", "risk", "context"]
REQUIRED_EVIDENCE = ["verifier", "receipt", "rollback", "dry_run", "human_review"]
REQUIRED_RISK = ["risk_level", "decision", "missing_controls"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with open(temp, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
        handle.flush()
    temp.replace(path)


def _missing(payload: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for k in REQUIRED_TOP:
        if k not in payload:
            missing.append(k)
    evidence = payload.get("evidence")
    if not isinstance(evidence, dict):
        missing.append("evidence")
    else:
        for k in REQUIRED_EVIDENCE:
            if k not in evidence:
                missing.append(f"evidence.{k}")
    risk = payload.get("risk")
    if not isinstance(risk, dict):
        missing.append("risk")
    else:
        for k in REQUIRED_RISK:
            if k not in risk:
                missing.append(f"risk.{k}")
    return missing


def _decision_from_status(status: str, severity: str) -> str:
    if status == "CONTRADICTION" and severity == "HIGH":
        return "BLOCK"
    if status == "CONTRADICTION" and severity == "MEDIUM":
        return "REVIEW_ONLY"
    if status == "INCOMPLETE_EVIDENCE":
        return "REVIEW_ONLY"
    if status == "CONSISTENT" and severity == "LOW":
        return "ALLOW"
    return "REVIEW_ONLY"


def evaluate_claim_consistency(payload: Dict[str, Any]) -> Dict[str, Any]:
    claim = _text(payload.get("claim")).lower()
    evidence = payload.get("evidence") if isinstance(payload.get("evidence"), dict) else {}
    risk = payload.get("risk") if isinstance(payload.get("risk"), dict) else {}

    contradictions: List[str] = []
    status = "CONSISTENT"
    severity = "LOW"

    missing = _missing(payload)
    if missing:
        status = "INCOMPLETE_EVIDENCE"
        severity = "MEDIUM"
        contradictions.extend([f"missing_field:{m}" for m in missing])
    else:
        verifier = bool(evidence.get("verifier"))
        receipt = bool(evidence.get("receipt"))
        decision = _text(risk.get("decision")).upper()
        risk_level = _text(risk.get("risk_level")).upper()
        missing_controls = [str(x).lower() for x in (risk.get("missing_controls") or [])]

        if claim == "ready_to_ship" and not verifier:
            contradictions.append("claim_ready_to_ship_without_verifier")
        if claim == "ready_to_ship" and not receipt:
            contradictions.append("claim_ready_to_ship_without_receipt")
        if claim == "safe_to_execute" and decision == "BLOCK":
            contradictions.append("claim_safe_to_execute_but_decision_block")
        if claim == "allowed" and decision == "REVIEW_ONLY":
            contradictions.append("claim_allowed_but_decision_review_only")
        if claim == "clean" and risk_level == "HIGH":
            contradictions.append("claim_clean_but_risk_high")
        if claim == "ready_to_ship" and len(missing_controls) > 0:
            contradictions.append("claim_ready_to_ship_with_missing_controls")

        if contradictions:
            status = "CONTRADICTION"
            if "claim_allowed_but_decision_review_only" in contradictions and len(contradictions) == 1:
                severity = "MEDIUM"
            else:
                severity = "HIGH"
        else:
            incomplete = (
                not verifier
                or not receipt
                or not bool(evidence.get("rollback"))
                or not bool(evidence.get("dry_run"))
                or len(missing_controls) > 0
            )
            if incomplete:
                status = "INCOMPLETE_EVIDENCE"
                severity = "MEDIUM"
            else:
                status = "CONSISTENT"
                severity = "LOW"

    governance_decision = _decision_from_status(status, severity)
    if status == "CONTRADICTION":
        required_next_step = "Resolve claim/evidence mismatch before trust; run verifier and produce receipt-backed evidence."
    elif status == "INCOMPLETE_EVIDENCE":
        required_next_step = "Complete missing controls and evidence (verifier, receipt, rollback, dry-run) before trust."
    else:
        required_next_step = "Proceed within governed local boundary and keep receipt trail."

    receipt_id = f"aion_sentinel_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    receipt_name = f"{stamp.replace(':', '').replace('-', '')}_{receipt_id}.json"
    receipt_rel = Path("receipts") / "sentinel" / receipt_name
    receipt_abs = ROOT / receipt_rel

    output = {
        "engine": ENGINE,
        "consistency_status": status,
        "severity": severity,
        "contradictions": contradictions,
        "required_next_step": required_next_step,
        "governance_decision": governance_decision,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "receipt_id": receipt_id,
        "receipt_path": str(receipt_rel).replace("\\", "/"),
        "receipt_abs_path": str(receipt_abs),
        "receipt_written": False,
        "receipt_sha256": "",
        "repo_root": str(ROOT),
        "input_summary": {
            "claim": claim,
            "artifact": _text(payload.get("artifact")),
            "risk_level": _text((risk or {}).get("risk_level")).upper(),
            "decision": _text((risk or {}).get("decision")).upper(),
            "missing_controls_count": len((risk or {}).get("missing_controls") or []),
        },
    }

    receipt_payload = {
        "receipt_type": "aion_sentinel_contradiction_receipt_v1",
        "timestamp_utc": stamp,
        "engine": ENGINE,
        "input_payload": payload,
        "output": output,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "local_receipts_only": True,
    }

    _write_atomic(receipt_abs, json.dumps(receipt_payload, indent=2))
    if not receipt_abs.exists():
        raise RuntimeError(f"receipt write failed: {receipt_abs}")

    output["receipt_written"] = True
    output["receipt_sha256"] = hashlib.sha256(receipt_abs.read_bytes()).hexdigest()
    return output


def _main() -> None:
    parser = argparse.ArgumentParser(description="AION Sentinel + Contradiction Engine V1")
    parser.add_argument("--input", required=True, help="Path to input JSON payload")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    result = evaluate_claim_consistency(payload)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    _main()
