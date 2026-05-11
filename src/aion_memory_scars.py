import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent.parent
MEMORY_DIR = ROOT / ".aion_public" / "memory"
MEMORY_PATH = MEMORY_DIR / "memory_scars_v1.jsonl"
RECEIPTS_DIR = ROOT / "receipts" / "memory"
ENGINE = "AION_MEMORY_SCARS_V1"
REQUIRED_SCAR_FIELDS = ["scar_id", "trigger", "harm", "repair", "future_rule", "severity", "tags", "public_safe"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _safe_text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _write_atomic(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    tmp.replace(path)


def _write_receipt(operation: str, payload: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    receipt_id = f"aion_memory_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    name = f"{stamp.replace(':', '').replace('-', '')}_{receipt_id}.json"
    rel = Path("receipts") / "memory" / name
    abs_path = ROOT / rel
    receipt = {
        "receipt_type": "aion_memory_scars_receipt_v1",
        "engine": ENGINE,
        "operation": operation,
        "timestamp_utc": stamp,
        "input_payload": payload,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "local_receipts_only": True,
    }
    _write_atomic(abs_path, json.dumps(receipt, indent=2))
    sha = hashlib.sha256(abs_path.read_bytes()).hexdigest()
    return {
        "receipt_id": receipt_id,
        "receipt_path": str(rel).replace("\\", "/"),
        "receipt_abs_path": str(abs_path),
        "receipt_written": abs_path.exists(),
        "receipt_sha256": sha,
        "repo_root": str(ROOT),
    }


def load_scars() -> List[Dict[str, Any]]:
    if not MEMORY_PATH.exists():
        return []
    scars = []
    for line in MEMORY_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            scars.append(json.loads(line))
        except Exception:
            continue
    return scars


def _validate_scar(scar: Dict[str, Any]) -> List[str]:
    missing = []
    for field in REQUIRED_SCAR_FIELDS:
        if field not in scar:
            missing.append(field)
    return missing


def add_scar(scar: Dict[str, Any]) -> Dict[str, Any]:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    missing = _validate_scar(scar)
    if missing:
        result = {
            "engine": ENGINE,
            "status": "INVALID",
            "reason": "Missing required scar fields.",
            "missing_fields": missing,
        }
        result.update(_write_receipt("add", scar, result))
        return result

    sanitized = {
        "scar_id": _safe_text(scar.get("scar_id")),
        "trigger": _safe_text(scar.get("trigger")),
        "harm": _safe_text(scar.get("harm")),
        "repair": _safe_text(scar.get("repair")),
        "future_rule": _safe_text(scar.get("future_rule")),
        "severity": _safe_text(scar.get("severity")).upper(),
        "tags": [_safe_text(t).lower() for t in (scar.get("tags") or []) if _safe_text(t)],
        "public_safe": bool(scar.get("public_safe")),
    }
    if not sanitized["public_safe"]:
        result = {
            "engine": ENGINE,
            "status": "REJECTED",
            "reason": "Scar rejected because public_safe is false.",
        }
        result.update(_write_receipt("add", scar, result))
        return result

    scars = load_scars()
    scars = [s for s in scars if _safe_text(s.get("scar_id")) != sanitized["scar_id"]]
    scars.append(sanitized)
    content = "\n".join(json.dumps(s, separators=(",", ":")) for s in scars) + "\n"
    _write_atomic(MEMORY_PATH, content)

    result = {
        "engine": ENGINE,
        "status": "ADDED",
        "scar_id": sanitized["scar_id"],
        "memory_store_path": str(MEMORY_PATH.relative_to(ROOT)).replace("\\", "/"),
        "memory_store_abs_path": str(MEMORY_PATH),
        "memory_store_count": len(scars),
    }
    result.update(_write_receipt("add", sanitized, result))
    return result


def evaluate_memory_influence(payload: Dict[str, Any]) -> Dict[str, Any]:
    scars = load_scars()
    risk_signals = {_safe_text(x).lower() for x in (payload.get("risk_signals") or [])}
    missing_controls = {_safe_text(x).lower() for x in (payload.get("missing_controls") or [])}
    action_type = _safe_text(payload.get("action_type")).lower()
    summary = _safe_text(payload.get("summary")).lower()

    matched = []
    highest = "NONE"
    bias = "NONE"
    for scar in scars:
        tags = {_safe_text(t).lower() for t in (scar.get("tags") or [])}
        trigger = _safe_text(scar.get("trigger")).lower()
        hit = bool(tags.intersection(risk_signals.union(missing_controls))) or (
            action_type and action_type in trigger
        ) or (trigger and trigger in summary)
        if not hit:
            continue
        matched.append(
            {
                "scar_id": scar.get("scar_id"),
                "severity": _safe_text(scar.get("severity")).upper(),
                "future_rule": scar.get("future_rule"),
            }
        )
        sev = _safe_text(scar.get("severity")).upper()
        if sev == "HIGH":
            highest = "RAISE_TO_BLOCK"
            bias = "BLOCK"
        elif sev == "MEDIUM" and highest != "RAISE_TO_BLOCK":
            highest = "RAISE_TO_WARN"
            bias = "WARN"

    reason = "No matching scars found."
    if matched:
        reason = "Memory scars matched event risk signals and missing controls."

    result = {
        "engine": ENGINE,
        "matched_scars": matched,
        "memory_risk_adjustment": highest,
        "recommended_decision_bias": bias,
        "reason": reason,
    }
    result.update(_write_receipt("evaluate", payload, result))
    return result


def _cli() -> None:
    parser = argparse.ArgumentParser(description="AION Memory Scars V1")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add")
    p_add.add_argument("--input", required=True)
    p_eval = sub.add_parser("evaluate")
    p_eval.add_argument("--input", required=True)
    sub.add_parser("list")
    args = parser.parse_args()

    if args.cmd == "list":
        print(json.dumps({"engine": ENGINE, "scars": load_scars()}, indent=2))
        return
    if args.cmd == "add":
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        print(json.dumps(add_scar(payload), indent=2))
        return
    if args.cmd == "evaluate":
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        print(json.dumps(evaluate_memory_influence(payload), indent=2))
        return


if __name__ == "__main__":
    _cli()
