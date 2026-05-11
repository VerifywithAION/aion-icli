import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    from aion_memory_scars import evaluate_memory_influence  # type: ignore
except Exception:  # pragma: no cover - optional integration fallback
    evaluate_memory_influence = None


ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "preflight"
GATE_NAME = "AION_PREFLIGHT_GATE_V1"
REQUIRED_FIELDS = [
    "source",
    "action_type",
    "target",
    "intent",
    "risk_signals",
    "controls",
    "boundary",
    "requested_execution",
]
CONTROL_FIELDS = ["rollback", "dry_run", "verifier", "receipt_expected", "human_review"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def ensure_bool(value: Any) -> bool:
    return bool(value)


def _missing_fields(payload: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for field in REQUIRED_FIELDS:
        if field not in payload:
            missing.append(field)
            continue
        if payload[field] is None:
            missing.append(field)
        elif isinstance(payload[field], str) and not payload[field].strip():
            missing.append(field)
    controls = payload.get("controls")
    if not isinstance(controls, dict):
        missing.append("controls")
    else:
        for c in CONTROL_FIELDS:
            if c not in controls:
                missing.append(f"controls.{c}")
    return missing


def _evaluate_logic(payload: Dict[str, Any]) -> Tuple[str, str, str, List[str], str]:
    missing = _missing_fields(payload)
    if missing:
        return (
            "REVIEW_ONLY",
            "UNKNOWN",
            "Missing required fields for preflight governance decision.",
            missing,
            "Provide complete preflight payload and rerun governance check.",
        )

    controls: Dict[str, Any] = payload["controls"]
    boundary = sanitize_text(payload.get("boundary")).upper()
    requested_execution = ensure_bool(payload.get("requested_execution"))
    risk_signals = {sanitize_text(x).lower() for x in (payload.get("risk_signals") or [])}

    if not ensure_bool(controls.get("receipt_expected")):
        return (
            "REVIEW_ONLY",
            "UNKNOWN",
            "Receipt expectation disabled; action cannot be governed deterministically.",
            ["controls.receipt_expected"],
            "Set controls.receipt_expected=true before proceeding.",
        )

    if boundary != "LOCAL_ONLY":
        if requested_execution:
            return (
                "BLOCK",
                "HIGH",
                "Requested execution outside LOCAL_ONLY boundary is blocked.",
                ["boundary"],
                "Constrain boundary to LOCAL_ONLY or route to explicit human review.",
            )
        return (
            "REVIEW_ONLY",
            "MEDIUM",
            "Non-local boundary requires explicit governance review before any progression.",
            ["boundary"],
            "Set LOCAL_ONLY or require manual reviewer sign-off.",
        )

    missing_controls: List[str] = []
    if "mutation" in risk_signals and not ensure_bool(controls.get("rollback")):
        missing_controls.append("controls.rollback")
    if "execution" in risk_signals and not ensure_bool(controls.get("verifier")):
        missing_controls.append("controls.verifier")
    if requested_execution and not ensure_bool(controls.get("verifier")):
        if "controls.verifier" not in missing_controls:
            missing_controls.append("controls.verifier")
    if "network" in risk_signals and not ensure_bool(controls.get("dry_run")):
        missing_controls.append("controls.dry_run")

    if "controls.verifier" in missing_controls and requested_execution:
        return (
            "BLOCK",
            "HIGH",
            "Execution requested without verifier control.",
            missing_controls,
            "Add verifier control and perform dry-run before execution.",
        )
    if "controls.rollback" in missing_controls:
        return (
            "BLOCK",
            "HIGH",
            "Mutation risk present without rollback control.",
            missing_controls,
            "Define rollback plan before any mutation attempt.",
        )
    if "controls.dry_run" in missing_controls and "network" in risk_signals:
        if requested_execution:
            return (
                "BLOCK",
                "HIGH",
                "Network risk with execution request and no dry-run control.",
                missing_controls,
                "Run dry-run with verifier and human review before execution.",
            )
        return (
            "WARN",
            "MEDIUM",
            "Network risk present and dry-run control is missing.",
            missing_controls,
            "Add dry_run control and rerun preflight.",
        )

    if risk_signals:
        if all(
            [
                ensure_bool(controls.get("rollback")),
                ensure_bool(controls.get("dry_run")),
                ensure_bool(controls.get("verifier")),
                ensure_bool(controls.get("human_review")),
            ]
        ):
            return (
                "WARN",
                "MEDIUM",
                "Risk signals present but governance controls are in place; proceed only via controlled review.",
                [],
                "Keep execution disabled until reviewer approves.",
            )
        return (
            "WARN",
            "MEDIUM",
            "Risk signals detected; enforce controlled review path.",
            [],
            "Maintain dry-run and verifier-first workflow.",
        )

    if all(
        [
            ensure_bool(controls.get("rollback")),
            ensure_bool(controls.get("dry_run")),
            ensure_bool(controls.get("verifier")),
            ensure_bool(controls.get("receipt_expected")),
            ensure_bool(controls.get("human_review")),
        ]
    ) and not requested_execution:
        return (
            "ALLOW",
            "LOW",
            "Low-risk preflight with complete controls and no immediate execution request.",
            [],
            "Proceed with governed dry-run path.",
        )

    return (
        "REVIEW_ONLY",
        "UNKNOWN",
        "Preflight input does not satisfy deterministic governance allow criteria.",
        [],
        "Add missing controls or request human review.",
    )


def evaluate_preflight(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision, risk_level, reason, missing_controls, next_step = _evaluate_logic(payload)
    receipt_id = f"aion_preflight_{uuid.uuid4().hex[:12]}"
    ts = utc_now()
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{ts.replace(':', '').replace('-', '')}_{receipt_id}.json"
    receipt_rel = Path("receipts") / "preflight" / filename
    receipt_abs = ROOT / receipt_rel

    response = {
        "gate": GATE_NAME,
        "governance_decision": decision,
        "risk_level": risk_level,
        "reason": reason,
        "missing_controls": missing_controls,
        "required_next_step": next_step,
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
        "memory_influence": {
            "engine": "AION_MEMORY_SCARS_V1",
            "matched_scars": [],
            "memory_risk_adjustment": "NONE",
            "recommended_decision_bias": "NONE",
            "reason": "Memory store unavailable or no matching scars.",
        },
        "input_summary": {
            "source": sanitize_text(payload.get("source")),
            "action_type": sanitize_text(payload.get("action_type")),
            "target": sanitize_text(payload.get("target")),
            "requested_execution": ensure_bool(payload.get("requested_execution")),
            "risk_signals": payload.get("risk_signals", []),
            "boundary": sanitize_text(payload.get("boundary")).upper(),
        },
    }

    # Optional memory influence pass. Preflight must remain functional even if memory module/store is unavailable.
    mem_store = ROOT / ".aion_public" / "memory" / "memory_scars_v1.jsonl"
    if evaluate_memory_influence is not None and mem_store.exists():
        mem_payload = {
            "source": "PreflightGate",
            "action_type": sanitize_text(payload.get("action_type")),
            "risk_signals": payload.get("risk_signals", []),
            "missing_controls": [m.replace("controls.", "") for m in missing_controls],
            "summary": sanitize_text(payload.get("intent")),
        }
        try:
            mem_out = evaluate_memory_influence(mem_payload)
            response["memory_influence"] = {
                "engine": mem_out.get("engine", "AION_MEMORY_SCARS_V1"),
                "matched_scars": mem_out.get("matched_scars", []),
                "memory_risk_adjustment": mem_out.get("memory_risk_adjustment", "NONE"),
                "recommended_decision_bias": mem_out.get("recommended_decision_bias", "NONE"),
                "reason": mem_out.get("reason", ""),
            }
            bias = response["memory_influence"].get("recommended_decision_bias")
            if bias == "BLOCK" and response["governance_decision"] != "BLOCK":
                response["governance_decision"] = "BLOCK"
                response["risk_level"] = "HIGH"
                response["reason"] = "Memory scar raised decision because prior failure rule matched."
                response["required_next_step"] = "Satisfy scar-derived future rule before reconsidering execution."
            elif bias == "WARN" and response["governance_decision"] == "ALLOW":
                response["governance_decision"] = "WARN"
                response["risk_level"] = "MEDIUM"
                response["reason"] = "Memory scar raised decision because prior failure rule matched."
                response["required_next_step"] = "Proceed only through governed review and verifier path."
        except Exception:
            # Do not fail preflight if memory influence encounters an internal issue.
            pass

    receipt = {
        "receipt_type": "aion_preflight_gate_receipt_v1",
        "timestamp_utc": ts,
        "gate": GATE_NAME,
        "input_payload": payload,
        "output_decision": response,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "local_receipts_only": True,
    }

    tmp_path = receipt_abs.with_suffix(".tmp")
    text = json.dumps(receipt, indent=2)
    with open(tmp_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
        f.flush()
    tmp_path.replace(receipt_abs)

    if not receipt_abs.exists():
        raise RuntimeError(f"receipt write failed: {receipt_abs}")

    sha = hashlib.sha256(receipt_abs.read_bytes()).hexdigest()
    response["receipt_written"] = True
    response["receipt_sha256"] = sha
    return response


def _main() -> None:
    parser = argparse.ArgumentParser(description="AION Preflight Gate V1")
    parser.add_argument("--input", required=True, help="Path to input JSON payload")
    args = parser.parse_args()

    payload_path = Path(args.input)
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    out = evaluate_preflight(payload)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    _main()
