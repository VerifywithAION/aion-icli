import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from aion_preflight_gate import evaluate_preflight
from aion_memory_scars import add_scar, evaluate_memory_influence
from aion_sentinel_contradiction import evaluate_claim_consistency
from aion_self_repair_planner import build_repair_plan
from aion_self_patching_sandbox import create_sandbox_patch
from aion_domain_governors import route_domain_governance
from aion_creativity_intuition import analyze_intuition
from aion_introspection_engine import build_living_proof_graph

ROOT = Path(__file__).resolve().parent.parent
RESULT_PATH = ROOT / "release" / "AION_DEMO_ORCHESTRATOR_V1_RESULT.json"
REPORT_PATH = ROOT / "reports" / "AION_DEMO_ORCHESTRATOR_V1_REPORT.md"
RECEIPTS_DIR = ROOT / "receipts" / "demo_orchestrator"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    tmp.replace(path)


def _step(name: str, expected: str, actual: str, status: bool, summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "step": name,
        "expected": expected,
        "actual": actual,
        "status": "PASS" if status else "FAIL",
        "summary": summary,
    }


def _write_receipt(result: Dict[str, Any]) -> Dict[str, Any]:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    rid = f"aion_demo_orch_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    name = f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    rel = Path("receipts") / "demo_orchestrator" / name
    abs_path = ROOT / rel
    receipt = {
        "receipt_type": "aion_demo_orchestrator_receipt_v1",
        "timestamp_utc": stamp,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "REPORTS_AND_RECEIPTS_ONLY",
        "execution": "GOVERNED_ACTION_NOT_EXECUTED",
    }
    _atomic_write(abs_path, json.dumps(receipt, indent=2))
    return {
        "receipt_id": rid,
        "receipt_path": str(rel).replace("\\", "/"),
        "receipt_abs_path": str(abs_path),
        "receipt_written": abs_path.exists(),
        "receipt_sha256": hashlib.sha256(abs_path.read_bytes()).hexdigest(),
        "repo_root": str(ROOT),
    }


