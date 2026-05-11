import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parent.parent
RUNTIME_ROOT = ROOT / "release_runtime" / "sandbox"
RECEIPTS_DIR = ROOT / "receipts" / "sandbox"
ENGINE = "AION_SELF_PATCHING_SANDBOX_V1"
FORBIDDEN_PARTS = {".git", ".env", "secrets", "private", "node_modules", "__pycache__"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as h:
        h.write(content)
        h.flush()
    tmp.replace(path)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe_target(rel_target: str) -> bool:
    p = Path(rel_target)
    if p.is_absolute():
        return False
    for part in p.parts:
        low = str(part).lower()
        if low == "..":
            return False
        if low in FORBIDDEN_PARTS:
            return False
    return True


def _receipt(payload: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    rid = f"aion_sandbox_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    name = f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    rel = Path("receipts") / "sandbox" / name
    abs_path = ROOT / rel

    doc = {
        "receipt_type": "aion_self_patching_sandbox_receipt_v1",
        "timestamp_utc": stamp,
        "engine": ENGINE,
        "input_payload": payload,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": result.get("mutation", "SANDBOX_ONLY"),
        "execution": "NOT_PERFORMED",
    }
    _atomic_write(abs_path, json.dumps(doc, indent=2))
    return {
        "receipt_id": rid,
        "receipt_path": str(rel).replace("\\", "/"),
        "receipt_abs_path": str(abs_path),
        "receipt_written": abs_path.exists(),
        "receipt_sha256": _sha(abs_path),
    }


def create_sandbox_patch(payload: Dict[str, Any]) -> Dict[str, Any]:
    target_file = str(payload.get("target_file") or "").strip()
    original_content = str(payload.get("original_content") or "")
    proposed_content = str(payload.get("proposed_content") or "")

    result: Dict[str, Any] = {
        "sandbox": ENGINE,
        "sandbox_id": f"sandbox_{uuid.uuid4().hex[:10]}",
        "patch_status": "REJECTED",
        "target_file": target_file,
        "production_mutation": "NOT_PERFORMED",
        "sandbox_mutation": "NOT_PERFORMED",
        "rollback_available": False,
        "dry_run_verified": False,
        "verification_marker": str(payload.get("verification_marker") or ""),
        "hashes": {
            "original_sha256": "",
            "proposed_sha256": "",
            "rollback_sha256": "",
        },
        "sandbox_paths": {
            "sandbox_root": "",
            "original": "",
            "proposed": "",
            "rollback": "",
            "summary": "",
        },
        "forbidden_actions": [
            "do_not_patch_production_without_human_review",
            "do_not_remove_rollback",
            "do_not_claim_applied_without_apply_gate",
        ],
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "SANDBOX_ONLY",
        "execution": "NOT_PERFORMED",
        "repo_root": str(ROOT),
    }

    if not _safe_target(target_file):
        result["reason"] = "Rejected unsafe target_file path."
        result.update(_receipt(payload, result))
        return result

    sandbox_root = RUNTIME_ROOT / result["sandbox_id"]
    sandbox_root.mkdir(parents=True, exist_ok=True)

    original_path = sandbox_root / "original.txt"
    proposed_path = sandbox_root / "proposed.txt"
    rollback_path = sandbox_root / "rollback.txt"
    summary_path = sandbox_root / "patch_summary.json"

    _atomic_write(original_path, original_content)
    _atomic_write(proposed_path, proposed_content)
    _atomic_write(rollback_path, original_content)

    orig_sha = _sha(original_path)
    prop_sha = _sha(proposed_path)
    roll_sha = _sha(rollback_path)

    rollback_available = roll_sha == orig_sha
    dry_run_verified = original_path.exists() and proposed_path.exists() and rollback_available

    summary = {
        "engine": ENGINE,
        "sandbox_id": result["sandbox_id"],
        "target_file": target_file,
        "reason": str(payload.get("reason") or ""),
        "verification_marker": str(payload.get("verification_marker") or ""),
        "production_mutation": "NOT_PERFORMED",
        "sandbox_mutation": "PERFORMED",
        "rollback_available": rollback_available,
        "dry_run_verified": dry_run_verified,
        "hashes": {
            "original_sha256": orig_sha,
            "proposed_sha256": prop_sha,
            "rollback_sha256": roll_sha,
        },
    }
    _atomic_write(summary_path, json.dumps(summary, indent=2))

    result.update(
        {
            "patch_status": "SANDBOXED_ONLY",
            "sandbox_mutation": "PERFORMED",
            "rollback_available": rollback_available,
            "dry_run_verified": dry_run_verified,
            "hashes": {
                "original_sha256": orig_sha,
                "proposed_sha256": prop_sha,
                "rollback_sha256": roll_sha,
            },
            "sandbox_paths": {
                "sandbox_root": str(sandbox_root),
                "original": str(original_path),
                "proposed": str(proposed_path),
                "rollback": str(rollback_path),
                "summary": str(summary_path),
            },
        }
    )

    result.update(_receipt(payload, result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="AION Self-Patching Sandbox V1")
    parser.add_argument("--input", required=True, help="Path to sandbox input JSON")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    out = create_sandbox_patch(payload)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
