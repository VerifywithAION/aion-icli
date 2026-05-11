import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent.parent
RELEASE_GRAPH_PATH = ROOT / "release" / "AION_LIVING_PROOF_GRAPH_V1.json"
REPORT_GRAPH_PATH = ROOT / "reports" / "AION_LIVING_PROOF_GRAPH_V1.md"
RECEIPTS_DIR = ROOT / "receipts" / "introspection"
ENGINE = "AION_INTROSPECTION_ENGINE_V1"


CAPABILITIES = [
    {
        "name": "Public Safe",
        "verifier": "scripts/VERIFY_PUBLIC_SAFE.ps1",
        "expected_marker": "AION_ICLI_PUBLIC_SAFE_VERIFY_OK",
        "docs": "docs/PUBLIC_BOUNDARY.md",
        "report": "reports/CONNECTOR_STACK_ACCEPTANCE_REPORT_V1.md",
        "release_artifact": "release/AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1.json",
    },
    {
        "name": "Feature Consolidation Map V1",
        "verifier": "scripts/VERIFY_AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1.ps1",
        "expected_marker": "AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1_VERIFY_OK",
        "docs": "reports/AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1.md",
        "report": "reports/AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1.md",
        "release_artifact": "release/AION_ICLI_FEATURE_CONSOLIDATION_MAP_V1.json",
    },
    {
        "name": "Evaluate API Adapter V1",
        "verifier": "scripts/VERIFY_AION_EVALUATE_API_V1.ps1",
        "expected_marker": "AION_EVALUATE_API_V1_VERIFY_OK",
        "docs": "docs/AION_EVALUATE_API_V1.md",
        "report": "reports/AION_EVALUATE_API_V1_DEMO_REPORT.md",
        "release_artifact": "release/AION_EVALUATE_API_V1_DEMO_RESULT.json",
    },
    {
        "name": "Preflight Gate V1",
        "verifier": "scripts/VERIFY_AION_PREFLIGHT_GATE_V1.ps1",
        "expected_marker": "AION_PREFLIGHT_GATE_V1_VERIFY_OK",
        "docs": "docs/AION_PREFLIGHT_GATE_V1.md",
        "report": "reports/AION_PREFLIGHT_GATE_V1_DEMO_REPORT.md",
        "release_artifact": "release/AION_PREFLIGHT_GATE_V1_DEMO_RESULT.json",
    },
    {
        "name": "Memory Scars V1",
        "verifier": "scripts/VERIFY_AION_MEMORY_SCARS_V1.ps1",
        "expected_marker": "AION_MEMORY_SCARS_V1_VERIFY_OK",
        "docs": "docs/AION_MEMORY_SCARS_V1.md",
        "report": "reports/AION_MEMORY_SCARS_V1_DEMO_REPORT.md",
        "release_artifact": "release/AION_MEMORY_SCARS_V1_DEMO_RESULT.json",
    },
    {
        "name": "Preflight + Memory Integration V1",
        "verifier": "scripts/VERIFY_AION_PREFLIGHT_MEMORY_INTEGRATION_V1.ps1",
        "expected_marker": "AION_PREFLIGHT_MEMORY_INTEGRATION_V1_VERIFY_OK",
        "docs": "docs/AION_PREFLIGHT_MEMORY_INTEGRATION_V1.md",
        "report": "reports/AION_PREFLIGHT_MEMORY_INTEGRATION_V1_DEMO_REPORT.md",
        "release_artifact": "release/AION_PREFLIGHT_MEMORY_INTEGRATION_V1_DEMO_RESULT.json",
    },
    {
        "name": "Sentinel + Contradiction Engine V1",
        "verifier": "scripts/VERIFY_AION_SENTINEL_CONTRADICTION_V1.ps1",
        "expected_marker": "AION_SENTINEL_CONTRADICTION_V1_VERIFY_OK",
        "docs": "docs/AION_SENTINEL_CONTRADICTION_V1.md",
        "report": "reports/AION_SENTINEL_CONTRADICTION_V1_DEMO_REPORT.md",
        "release_artifact": "release/AION_SENTINEL_CONTRADICTION_V1_DEMO_RESULT.json",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _exists(rel_path: str) -> bool:
    return (ROOT / rel_path).exists()


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with open(temp, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
        handle.flush()
    temp.replace(path)


def _status_for_capability(cap: Dict[str, str]) -> str:
    has_verifier = _exists(cap["verifier"])
    has_docs = _exists(cap["docs"])
    has_report = _exists(cap["report"])
    if not has_verifier:
        return "MISSING_VERIFIER"
    if not has_docs:
        return "MISSING_DOC"
    if not has_report:
        return "MISSING_REPORT"
    return "PROVEN"


def _receipt(payload: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    rid = f"aion_introspection_{uuid.uuid4().hex[:12]}"
    stamp = utc_now()
    name = f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    rel = Path("receipts") / "introspection" / name
    abs_path = ROOT / rel
    doc = {
        "receipt_type": "aion_introspection_engine_receipt_v1",
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
    }


def build_living_proof_graph() -> Dict[str, Any]:
    proven_capabilities: List[Dict[str, Any]] = []
    missing_or_partial: List[str] = []

    for cap in CAPABILITIES:
        status = _status_for_capability(cap)
        entry = {
            "name": cap["name"],
            "verifier": cap["verifier"],
            "expected_marker": cap["expected_marker"],
            "status": status,
            "docs": cap["docs"],
            "report": cap["report"],
            "release_artifact": cap["release_artifact"],
        }
        proven_capabilities.append(entry)
        if status != "PROVEN":
            missing_or_partial.append(f"{cap['name']}:{status}")

    proven_count = sum(1 for x in proven_capabilities if x["status"] == "PROVEN")
    missing_count = len(proven_capabilities) - proven_count

    core_locked_markers = [cap["expected_marker"] for cap in CAPABILITIES if _exists(cap["verifier"]) ]

    graph = {
        "engine": ENGINE,
        "generated_at_utc": utc_now(),
        "repo_root": str(ROOT),
        "proven_capabilities": proven_capabilities,
        "core_locked_markers": core_locked_markers,
        "known_receipt_domains": ["local", "evaluate", "preflight", "memory", "sentinel"],
        "missing_or_partial": missing_or_partial,
        "next_build_pointer": "Self-Patching Sandbox V1",
        "summary": {
            "proven_count": proven_count,
            "missing_count": missing_count,
        },
    }

    _atomic_write(RELEASE_GRAPH_PATH, json.dumps(graph, indent=2))

    lines = [
        "# AION Living Proof Graph V1",
        "",
        f"Generated at UTC: {graph['generated_at_utc']}",
        f"Engine: {ENGINE}",
        "",
        "## Proven capabilities",
    ]
    for item in proven_capabilities:
        lines.append(f"- {item['name']} | {item['status']} | {item['verifier']}")
    lines += [
        "",
        "## Summary",
        f"- proven_count: {proven_count}",
        f"- missing_count: {missing_count}",
        f"- next_build_pointer: {graph['next_build_pointer']}",
    ]
    _atomic_write(REPORT_GRAPH_PATH, "\n".join(lines) + "\n")

    receipt_meta = _receipt({"action": "build"}, graph)
    graph.update(receipt_meta)
    return graph


def status() -> Dict[str, Any]:
    if RELEASE_GRAPH_PATH.exists():
        return json.loads(RELEASE_GRAPH_PATH.read_text(encoding="utf-8-sig"))
    return {"engine": ENGINE, "status": "MISSING_GRAPH", "repo_root": str(ROOT)}


def main() -> None:
    parser = argparse.ArgumentParser(description="AION Introspection Engine V1")
    parser.add_argument("action", choices=["build", "status"])
    args = parser.parse_args()

    if args.action == "build":
        out = build_living_proof_graph()
    else:
        out = status()
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