def run_demo_orchestration() -> Dict[str, Any]:
    steps: List[Dict[str, Any]] = []

    preflight_payload = {
        "source": "Agent",
        "action_type": "wallet_action",
        "target": "web3 wallet helper",
        "intent": "claim ready to ship wallet interaction helper",
        "risk_signals": ["execution", "mutation"],
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
    preflight = evaluate_preflight(preflight_payload)
    steps.append(_step("preflight", "BLOCK", preflight.get("governance_decision", ""), preflight.get("governance_decision") == "BLOCK", {"risk_level": preflight.get("risk_level")}))

    scar = {
        "scar_id": "demo_wallet_signature_without_verifier",
        "trigger": "agent wants execution/signature flow without verifier",
        "harm": "unsafe wallet action may be trusted without admissible proof",
        "repair": "require verifier and human review",
        "future_rule": "BLOCK execution/signature flows when verifier is missing",
        "severity": "HIGH",
        "tags": ["execution", "signature", "verifier"],
        "public_safe": True,
    }
    add_scar(scar)
    mem = evaluate_memory_influence(
        {
            "source": "PreflightGate",
            "action_type": "wallet_action",
            "risk_signals": ["execution", "signature"],
            "missing_controls": ["verifier", "rollback", "dry_run"],
            "summary": "ready to ship wallet helper without verifier",
        }
    )
    steps.append(_step("memory", "BLOCK", mem.get("recommended_decision_bias", ""), mem.get("recommended_decision_bias") == "BLOCK", {"matched_scars": len(mem.get("matched_scars", []))}))

    sentinel = evaluate_claim_consistency(
        {
            "claim": "ready_to_ship",
            "artifact": "docs/DEMO_TARGET.md",
            "evidence": {
                "verifier": False,
                "receipt": True,
                "rollback": False,
                "dry_run": False,
                "human_review": False,
            },
            "risk": {
                "risk_level": "HIGH",
                "decision": "BLOCK",
                "missing_controls": ["verifier", "rollback", "dry_run"],
            },
            "context": "wallet helper claim conflicts with governance evidence",
        }
    )
    steps.append(_step("sentinel", "CONTRADICTION", sentinel.get("consistency_status", ""), sentinel.get("consistency_status") == "CONTRADICTION", {"severity": sentinel.get("severity"), "decision": sentinel.get("governance_decision")}))

    repair = build_repair_plan(
        {
            "source": "Sentinel",
            "problem_type": "contradiction",
            "governance_decision": "BLOCK",
            "risk_level": "HIGH",
            "missing_controls": ["verifier", "rollback", "dry_run"],
            "contradictions": ["ready_to_ship_without_verifier"],
            "missing_artifacts": [],
            "context": "claim/evidence mismatch for wallet readiness",
        }
    )
    steps.append(_step("self_repair", "PLAN_ONLY", repair.get("repair_status", ""), repair.get("repair_status") == "PLAN_ONLY", {"repair_items": len(repair.get("repair_plan", []))}))

    sandbox = create_sandbox_patch(
        {
            "source": "SelfRepairPlanner",
            "target_file": "docs/DEMO_TARGET.md",
            "original_content": "status: missing verifier",
            "proposed_content": "status: verifier and human-review required before wallet execution",
            "reason": "demonstrate admissibility patch proposal in sandbox",
            "verification_marker": "AION_DEMO_TARGET_PATCH_OK",
        }
    )
    sandbox_ok = (
        sandbox.get("patch_status") == "SANDBOXED_ONLY"
        and sandbox.get("production_mutation") == "NOT_PERFORMED"
        and sandbox.get("rollback_available") is True
        and sandbox.get("dry_run_verified") is True
    )
    steps.append(_step("sandbox", "SANDBOXED_ONLY", sandbox.get("patch_status", ""), sandbox_ok, {"production_mutation": sandbox.get("production_mutation"), "rollback_available": sandbox.get("rollback_available")}))

    domain = route_domain_governance(
        {
            "domain": "wallet",
            "source": "Manual",
            "action": "wallet helper sign+transfer request",
            "risk_level": "HIGH",
            "signals": ["signature", "funds_at_risk"],
            "controls": {
                "verifier": True,
                "receipt": True,
                "rollback": False,
                "dry_run": True,
                "human_review": False,
            },
            "requested_execution": False,
        }
    )
    steps.append(_step("domain_governor", "BLOCK", domain.get("governance_decision", ""), domain.get("governance_decision") == "BLOCK", {"selected_governor": domain.get("selected_governor")}))

    intuition = analyze_intuition(
        {
            "source": "DomainGovernor",
            "context": "wallet claim/evidence mismatch demo",
            "signals": {
                "contradictions": 1,
                "memory_matches": max(len(mem.get("matched_scars", [])), 1),
                "missing_controls": ["verifier", "rollback", "dry_run"],
                "risk_signals": ["signature", "funds_at_risk", "execution"],
                "domain": "wallet",
                "governance_decision": "BLOCK",
                "evidence_complete": False,
                "proof_graph_missing_count": 0,
            },
        }
    )
    steps.append(_step("intuition", "CRITICAL_SIGNAL", intuition.get("intuition_class", ""), intuition.get("intuition_class") == "CRITICAL_SIGNAL", {"intuition_score": intuition.get("intuition_score")}))

    graph = build_living_proof_graph()
    graph_written = (ROOT / "release" / "AION_LIVING_PROOF_GRAPH_V1.json").exists()
    steps.append(_step("introspection", "GRAPH_WRITTEN", "GRAPH_WRITTEN" if graph_written else "MISSING", graph_written, {"next_build_pointer": graph.get("next_build_pointer")}))

    final_pass = all(s["status"] == "PASS" for s in steps)

    result: Dict[str, Any] = {
        "orchestrator": "AION_DEMO_ORCHESTRATOR_V1",
        "generated_at_utc": utc_now(),
        "demo_thesis": "Generation is not governance. AION governs admissibility before consequence.",
        "scenario": "AI agent claims a Web3 wallet interaction helper is ready to ship, but it includes execution/signature/funds-at-risk signals and lacks verifier/human-review proof.",
        "steps": steps,
        "final_demo_verdict": "PASS" if final_pass else "FAIL",
        "public_safe": True,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "REPORTS_AND_RECEIPTS_ONLY",
        "execution": "GOVERNED_ACTION_NOT_EXECUTED",
    }

    result.update(_write_receipt(result))

    _atomic_write(RESULT_PATH, json.dumps(result, indent=2))

    lines = [
        "# AION Demo Orchestrator V1 Report",
        "",
        f"Generated at UTC: {result['generated_at_utc']}",
        f"Final verdict: {result['final_demo_verdict']}",
        "",
        "## Step Results",
    ]
    for s in steps:
        lines.append(f"- {s['step']}: {s['actual']} ({s['status']})")
    lines += [
        "",
        "## Thesis",
        result["demo_thesis"],
    ]
    _atomic_write(REPORT_PATH, "\n".join(lines) + "\n")

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="AION Demo Orchestrator V1")
    parser.add_argument("action", choices=["run"])
    args = parser.parse_args()
    if args.action == "run":
        print(json.dumps(run_demo_orchestration(), indent=2))


if __name__ == "__main__":
    main()
