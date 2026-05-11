import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "self_repair"
PLANNER = "AION_SELF_REPAIR_PLANNER_V1"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _text(v: Any) -> str:
    return "" if v is None else str(v).strip()


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as h:
        h.write(content)
        h.flush()
    tmp.replace(path)


def _add_step(steps: List[Dict[str, Any]], title: str, rationale: str, surface: str, required_artifact: str, marker: str) -> None:
    sid = f"repair_{len(steps)+1:03d}"
    steps.append(
        {
            "step_id": sid,
            "title": title,
            "rationale": rationale,
            "target_surface": surface,
            "required_artifact": required_artifact,
            "verification_marker": marker,
        }
    )


def build_repair_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    problem_type = _text(payload.get("problem_type")).lower()
    risk_level = _text(payload.get("risk_level")).upper() or "UNKNOWN"
    missing_controls = [str(x).lower() for x in (payload.get("missing_controls") or [])]
    contradictions = [str(x) for x in (payload.get("contradictions") or [])]
    missing_artifacts = [str(x) for x in (payload.get("missing_artifacts") or [])]

    repair_plan: List[Dict[str, Any]] = []

    if "verifier" in missing_controls:
        _add_step(
            repair_plan,
            "Create verifier for missing control",
            "No verifier means the claim cannot be proven deterministically.",
            "scripts",
            "scripts/VERIFY_<TARGET>_V1.ps1",
            "AION_<TARGET>_VERIFY_OK",
        )
    if "rollback" in missing_controls:
        _add_step(
            repair_plan,
            "Add rollback procedure",
            "Mutation-risk actions require explicit rollback to remain governable.",
            "policy",
            "docs/<TARGET>_ROLLBACK_PLAN.md",
            "AION_<TARGET>_ROLLBACK_READY",
        )
    if "dry_run" in missing_controls:
        _add_step(
            repair_plan,
            "Add dry-run path",
            "Dry-run provides non-destructive pre-execution validation.",
            "scripts",
            "scripts/RUN_<TARGET>_DRY_RUN.ps1",
            "AION_<TARGET>_DRY_RUN_OK",
        )

    if problem_type == "receipt_failure":
        _add_step(
            repair_plan,
            "Harden receipt writer",
            "Receipt path failure breaks proof chain and must be fixed first.",
            "src",
            "root-anchored atomic receipt write with sha256",
            "AION_RECEIPT_PATH_HARDENING_OK",
        )

    if problem_type == "contradiction" or contradictions:
        _add_step(
            repair_plan,
            "Downgrade claim until evidence aligns",
            "Contradictory claims must be downgraded to REVIEW_ONLY pending proof.",
            "policy",
            "claim downgrade + explicit evidence requirements",
            "AION_CONTRADICTION_ALIGNMENT_OK",
        )
        _add_step(
            repair_plan,
            "Require verifier and receipt evidence",
            "Claim cannot return to ready state until verifier marker and receipt exist.",
            "reports",
            "report with verifier marker + receipt reference",
            "AION_EVIDENCE_ALIGNMENT_OK",
        )

    if problem_type == "incomplete_evidence":
        _add_step(
            repair_plan,
            "Capture missing evidence surfaces",
            "Incomplete evidence requires explicit capture before admissibility.",
            "reports",
            "evidence report with artifact + marker linkage",
            "AION_EVIDENCE_CAPTURE_OK",
        )

    if problem_type == "missing_proof_surface" or missing_artifacts:
        _add_step(
            repair_plan,
            "Add missing docs/verifier/report/release artifacts",
            "Missing proof surfaces block admissibility review.",
            "docs",
            ", ".join(missing_artifacts) if missing_artifacts else "docs + scripts + reports + release artifact",
            "AION_PROOF_SURFACE_COMPLETE_OK",
        )

    if not repair_plan:
        _add_step(
            repair_plan,
            "Collect complete governance context",
            "Unknown problem type needs bounded evidence before planning.",
            "policy",
            "normalized payload with controls/evidence/receipts",
            "AION_REPAIR_CONTEXT_READY",
        )

    required_human_review = risk_level == "HIGH" or _text(payload.get("governance_decision")).upper() in {"BLOCK", "REVIEW_ONLY"}

    result: Dict[str, Any] = {
        "planner": PLANNER,
        "repair_status": "PLAN_ONLY",
        "risk_level": risk_level,
        "repair_plan": repair_plan,
        "required_human_review": required_human_review,
        "admissibility_after_repair": "RECHECK_REQUIRED",
        "forbidden_actions": [
            "do_not_execute_target_action",
            "do_not_patch_without_sandbox",
            "do_not_claim_ready_without_verifier",
        ],
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED_ON_TARGET",
        "execution": "NOT_PERFORMED",
        "repo_root": str(ROOT),
    }

    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    rid = f"aion_self_repair_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    name = f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    rel = Path("receipts") / "self_repair" / name
    abs_path = ROOT / rel

    receipt = {
        "receipt_type": "aion_self_repair_planner_receipt_v1",
        "timestamp_utc": stamp,
        "planner": PLANNER,
        "input_payload": payload,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED_ON_TARGET",
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
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="AION Self-Repair Planner V1")
    parser.add_argument("--input", required=True, help="Path to planner input JSON")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    out = build_repair_plan(payload)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
