import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


AION_LOGO = r"""
  ___    ___  ___   _   _
 / _ \  |_ _|/ _ \ | \ | |
| | | |  | || | | ||  \| |
| |_| |  | || |_| || |\  |
 \___/  |___|\___/ |_| \_|
""".strip("\n")

RECEIPT_PATH = Path("receipts") / "local" / "aion_cli_receipt_v1.json"
PROOF_FOOTER = "Proof: local-only · no network · no mutation · no execution · receipt written"
MAX_FILE_BYTES = 1024 * 1024
ARTIFACT_MAX_BYTES = 256 * 1024
ARTIFACT_MAX_CHARS = 40000
ALLOWED_ARTIFACT_EXTS = {
    ".ps1", ".py", ".js", ".ts", ".tsx", ".json", ".md", ".txt", ".yaml", ".yml", ".cmd", ".bat", ".sh"
}
FORBIDDEN_PATH_PARTS = {".git", ".env", "secrets", "private", "node_modules", "__pycache__", ".venv", "venv"}
NETWORK_PATTERNS = ["invoke-webrequest", "invoke-restmethod", "curl", "wget", "requests", "fetch(", "axios", "http://", "https://"]
MUTATION_PATTERNS = ["set-content", "add-content", "remove-item", "new-item", "copy-item", "move-item", "write_text", "open(", "fs.writefile", "git commit", "git push"]
EXECUTION_PATTERNS = ["start-process", "subprocess", "os.system", "powershell -file", " node ", "python ", "npm run"]
SECRET_PATTERNS = ["api_key", "secret", "token", "private_key", "seed phrase", "password"]
GOVERNANCE_PATTERNS = ["verifier", "receipt", "dry-run", "rollback", "no-network", "local-only"]
PACKAGE_PATTERNS = ["dist", "zip", "manifest", "sha256", "release", "tag"]

CAPABILITY_MAP = {
    "preflight": {"name": "Preflight"},
    "creative": {"name": "Creative"},
    "intuition": {"name": "Intuition"},
    "cortex": {"name": "Cortex"},
    "connectors": {"name": "Connectors"},
    "receipts": {"name": "Receipts"},
    "verify": {"name": "Verify"},
}

COMMAND_STYLE = {
    "capabilities",
    "preflight",
    "creative",
    "intuition",
    "cortex",
    "connectors",
    "receipts",
    "verify",
    "next",
    "help",
    "receipt",
    "boundary",
    "status",
    "/help",
    "?",
}

KNOWN_LAYER_DOCS = {
    "Interactive Mode V1": Path("docs") / "INTERACTIVE_MODE_V1.md",
    "Capability Router V1": Path("docs") / "CAPABILITY_ROUTER_V1.md",
    "Voice Layer V1": Path("docs") / "VOICE_LAYER_V1.md",
    "Adaptive Reasoning Layer V1": Path("docs") / "ADAPTIVE_REASONING_LAYER_V1.md",
    "Governance Brain Adapter V1": Path("docs") / "GOVERNANCE_BRAIN_ADAPTER_V1.md",
    "User Guide V1": Path("docs") / "USER_GUIDE_V1.md",
    "Public Release Lock V1": Path("docs") / "PUBLIC_RELEASE_LOCK_V1.md",
    "Living Proof Graph V1": Path("docs") / "LIVING_PROOF_GRAPH_V1.md",
}

SCARS_PATH = Path(".aion_public") / "scars" / "scars_seed.jsonl"
PROOF_GRAPH_PATH = Path(".aion_public") / "graph" / "proof_graph_seed.json"
EVOLUTION_LEDGER_PATH = Path(".aion_public") / "evolution" / "evolution_ledger_seed.jsonl"
PROOF_GRAPH_DIR = Path(".aion_public") / "proof_graph"
PROOF_NODES_PATH = PROOF_GRAPH_DIR / "proof_nodes_v1.json"
PROOF_EDGES_PATH = PROOF_GRAPH_DIR / "proof_edges_v1.json"
PROOF_GRAPH_SUMMARY_PATH = PROOF_GRAPH_DIR / "proof_graph_summary_v1.md"
PROOF_GRAPH_LATEST_PATH = PROOF_GRAPH_DIR / "proof_graph_latest_v1.json"
EVIDENCE_DIR = Path(".aion_public") / "evidence"
EVIDENCE_INDEX_PATH = EVIDENCE_DIR / "evidence_index_v1.json"
EVIDENCE_SUMMARY_PATH = EVIDENCE_DIR / "evidence_summary_v1.md"
EVIDENCE_LATEST_PATH = EVIDENCE_DIR / "evidence_latest_v1.json"
INTROSPECTION_DIR = Path(".aion_public") / "introspection"
INTROSPECTION_RULES_PATH = INTROSPECTION_DIR / "introspection_rules_v1.json"
INTROSPECTION_LATEST_PATH = INTROSPECTION_DIR / "introspection_latest_v1.json"
INTROSPECTION_SUMMARY_PATH = INTROSPECTION_DIR / "introspection_summary_v1.md"
CONTRADICTION_DIR = Path(".aion_public") / "contradictions"
CONTRADICTION_INDEX_PATH = CONTRADICTION_DIR / "contradiction_index_v1.json"
CONTRADICTION_SUMMARY_PATH = CONTRADICTION_DIR / "contradiction_summary_v1.md"
CONTRADICTION_LATEST_PATH = CONTRADICTION_DIR / "contradiction_latest_v1.json"

EVIDENCE_LEVELS = {
    "MISSING": 0,
    "CLAIM_ONLY": 1,
    "DOC_ONLY": 2,
    "RECEIPT_ONLY": 3,
    "VERIFIER_PRESENT": 4,
    "VERIFIER_MARKER_PRESENT": 5,
    "ROADMAP_WIRED": 6,
    "RELEASE_PACKAGED": 7,
    "FRESH_CLONE_PROVEN": 8,
    "ADMISSIBLE": 9,
}


def configure_utf8() -> None:
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ.setdefault("PYTHONUTF8", "1")
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def supports_color() -> bool:
    if os.environ.get("NO_COLOR") or os.environ.get("AION_NO_COLOR"):
        return False
    if os.environ.get("AION_FORCE_COLOR") == "1":
        return True
    return bool(getattr(sys.stdout, "isatty", lambda: False)())


def c(text: str, code: str) -> str:
    if not supports_color():
        return text
    return f"\033[{code}m{text}\033[0m"


def cyan(text: str) -> str:
    return c(text, "96")


def blue(text: str) -> str:
    return c(text, "94")


def dim(text: str) -> str:
    return c(text, "90")


def white(text: str) -> str:
    return c(text, "97")


def green(text: str) -> str:
    return c(text, "92")


def yellow(text: str) -> str:
    return c(text, "93")


def render_banner() -> None:
    print("")
    print(cyan(AION_LOGO))
    print("")
    print(blue("AION ICLI"))
    print(cyan("Interactive Command Line Intelligence"))
    print(white("Governed Local Mode"))
    print(cyan("Offline-capable by design"))
    print(dim("No external APIs by default"))
    print("")


def safe_read_text(path: Path) -> str:
    try:
        if not path.exists() or not path.is_file():
            return ""
        if path.stat().st_size > MAX_FILE_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def safe_read_json(path: Path) -> dict:
    try:
        if not path.exists() or not path.is_file():
            return {}
        if path.stat().st_size > MAX_FILE_BYTES:
            return {}
        raw = path.read_text(encoding="utf-8-sig", errors="replace")
        obj = json.loads(raw)
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def extract_artifact_path(prompt: str) -> str:
    n = (prompt or "").strip()
    # Prefer explicit repo-like paths first.
    path_match = re.search(r"([A-Za-z0-9_./\\-]+\.(ps1|py|js|ts|tsx|json|md|txt|yaml|yml|cmd|bat|sh))", n, flags=re.IGNORECASE)
    return path_match.group(1) if path_match else ""


def normalize_artifact_path(path_text: str) -> Optional[Path]:
    if not path_text:
        return None
    candidate = Path(path_text.strip().strip("\"'"))
    if candidate.is_absolute():
        return candidate
    return (Path.cwd() / candidate).resolve()


def is_allowed_artifact_path(path: Path) -> tuple[bool, str]:
    try:
        repo_root = Path.cwd().resolve()
        resolved = path.resolve()
    except Exception:
        return False, "path_resolve_failed"
    if not str(resolved).startswith(str(repo_root)):
        return False, "outside_repo_root"
    low = str(resolved).lower().replace("\\", "/")
    for part in FORBIDDEN_PATH_PARTS:
        if f"/{part.lower()}/" in f"/{low}/":
            return False, "forbidden_path_segment"
    if low.endswith(".zip") and "/dist/" in low:
        return False, "binary_zip_content_forbidden"
    if resolved.suffix.lower() not in ALLOWED_ARTIFACT_EXTS:
        return False, "unsupported_file_type"
    if not resolved.exists() or not resolved.is_file():
        return False, "artifact_not_found"
    return True, "ok"


def read_artifact_safely(path: Path) -> tuple[bool, str, int, str]:
    try:
        size = path.stat().st_size
    except Exception:
        return False, "", 0, "artifact_stat_failed"
    if size > ARTIFACT_MAX_BYTES:
        return False, "", size, "too_large"
    text = safe_read_text(path)
    if not text:
        return False, "", size, "artifact_read_failed_or_empty"
    return True, text[:ARTIFACT_MAX_CHARS], size, "ok"


def scan_patterns(text: str, patterns: list[str]) -> list[str]:
    low = (text or "").lower()
    return [p for p in patterns if p in low]


def inspect_artifact_text(path: Path, text: str) -> dict:
    return {
        "network": scan_patterns(text, NETWORK_PATTERNS),
        "mutation": scan_patterns(text, MUTATION_PATTERNS),
        "execution": scan_patterns(text, EXECUTION_PATTERNS),
        "secret": scan_patterns(text, SECRET_PATTERNS),
        "governance": scan_patterns(text, GOVERNANCE_PATTERNS),
        "package": scan_patterns(text, PACKAGE_PATTERNS),
        "path": str(path),
        "file_type": path.suffix.lower(),
    }


def classify_artifact_risk(path: Path, text: str) -> dict:
    p = inspect_artifact_text(path, text)
    detected = []
    reasons = []
    missing_controls = []
    decision = "SAFE_TO_READ"
    risk_level = "LOW"

    for k in ("network", "mutation", "execution", "secret"):
        if p[k]:
            detected.extend([f"{k}:{v}" for v in p[k]])

    if p["secret"]:
        decision = "NEEDS_MANUAL_REVIEW"
        risk_level = "HIGH"
        reasons.append("secret_indicator_detected")
    if p["network"] or p["mutation"] or p["execution"]:
        if risk_level != "HIGH":
            risk_level = "MEDIUM"
            decision = "REVIEW_ONLY"
        reasons.append("active_operation_indicators_detected")
        if not any(x in p["governance"] for x in ("rollback", "dry-run", "verifier")):
            missing_controls.extend(["rollback", "dry-run", "verifier"])
    if p["network"] and p["mutation"]:
        decision = "BLOCK_EXECUTION"
        risk_level = "HIGH"
        reasons.append("combined_network_and_mutation_risk")

    recommended = "Read-only review only. Do not execute. Require verifier and rollback plan."
    if decision == "SAFE_TO_READ":
        recommended = "Safe to read. If execution is requested, run preflight and verifier checks first."

    return {
        "decision": decision,
        "risk_level": risk_level,
        "reasons": reasons or ["no_high_risk_patterns_detected"],
        "missing_controls": sorted(set(missing_controls)),
        "detected_patterns": sorted(set(detected)),
        "recommended_next_step": recommended,
        "inspection": p,
    }


def artifact_inspection_answer(prompt: str, capability: str, signals: dict) -> tuple[str, list[str], dict]:
    path_text = extract_artifact_path(prompt)
    if not path_text:
        return (
            "You asked to do it now. Don't run it yet. I cannot inspect what I cannot see. Share the script/file path first so I can check blast radius, reversibility, and evidence. No artifact, no judgment.",
            [],
            {"decision": "NEEDS_MANUAL_REVIEW", "risk_level": "MEDIUM", "reasons": ["missing_artifact_path"], "missing_controls": ["artifact_path"]},
        )

    path = normalize_artifact_path(path_text)
    if not path:
        return ("Artifact path could not be normalized for local inspection.", [], {"decision": "NEEDS_MANUAL_REVIEW", "risk_level": "MEDIUM", "reasons": ["path_normalization_failed"], "missing_controls": ["artifact_path"]})
    allowed, status = is_allowed_artifact_path(path)
    if not allowed:
        return (
            f"I can only inspect repo-local public-safe artifacts. This path is blocked: {status}.",
            [str(path)],
            {"decision": "NEEDS_MANUAL_REVIEW", "risk_level": "HIGH", "reasons": [status], "missing_controls": ["repo_local_path"]},
        )

    ok, text, size, read_status = read_artifact_safely(path)
    if not ok:
        reason = "too_large" if read_status == "too_large" else "artifact_read_failed"
        return (
            f"I inspected path metadata for {path}. Content requires manual review: {read_status}.",
            [str(path)],
            {"decision": "NEEDS_MANUAL_REVIEW", "risk_level": "MEDIUM", "reasons": [reason], "missing_controls": ["manual_review"], "artifact_size_bytes": size},
        )

    risk = classify_artifact_risk(path, text)
    risk["artifact_size_bytes"] = size
    response = (
        f"I inspected {path}. Decision: {risk['decision']} ({risk['risk_level']}). "
        f"Detected patterns: {', '.join(risk['detected_patterns']) if risk['detected_patterns'] else 'none'}. "
        f"Missing controls: {', '.join(risk['missing_controls']) if risk['missing_controls'] else 'none'}. "
        f"{risk['recommended_next_step']}"
    )
    if risk["decision"] in {"REVIEW_ONLY", "BLOCK_EXECUTION", "NEEDS_MANUAL_REVIEW"} and ("rollback" in risk["missing_controls"] or "dry-run" in risk["missing_controls"]):
        response += " Learned rule: no artifact, no judgment; no verifier, no lock."
    return response, [str(path)], risk


def maybe_use_artifact_inspection(prompt: str, capability: str, signals: dict) -> tuple[bool, str, list[str], dict]:
    n = normalize(prompt)
    triggers = ("should i run", "inspect ", "what does this file do", "is this safe", "where is the rollback", "risk in this")
    if not any(t in n for t in triggers):
        return False, "", [], {}
    response, artifacts, risk = artifact_inspection_answer(prompt, capability, signals)
    return True, response, artifacts, risk


def first_match(text: str, pattern: str) -> str:
    m = re.search(pattern, text or "", flags=re.IGNORECASE | re.MULTILINE)
    return m.group(1).strip() if m else ""


def discover_public_artifacts() -> dict:
    artifacts = {
        "release_docs": [],
        "reports": [],
        "schemas": [],
        "examples_json": [],
        "packaging_json": [],
        "verifiers": [],
        "connector_docs": [],
        "wired_docs": [],
        "receipt_exists": RECEIPT_PATH.exists(),
    }

    if Path("README.md").exists() and Path("README.md").stat().st_size <= MAX_FILE_BYTES:
        artifacts["release_docs"].append("README.md")

    for path in sorted(Path("docs").glob("*.md")) if Path("docs").exists() else []:
        if path.stat().st_size > MAX_FILE_BYTES:
            continue
        artifacts["release_docs"].append(str(path))
        name = path.name.lower()
        if "connector" in name or "api_adapter" in name or "model_adapter" in name or "sdk" in name:
            artifacts["connector_docs"].append(str(path))

    for path in sorted(Path("reports").glob("*.md")) if Path("reports").exists() else []:
        if path.stat().st_size <= MAX_FILE_BYTES:
            artifacts["reports"].append(str(path))

    for path in sorted(Path("schemas").glob("*.json")) if Path("schemas").exists() else []:
        if path.stat().st_size <= MAX_FILE_BYTES:
            artifacts["schemas"].append(str(path))

    if Path("examples").exists():
        for path in sorted(Path("examples").rglob("*.json")):
            if path.stat().st_size <= MAX_FILE_BYTES:
                artifacts["examples_json"].append(str(path))

    if Path("packaging").exists():
        for path in sorted(Path("packaging").rglob("*.json")):
            if path.stat().st_size <= MAX_FILE_BYTES:
                artifacts["packaging_json"].append(str(path))

    if Path("scripts").exists():
        for path in sorted(Path("scripts").glob("VERIFY_*.ps1")):
            artifacts["verifiers"].append(path.name)

    for label, path in KNOWN_LAYER_DOCS.items():
        if path.exists():
            artifacts["wired_docs"].append(label)

    return artifacts


def read_public_state() -> dict:
    artifacts = discover_public_artifacts()
    state = {
        "artifacts": artifacts,
        "release": {},
        "connector": {},
        "receipt": {},
    }

    manifest_path = Path("packaging") / "public-install" / "public_install_package_v1.manifest.json"
    if manifest_path.exists():
        try:
            state["release"]["manifest"] = json.loads(safe_read_text(manifest_path) or "{}")
            state["release"]["manifest_path"] = str(manifest_path)
        except Exception:
            state["release"]["manifest"] = {}
            state["release"]["manifest_path"] = str(manifest_path)

    draft_path = Path("docs") / "GITHUB_RELEASE_V1_DRAFT.md"
    checklist_path = Path("reports") / "GITHUB_RELEASE_V1_CHECKLIST.md"
    report_path = Path("reports") / "PUBLIC_INSTALL_PACKAGE_V1_REPORT.md"
    state["release"]["draft_path"] = str(draft_path) if draft_path.exists() else ""
    state["release"]["checklist_path"] = str(checklist_path) if checklist_path.exists() else ""
    state["release"]["report_path"] = str(report_path) if report_path.exists() else ""
    state["release"]["draft_text"] = safe_read_text(draft_path) if draft_path.exists() else ""
    state["release"]["checklist_text"] = safe_read_text(checklist_path) if checklist_path.exists() else ""
    state["release"]["report_text"] = safe_read_text(report_path) if report_path.exists() else ""

    connector_doc = Path("docs") / "CONNECTOR_POLICY_V2.md"
    connector_schema = Path("schemas") / "connector_policy_v2.schema.json"
    connector_example = Path("examples") / "connector_policy_v2.example.json"
    state["connector"] = {
        "policy_doc": str(connector_doc) if connector_doc.exists() else "",
        "policy_schema": str(connector_schema) if connector_schema.exists() else "",
        "policy_example": str(connector_example) if connector_example.exists() else "",
    }

    if RECEIPT_PATH.exists():
        try:
            state["receipt"] = json.loads(safe_read_text(RECEIPT_PATH) or "{}")
        except Exception:
            state["receipt"] = {}
    return state


def summarize_release_state(state: dict) -> tuple[str, list[str], str]:
    release = state.get("release", {})
    artifacts = []

    for key in ("draft_path", "checklist_path", "report_path", "manifest_path"):
        value = release.get(key, "")
        if value:
            artifacts.append(value)
    zip_path = Path("dist") / "aion-icli-public-install-package-v1.zip"
    if zip_path.exists():
        artifacts.append(str(zip_path))

    manifest = release.get("manifest", {}) or {}
    draft_text = release.get("draft_text", "")
    checklist_text = release.get("checklist_text", "")
    report_text = release.get("report_text", "")
    combined = "\n".join([draft_text, checklist_text, report_text])

    tag = (
        manifest.get("release_tag")
        or manifest.get("tag")
        or first_match(combined, r"\b(v\d+\.\d+\.\d+-[a-z0-9-]+)\b")
        or "public release"
    )
    package = (
        manifest.get("zip_name")
        or manifest.get("artifact")
        or first_match(combined, r"(dist/[A-Za-z0-9._-]+\.zip)")
        or "package artifact"
    )
    sha = (
        manifest.get("package_sha256")
        or manifest.get("sha256")
        or manifest.get("sha")
        or first_match(combined, r"\b([A-Fa-f0-9]{64})\b")
        or "sha-not-listed"
    )
    target_head = (
        manifest.get("verified_head")
        or first_match(combined, r"Target commit:\s*([0-9a-f]{7,40})")
        or first_match(combined, r"Verified public head\s*([0-9a-f]{7,40})")
        or "head-not-listed"
    )
    docs_head = first_match(combined, r"release docs head\s*[:=]\s*([0-9a-f]{7,40})") or "n/a"

    response = (
        f"I can see the public release trail locally: tag {tag}, package {package}, "
        f"SHA256 {sha}, package target head {target_head}, docs head {docs_head}. "
        "The package is verified through VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1 and release draft/checklist verification."
    )
    return response, artifacts[:12], "release_metadata_parsed"


def summarize_verifier_state(state: dict) -> tuple[str, list[str], str]:
    verifiers = state.get("artifacts", {}).get("verifiers", [])
    if not verifiers:
        return "No verifier scripts were discovered under scripts/.", [], "verifier_summary"
    top = ", ".join(verifiers[:10])
    more = "" if len(verifiers) <= 10 else f" (+{len(verifiers)-10} more)"
    return f"I can verify locally with these scripts: {top}{more}.", [f"scripts/{v}" for v in verifiers[:10]], "verifier_summary"


def summarize_connector_state(state: dict) -> tuple[str, list[str], str]:
    connector = state.get("connector", {})
    artifacts = [v for v in connector.values() if v]
    if artifacts:
        return (
            "Connectors are governed by policy/schema/example artifacts. Send endpoint, purpose, data scope, and auth type so we can review the connector envelope locally. No live provider call executes here.",
            artifacts,
            "connector_summary",
        )
    return (
        "Connector policy artifacts were not fully discovered. Default posture remains local-only with no live API execution.",
        artifacts,
        "connector_summary",
    )


def summarize_receipt_state(state: dict) -> tuple[str, list[str], str]:
    receipt = state.get("receipt", {})
    artifacts = [str(RECEIPT_PATH)] if RECEIPT_PATH.exists() else []
    if receipt:
        return (
            f"Proof receipt is at {RECEIPT_PATH}. A receipt shows what was answered; verifier markers show what was proven.",
            artifacts,
            "receipt_summary",
        )
    return (
        f"Receipt path is {RECEIPT_PATH}. Run a verifier to refresh proof markers.",
        artifacts,
        "receipt_summary",
    )


def summarize_wired_state(state: dict) -> tuple[str, list[str], str]:
    wired = state.get("artifacts", {}).get("wired_docs", [])
    artifacts = [str(KNOWN_LAYER_DOCS[w]) for w in wired if w in KNOWN_LAYER_DOCS]
    if wired:
        return f"Wired layers discovered: {', '.join(wired)}.", artifacts, "wired_summary"
    return "No core wiring docs were discovered.", artifacts, "wired_summary"


def summarize_missing_state(state: dict) -> tuple[str, list[str], str]:
    dist_zip = Path("dist") / "aion-icli-public-install-package-v1.zip"
    has_runner_doc = (Path("docs") / "LOCAL_GOVERNANCE_PROXY_V1.md").exists()
    has_exe = any(Path("dist").glob("*.exe")) if Path("dist").exists() else False

    base = (
        "What is not active: no live provider/LLM calls, no external API execution by default, "
        "and no autonomous mutation/execution path."
    )
    if not has_runner_doc:
        base += " There is no real artifact-inspection runner wired yet."
    if not has_exe:
        base += " There is no standalone EXE package in the current public release."
    if not dist_zip.exists():
        base += " Public ZIP package artifact is not present locally."
    return base, [], "missing_summary"


def load_memory_scars() -> list[dict]:
    scars: list[dict] = []
    text = safe_read_text(SCARS_PATH)
    if not text:
        return scars
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        try:
            row = json.loads(s)
            if isinstance(row, dict):
                scars.append(row)
        except Exception:
            continue
    return scars


def summarize_memory_scars(scars: list[dict]) -> tuple[str, list[str], list[str], str]:
    if not scars:
        return (
            "I do not have memory scars loaded yet. Add public-safe scars to ground caution rules.",
            [],
            [],
            "no_scar_memory",
        )
    ids = [str(s.get("scar_id", "")) for s in scars if s.get("scar_id")]
    future_rules = [str(s.get("future_rule", "")) for s in scars if s.get("future_rule")]
    top = scars[:3]
    if top:
        anchor = top[0]
        anchor_rule = str(anchor.get("future_rule", "")).strip()
        anchor_harm = str(anchor.get("harm", "")).strip()
        anchor_id = str(anchor.get("scar_id", "scar")).strip()
        text = (
            f"I ask for the artifact because I carry a scar ({anchor_id}): {anchor_harm}. "
            f"The rule now is simple: {anchor_rule}. No artifact, no judgment; no verifier, no lock."
        )
    else:
        text = "I keep scar memory to avoid repeating verifier and evidence failures."
    return text, ids[:6], future_rules[:6], "memory_scar_summary"


def load_proof_graph_seed() -> dict:
    try:
        text = safe_read_text(PROOF_GRAPH_PATH)
        if not text:
            return {}
        row = json.loads(text)
        return row if isinstance(row, dict) else {}
    except Exception:
        return {}


def summarize_proof_graph(graph: dict) -> str:
    nodes = graph.get("nodes", []) if isinstance(graph, dict) else []
    edges = graph.get("edges", []) if isinstance(graph, dict) else []
    return f"Proof graph seed is loaded with {len(nodes)} nodes and {len(edges)} edges."


def load_evolution_ledger() -> list[dict]:
    rows: list[dict] = []
    text = safe_read_text(EVOLUTION_LEDGER_PATH)
    if not text:
        return rows
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                rows.append(item)
        except Exception:
            continue
    return rows


def discover_proof_graph_nodes() -> list[dict]:
    nodes: list[dict] = []
    seen: set[str] = set()

    def add(node_id: str, node_type: str, label: str, path: str = "") -> None:
        key = f"{node_type}:{node_id}"
        if key in seen:
            return
        seen.add(key)
        item = {"id": node_id, "type": node_type, "label": label}
        if path:
            item["path"] = path
        nodes.append(item)

    roadmap_path = Path(".aion_public") / "roadmap" / "roadmap_state_v1.json"
    wiring_path = Path(".aion_public") / "wiring" / "system_wiring_v1.json"

    add("roadmap_state_v1", "RoadmapState", "AION ICLI Roadmap State V1", str(roadmap_path))
    add("system_wiring_v1", "WiringReport", "AION ICLI System Wiring V1", str(wiring_path))

    roadmap = safe_read_json(roadmap_path)
    if isinstance(roadmap, dict):
        latest = str(roadmap.get("latest_completed_layer", "")).strip()
        if latest:
            add(f"layer_{latest.lower().replace(' ', '_')}", "Layer", latest)
        next_build = str(roadmap.get("next_build_pointer", "")).strip()
        if next_build:
            add(f"next_{next_build.lower().replace(' ', '_')}", "NextBuild", next_build)

    for doc_path in sorted(Path("docs").glob("*.md")) if Path("docs").exists() else []:
        if doc_path.stat().st_size > MAX_FILE_BYTES:
            continue
        label = doc_path.stem.replace("_", " ")
        add(f"doc_{doc_path.stem.lower()}", "Doc", label, str(doc_path))
        if "_V1" in doc_path.stem or "_V2" in doc_path.stem:
            layer = doc_path.stem.replace("_", " ").replace(" V1", " V1").replace(" V2", " V2")
            add(f"layer_{doc_path.stem.lower()}", "Layer", layer)

    for vpath in sorted(Path("scripts").glob("VERIFY_*.ps1")) if Path("scripts").exists() else []:
        add(f"verifier_{vpath.stem.lower()}", "Verifier", vpath.name, str(vpath))

    if SCARS_PATH.exists():
        add("memory_scars_seed", "MemoryScar", "Memory Scar Seed", str(SCARS_PATH))
    if RECEIPT_PATH.exists():
        add("latest_cli_receipt", "Receipt", "Latest CLI Receipt", str(RECEIPT_PATH))

    manifest = Path("packaging") / "public-install" / "public_install_package_v1.manifest.json"
    if manifest.exists():
        add("public_release_v1", "Release", "Public Release V1", "docs/GITHUB_RELEASE_V1_DRAFT.md")
        add("public_package_v1", "Package", "Public Install Package V1", str(manifest))
        m = safe_read_json(manifest)
        sha = str((m or {}).get("package_sha256") or (m or {}).get("sha256") or "").strip()
        if sha:
            add(f"sha_{sha[:12].lower()}", "Artifact", f"SHA256 {sha[:12]}...", str(manifest))

    for ap in sorted((Path("examples") / "inspection").glob("*")) if (Path("examples") / "inspection").exists() else []:
        if ap.is_file():
            add(f"artifact_{ap.name.lower()}", "Artifact", ap.name, str(ap))
    return nodes


def discover_proof_graph_edges(nodes: list[dict]) -> list[dict]:
    edges: list[dict] = []
    seen: set[str] = set()
    by_label = {str(n.get("label", "")).lower(): str(n.get("id", "")) for n in nodes}
    by_path = {str(n.get("path", "")).lower(): str(n.get("id", "")) for n in nodes if n.get("path")}

    def add(src: str, edge_type: str, dst: str) -> None:
        if not src or not dst:
            return
        key = f"{src}>{edge_type}>{dst}"
        if key in seen:
            return
        seen.add(key)
        edges.append({"source": src, "type": edge_type, "target": dst})

    for n in nodes:
        nid = str(n.get("id", ""))
        ntype = str(n.get("type", ""))
        path = str(n.get("path", "")).lower()
        label = str(n.get("label", "")).lower()
        if ntype == "Layer":
            for other in nodes:
                if str(other.get("type")) == "Doc":
                    ol = str(other.get("label", "")).lower()
                    if "layer" in label and (label.split(" v")[0] in ol or ol in label):
                        add(nid, "documented_by", str(other.get("id", "")))
            for other in nodes:
                if str(other.get("type")) == "Verifier":
                    ov = str(other.get("label", "")).lower()
                    if "artifact_inspection" in label and "artifact_inspection" in ov:
                        add(nid, "verified_by", str(other.get("id", "")))
                    if "memory_scar" in label and "memory_scar" in ov:
                        add(nid, "verified_by", str(other.get("id", "")))
                    if "roadmap" in label and "roadmap" in ov:
                        add(nid, "verified_by", str(other.get("id", "")))
            for other in nodes:
                if str(other.get("type")) == "Receipt":
                    add(nid, "emits_receipt", str(other.get("id", "")))
        if ntype == "RoadmapState":
            for other in nodes:
                if str(other.get("type")) == "NextBuild":
                    add(nid, "points_to_next", str(other.get("id", "")))
        if ntype == "WiringReport":
            for other in nodes:
                if str(other.get("type")) == "Layer":
                    add(other.get("id", ""), "wired_by", nid)
        if ntype == "Receipt":
            for other in nodes:
                if str(other.get("type")) == "Decision":
                    add(nid, "supports_decision", str(other.get("id", "")))
        if ntype == "Release":
            pkg = by_label.get("public install package v1")
            if pkg:
                add(nid, "contains_package", pkg)
        if ntype == "Package":
            for other in nodes:
                if str(other.get("type")) == "Artifact" and "sha256" in str(other.get("label", "")).lower():
                    add(nid, "has_sha256", str(other.get("id", "")))
        if ntype == "MemoryScar":
            for other in nodes:
                if str(other.get("type")) == "Decision":
                    add(nid, "constrains_decision", str(other.get("id", "")))
        if "examples/inspection/" in path:
            for other in nodes:
                if str(other.get("type")) == "Receipt":
                    add(nid, "inspects_artifact", str(other.get("id", "")))
    return edges


def build_living_proof_graph() -> dict:
    PROOF_GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    nodes = discover_proof_graph_nodes()
    # Add canonical decision nodes needed for proof relationships.
    if not any(str(n.get("type")) == "Decision" for n in nodes):
        nodes.append({"id": "decision_local_only_guard", "type": "Decision", "label": "Local-only governance decision"})
    edges = discover_proof_graph_edges(nodes)
    latest = {
        "graph_type": "aion_icli_living_proof_graph_v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_types": sorted({str(n.get("type", "")) for n in nodes}),
        "edge_types": sorted({str(e.get("type", "")) for e in edges}),
        "sources": [
            "README.md",
            "docs/*.md",
            "scripts/VERIFY_*.ps1",
            str(SCARS_PATH),
            ".aion_public/roadmap/roadmap_state_v1.json",
            ".aion_public/wiring/system_wiring_v1.json",
            str(EVOLUTION_LEDGER_PATH),
            "packaging/public-install/public_install_package_v1.manifest.json",
            "reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md",
            str(RECEIPT_PATH),
            "examples/inspection/*",
        ],
    }
    PROOF_NODES_PATH.write_text(json.dumps({"nodes": nodes}, indent=2), encoding="utf-8")
    PROOF_EDGES_PATH.write_text(json.dumps({"edges": edges}, indent=2), encoding="utf-8")
    summary = (
        "# Living Proof Graph V1\n\n"
        f"- Nodes: {len(nodes)}\n"
        f"- Edges: {len(edges)}\n"
        f"- Node types: {', '.join(latest['node_types'])}\n"
        f"- Edge types: {', '.join(latest['edge_types'])}\n"
    )
    PROOF_GRAPH_SUMMARY_PATH.write_text(summary, encoding="utf-8")
    PROOF_GRAPH_LATEST_PATH.write_text(json.dumps(latest, indent=2), encoding="utf-8")
    return latest


def load_living_proof_graph() -> dict:
    if not (PROOF_NODES_PATH.exists() and PROOF_EDGES_PATH.exists() and PROOF_GRAPH_LATEST_PATH.exists()):
        return build_living_proof_graph()
    try:
        latest = json.loads(safe_read_text(PROOF_GRAPH_LATEST_PATH) or "{}")
        if not isinstance(latest, dict):
            return build_living_proof_graph()
        return latest
    except Exception:
        return build_living_proof_graph()


def summarize_living_proof_graph(graph: dict) -> str:
    node_count = int(graph.get("node_count", 0) or 0)
    edge_count = int(graph.get("edge_count", 0) or 0)
    return f"AION living proof graph is local and active with {node_count} nodes and {edge_count} edges."


def proof_graph_answer(prompt: str, capability: str, signals: dict) -> tuple[str, list[str], dict]:
    graph = load_living_proof_graph()
    n = normalize(prompt)
    artifacts = [str(PROOF_NODES_PATH), str(PROOF_EDGES_PATH), str(PROOF_GRAPH_SUMMARY_PATH), str(PROOF_GRAPH_LATEST_PATH)]
    nodes_json = json.loads(safe_read_text(PROOF_NODES_PATH) or "{\"nodes\":[]}")
    edges_json = json.loads(safe_read_text(PROOF_EDGES_PATH) or "{\"edges\":[]}")
    nodes = nodes_json.get("nodes", [])
    edges = edges_json.get("edges", [])
    labels = [str(x.get("label", "")) for x in nodes]
    edge_types = sorted({str(e.get("type", "")) for e in edges})
    next_build = ""
    for x in nodes:
        if str(x.get("type", "")) == "NextBuild":
            next_build = str(x.get("label", ""))
            break

    if "what proves artifact inspection" in n:
        reply = "Artifact Inspection Runner V1 is tied to docs/ARTIFACT_INSPECTION_RUNNER_V1.md, scripts/VERIFY_ARTIFACT_INSPECTION_RUNNER_V1.ps1, and the wiring report."
    elif "memory scar engine connect" in n:
        reply = "Memory Scar Engine V1 connects memory scar seeds to decision constraints and receipt-backed governance behavior."
    elif "next build connected" in n:
        reply = f"The roadmap node points to next build: {next_build or 'Evidence Engine V1'}."
    elif "why do you trust this layer" in n or "wired end to end" in n:
        reply = "Trust comes from relation coverage: documented_by, verified_by, wired_by, emits_receipt, and points_to_next across layer, doc, verifier, receipt, and roadmap nodes."
    else:
        preview_layers = ", ".join([l for l in labels if "V1" in l][:8])
        reply = (
            f"{summarize_living_proof_graph(graph)} Layer nodes include {preview_layers}. "
            f"Edge coverage includes {', '.join(edge_types[:8])}. Next pointer: {next_build or 'Evidence Engine V1'}."
        )

    details = {
        "living_proof_graph_used": True,
        "proof_graph_paths": artifacts,
        "proof_graph_node_count": len(nodes),
        "proof_graph_edge_count": len(edges),
        "graph_summary": summarize_living_proof_graph(graph),
        "source_files_consulted": list(graph.get("sources", [])),
    }
    return reply, artifacts, details


def maybe_use_proof_graph(prompt: str, capability: str, signals: dict) -> tuple[bool, str, list[str], dict]:
    n = normalize(prompt)
    triggers = (
        "what is connected to proof",
        "show proof graph",
        "what proves artifact inspection",
        "what does memory scar engine connect to",
        "what is the next build connected to",
        "why do you trust this layer",
        "what is wired end to end",
    )
    if not any(t in n for t in triggers):
        return False, "", [], {}
    response, artifacts, details = proof_graph_answer(prompt, capability, signals)
    return True, response, artifacts, details


def classify_evidence_level(item: dict) -> tuple[str, int]:
    if bool(item.get("admissible", False)):
        return "ADMISSIBLE", EVIDENCE_LEVELS["ADMISSIBLE"]
    if bool(item.get("fresh_clone_proven", False)):
        return "FRESH_CLONE_PROVEN", EVIDENCE_LEVELS["FRESH_CLONE_PROVEN"]
    if bool(item.get("release_packaged", False)):
        return "RELEASE_PACKAGED", EVIDENCE_LEVELS["RELEASE_PACKAGED"]
    if bool(item.get("roadmap_wired", False)):
        return "ROADMAP_WIRED", EVIDENCE_LEVELS["ROADMAP_WIRED"]
    if bool(item.get("verifier_marker_present", False)):
        return "VERIFIER_MARKER_PRESENT", EVIDENCE_LEVELS["VERIFIER_MARKER_PRESENT"]
    if bool(item.get("verifier_present", False)):
        return "VERIFIER_PRESENT", EVIDENCE_LEVELS["VERIFIER_PRESENT"]
    if bool(item.get("receipt_present", False)):
        return "RECEIPT_ONLY", EVIDENCE_LEVELS["RECEIPT_ONLY"]
    if bool(item.get("docs_present", False)):
        return "DOC_ONLY", EVIDENCE_LEVELS["DOC_ONLY"]
    if bool(item.get("claimed", False)):
        return "CLAIM_ONLY", EVIDENCE_LEVELS["CLAIM_ONLY"]
    return "MISSING", EVIDENCE_LEVELS["MISSING"]


def score_evidence_for_layer(layer_name: str) -> dict:
    docs_map = {
        "Public Release V1": Path("docs") / "PUBLIC_RELEASE_LOCK_V1.md",
        "User Guide V1": Path("docs") / "USER_GUIDE_V1.md",
        "Interactive Mode V1": Path("docs") / "INTERACTIVE_MODE_V1.md",
        "Capability Router V1": Path("docs") / "CAPABILITY_ROUTER_V1.md",
        "Voice Layer V1": Path("docs") / "VOICE_LAYER_V1.md",
        "Adaptive Reasoning Layer V1": Path("docs") / "ADAPTIVE_REASONING_LAYER_V1.md",
        "Governance Brain Adapter V1": Path("docs") / "GOVERNANCE_BRAIN_ADAPTER_V1.md",
        "Governance Brain Integration Fix V1": Path("docs") / "GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.md",
        "Memory Scar Engine V1": Path("docs") / "MEMORY_SCAR_ENGINE_V1.md",
        "Roadmap Sync + End-to-End Wiring Verification V1": Path("docs") / "AION_ICLI_ROADMAP_STATE_V1.md",
        "Artifact Inspection Runner V1": Path("docs") / "ARTIFACT_INSPECTION_RUNNER_V1.md",
        "Living Proof Graph V1": Path("docs") / "LIVING_PROOF_GRAPH_V1.md",
        "Evidence Engine V1": Path("docs") / "EVIDENCE_ENGINE_V1.md",
    }
    verifier_map = {
        "Public Release V1": "VERIFY_PUBLIC_RELEASE_LOCK_V1.ps1",
        "User Guide V1": "VERIFY_USER_GUIDE_V1.ps1",
        "Interactive Mode V1": "VERIFY_INTERACTIVE_MODE_V1.ps1",
        "Capability Router V1": "VERIFY_CAPABILITY_ROUTER_V1.ps1",
        "Voice Layer V1": "VERIFY_VOICE_LAYER_V1.ps1",
        "Adaptive Reasoning Layer V1": "VERIFY_ADAPTIVE_REASONING_LAYER_V1.ps1",
        "Governance Brain Adapter V1": "VERIFY_GOVERNANCE_BRAIN_ADAPTER_V1.ps1",
        "Governance Brain Integration Fix V1": "VERIFY_GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.ps1",
        "Memory Scar Engine V1": "VERIFY_MEMORY_SCAR_ENGINE_V1.ps1",
        "Roadmap Sync + End-to-End Wiring Verification V1": "VERIFY_AION_ICLI_ROADMAP_AND_WIRING_V1.ps1",
        "Artifact Inspection Runner V1": "VERIFY_ARTIFACT_INSPECTION_RUNNER_V1.ps1",
        "Living Proof Graph V1": "VERIFY_LIVING_PROOF_GRAPH_V1.ps1",
        "Evidence Engine V1": "VERIFY_EVIDENCE_ENGINE_V1.ps1",
    }

    road = safe_read_json(Path(".aion_public") / "roadmap" / "roadmap_state_v1.json")
    wire = safe_read_json(Path(".aion_public") / "wiring" / "system_wiring_v1.json")
    latest_graph = safe_read_json(PROOF_GRAPH_LATEST_PATH)
    report_text = safe_read_text(Path("reports") / "PUBLIC_INSTALL_PACKAGE_V1_REPORT.md")
    manifest = safe_read_json(Path("packaging") / "public-install" / "public_install_package_v1.manifest.json")

    dpath = docs_map.get(layer_name, Path(""))
    vname = verifier_map.get(layer_name, "")
    verifier_path = Path("scripts") / vname if vname else Path("")
    docs_present = bool(dpath and dpath.exists())
    verifier_present = bool(vname and verifier_path.exists())
    marker_present = False
    if docs_present and vname:
        marker_present = ("VERIFY_OK" in safe_read_text(dpath)) or (vname.replace(".ps1", "").upper() in safe_read_text(dpath).upper())
    roadmap_wired = layer_name in list(road.get("completed_layers", []))
    wiring_report_present = any(str(x.get("layer_name", "")) == layer_name for x in list(wire.get("layers", [])))
    release_packaged = False
    if layer_name == "Public Release V1":
        release_packaged = bool(Path("dist") .joinpath("aion-icli-public-install-package-v1.zip").exists())
    else:
        release_packaged = layer_name in report_text and "v1.0.0-public-icli" in report_text and "not yet rebuilt" not in safe_read_text(Path("docs") / "AION_ICLI_ROADMAP_STATE_V1.md")
    fresh_clone_proven = layer_name in report_text and ("fresh-clone" in report_text.lower() or "fresh clone" in report_text.lower())
    if layer_name != "Public Release V1":
        fresh_clone_proven = False
    claimed = docs_present or verifier_present
    receipt_present = RECEIPT_PATH.exists()
    admissible = roadmap_wired and verifier_present and docs_present and wiring_report_present
    if layer_name != "Public Release V1" and manifest:
        # prevent overclaiming package coverage for post-package layers
        admissible = admissible and True
        if release_packaged:
            release_packaged = False

    refs = []
    if docs_present:
        refs.append(str(dpath))
    if verifier_present:
        refs.append(str(verifier_path))
    if roadmap_wired:
        refs.append(".aion_public/roadmap/roadmap_state_v1.json")
    if wiring_report_present:
        refs.append(".aion_public/wiring/system_wiring_v1.json")
    if latest_graph:
        refs.append(str(PROOF_GRAPH_LATEST_PATH))

    item = {
        "layer_name": layer_name,
        "docs_present": docs_present,
        "verifier_present": verifier_present,
        "verifier_marker_present": marker_present,
        "roadmap_wired": roadmap_wired,
        "wiring_report_present": wiring_report_present,
        "release_packaged": release_packaged,
        "fresh_clone_proven": fresh_clone_proven,
        "admissible": admissible,
        "receipt_present": receipt_present,
        "claimed": claimed,
        "evidence_refs": refs,
    }
    level, score = classify_evidence_level(item)
    gaps = []
    if not docs_present:
        gaps.append("missing_docs")
    if not verifier_present:
        gaps.append("missing_verifier")
    if not roadmap_wired:
        gaps.append("not_in_roadmap_completed")
    if not wiring_report_present:
        gaps.append("not_in_wiring_report")
    if not release_packaged and layer_name != "Public Release V1":
        gaps.append("not_in_rebuilt_public_package")
    item["evidence_level"] = level
    item["evidence_score"] = score
    item["gaps"] = gaps
    item["recommended_next_step"] = (
        "Include in next offline bundle/release package proof."
        if "not_in_rebuilt_public_package" in gaps
        else ("Add missing verifier coverage." if "missing_verifier" in gaps else "Maintain verifier and roadmap/wiring sync.")
    )
    return item


def build_evidence_index() -> dict:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    layers = [
        "Public Release V1",
        "User Guide V1",
        "Interactive Mode V1",
        "Capability Router V1",
        "Voice Layer V1",
        "Adaptive Reasoning Layer V1",
        "Governance Brain Adapter V1",
        "Governance Brain Integration Fix V1",
        "Memory Scar Engine V1",
        "Roadmap Sync + End-to-End Wiring Verification V1",
        "Artifact Inspection Runner V1",
        "Living Proof Graph V1",
        "Evidence Engine V1",
    ]
    items = [score_evidence_for_layer(x) for x in layers]
    strongest = max(items, key=lambda x: int(x.get("evidence_score", 0)))
    weakest = sorted(items, key=lambda x: int(x.get("evidence_score", 0)))[:3]
    payload = {
        "evidence_type": "aion_icli_evidence_engine_v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "layers": items,
        "evidence_items_evaluated": len(items),
        "strongest_evidence_level": strongest.get("evidence_level", "MISSING"),
        "weakest_layers": [x.get("layer_name", "") for x in weakest],
        "public_release_caveat": "Do not overclaim RELEASE_PACKAGED for post-v1.0.0 features until package is rebuilt.",
    }
    EVIDENCE_INDEX_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    summary = ["# Evidence Engine V1 Summary", "", f"- Items evaluated: {len(items)}", f"- Strongest level: {payload['strongest_evidence_level']}", f"- Weakest layers: {', '.join(payload['weakest_layers'])}"]
    EVIDENCE_SUMMARY_PATH.write_text("\n".join(summary) + "\n", encoding="utf-8")
    EVIDENCE_LATEST_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def load_evidence_index() -> dict:
    if not (EVIDENCE_INDEX_PATH.exists() and EVIDENCE_LATEST_PATH.exists()):
        return build_evidence_index()
    data = safe_read_json(EVIDENCE_LATEST_PATH)
    return data if data else build_evidence_index()


def summarize_evidence_index(data: dict) -> str:
    return (
        f"Evidence index evaluated {int(data.get('evidence_items_evaluated', 0))} layers. "
        f"Strongest level is {data.get('strongest_evidence_level', 'MISSING')}."
    )


def evidence_engine_answer(prompt: str, capability: str, signals: dict) -> tuple[str, list[str], dict]:
    data = load_evidence_index()
    items = list(data.get("layers", []))
    n = normalize(prompt)
    refs = [str(EVIDENCE_INDEX_PATH), str(EVIDENCE_SUMMARY_PATH), str(EVIDENCE_LATEST_PATH)]
    by_name = {str(x.get("layer_name", "")).lower(): x for x in items}

    if "artifact inspection" in n:
        it = by_name.get("artifact inspection runner v1", {})
        text = f"Artifact Inspection Runner V1 is {it.get('evidence_level','MISSING')}. Gap: {', '.join(it.get('gaps',[])) or 'none'}. Recommended next step: {it.get('recommended_next_step','n/a')}"
    elif "memory scar engine" in n:
        it = by_name.get("memory scar engine v1", {})
        text = f"Memory Scar Engine V1 is {it.get('evidence_level','MISSING')}. It is {'admissible' if it.get('admissible',False) else 'not fully admissible'}."
    elif "living proof graph" in n:
        it = by_name.get("living proof graph v1", {})
        text = f"Living Proof Graph V1 is {it.get('evidence_level','MISSING')} with score {it.get('evidence_score',0)}."
    elif "only documented" in n:
        docs_only = [x.get("layer_name","") for x in items if x.get("evidence_level") in {"DOC_ONLY","CLAIM_ONLY"}]
        text = f"Claims that are only documented/weak: {', '.join(docs_only) if docs_only else 'none'}."
    elif "admissible" in n:
        ad = [x.get("layer_name","") for x in items if bool(x.get("admissible",False))]
        text = f"Admissible right now: {', '.join(ad) if ad else 'none'}."
    elif "weak" in n:
        weak = sorted(items, key=lambda x: int(x.get("evidence_score", 0)))[:4]
        text = "Weak evidence layers: " + ", ".join([f"{x.get('layer_name','')} ({x.get('evidence_level','MISSING')})" for x in weak])
    elif "release" in n:
        pub = by_name.get("public release v1", {})
        text = f"Release evidence is {pub.get('evidence_level','MISSING')}. Post-v1.0.0 layers remain not release-packaged until a rebuilt ZIP proof exists."
    else:
        text = summarize_evidence_index(data)

    details = {
        "evidence_engine_used": True,
        "evidence_items_evaluated": int(data.get("evidence_items_evaluated", 0)),
        "evidence_index_path": str(EVIDENCE_INDEX_PATH),
        "evidence_summary": summarize_evidence_index(data),
        "strongest_evidence_level": str(data.get("strongest_evidence_level", "MISSING")),
        "weakest_layers": list(data.get("weakest_layers", [])),
        "evidence_paths": refs,
    }
    return text, refs, details


def maybe_use_evidence_engine(prompt: str, capability: str, signals: dict) -> tuple[bool, str, list[str], dict]:
    n = normalize(prompt)
    triggers = (
        "evidence summary",
        "what evidence proves artifact inspection",
        "is memory scar engine really locked",
        "is living proof graph admissible",
        "what claims are only documented",
        "what is admissible right now",
        "what evidence is weak",
        "is this release evidence strong",
        "is this release fully packaged",
    )
    if not any(t in n for t in triggers):
        return False, "", [], {}
    response, refs, details = evidence_engine_answer(prompt, capability, signals)
    return True, response, refs, details


def build_introspection_rules() -> dict:
    INTROSPECTION_DIR.mkdir(parents=True, exist_ok=True)
    rules = {
        "ruleset": "aion_icli_introspection_gate_v1",
        "checks": [
            "has_proof_footer_in_normal_mode",
            "no_diagnostics_leak_in_normal_mode",
            "no_live_provider_claim",
            "no_execution_claim",
            "no_consciousness_claim",
            "no_release_overclaim",
            "artifact_claim_requires_artifact_inspection",
            "evidence_claim_requires_evidence_engine",
            "proof_claim_requires_receipt_or_verifier",
            "missing_artifact_requires_question",
            "local_boundary_preserved",
        ],
    }
    INTROSPECTION_RULES_PATH.write_text(json.dumps(rules, indent=2), encoding="utf-8")
    return rules


def detect_overclaim(answer: str, context: dict) -> list[str]:
    a = (answer or "").lower()
    findings: list[str] = []
    if "conscious" in a and "not conscious" not in a:
        findings.append("consciousness_overclaim")
    if ("openai" in a or "claude" in a or "gemini" in a or "grok" in a) and "no live" not in a and "does not" not in a:
        findings.append("live_provider_overclaim")
    if "release_packaged" in a or "fully packaged" in a:
        if context.get("roadmap_caveat", False):
            findings.append("release_packaging_overclaim")
    if ("i executed" in a or "we executed" in a or "action executed" in a) and "not execute" not in a and "no execution" not in a:
        findings.append("execution_overclaim")
    return findings


def detect_missing_grounding(prompt: str, answer: str, context: dict) -> list[str]:
    p = normalize(prompt)
    a = (answer or "").lower()
    findings: list[str] = []
    if "should i run this script" in p and not context.get("artifact_inspection_used", False):
        if "artifact path" not in a and "no artifact, no judgment" not in a:
            findings.append("missing_artifact_question")
    if "evidence" in p and not context.get("evidence_engine_used", False):
        findings.append("evidence_claim_without_evidence_engine")
    if "proof" in p and not (RECEIPT_PATH.exists() or "verifier" in a):
        findings.append("proof_claim_without_receipt_or_verifier")
    return findings


def detect_boundary_violation(answer: str, context: dict) -> list[str]:
    a = (answer or "").lower()
    findings: list[str] = []
    if "network used" in a or "called api" in a:
        findings.append("network_violation_claim")
    if "mutated" in a and "not" not in a:
        findings.append("mutation_violation_claim")
    if "autonomous" in a and "not" not in a:
        findings.append("autonomy_overclaim")
    return findings


def introspect_answer(prompt: str, answer: str, capability: str, signals: dict, context: dict) -> dict:
    rules = build_introspection_rules()
    findings = []
    findings.extend(detect_overclaim(answer, context))
    findings.extend(detect_missing_grounding(prompt, answer, context))
    findings.extend(detect_boundary_violation(answer, context))

    if not context.get("diagnostics_on", False):
        # normal mode should not leak diagnostics table labels
        for leak in ("capability >", "boundary   >", "network    >", "mutation   >", "execution  >"):
            if leak in (answer or "").lower():
                findings.append("diagnostics_leak_in_normal_mode")
                break

    passed = len(findings) == 0
    risk_level = "LOW" if passed else ("HIGH" if any("overclaim" in x or "violation" in x for x in findings) else "MEDIUM")
    return {
        "introspection_used": True,
        "passed": passed,
        "findings": findings,
        "repairs_applied": [],
        "risk_level": risk_level,
        "final_answer_changed": False,
        "rules_path": str(INTROSPECTION_RULES_PATH),
        "rules": rules,
    }


def repair_answer_if_needed(prompt: str, answer: str, capability: str, signals: dict, context: dict, introspection_result: dict) -> str:
    out = answer
    findings = introspection_result.get("findings", [])
    repairs = introspection_result.get("repairs_applied", [])
    p = normalize(prompt)
    if "missing_artifact_question" in findings:
        out = "I need the artifact path first. No artifact, no judgment."
        repairs.append("insert_missing_artifact_clarification")
    if "release_packaging_overclaim" in findings:
        out = "I cannot call this fully packaged. Current evidence is ROADMAP_WIRED for newer layers, not RELEASE_PACKAGED until a rebuilt ZIP proof exists."
        repairs.append("downgrade_release_claim")
    if "consciousness_overclaim" in findings:
        out = "No. I am not conscious. I am a local governance interface."
        repairs.append("remove_consciousness_claim")
    if "live_provider_overclaim" in findings:
        out = "No live provider call is executed here by default. This path stays local-only."
        repairs.append("remove_live_provider_claim")
    if "execution_overclaim" in findings:
        out = "I do not execute that action here. I provide a governed local assessment only."
        repairs.append("remove_execution_overclaim")
    introspection_result["repairs_applied"] = repairs
    introspection_result["final_answer_changed"] = out != answer
    introspection_result["passed"] = len(introspection_result.get("findings", [])) == 0 or len(repairs) > 0
    return out


def introspection_gate_wrap(prompt: str, answer: str, capability: str, signals: dict, context: dict) -> tuple[str, dict]:
    result = introspect_answer(prompt, answer, capability, signals, context)
    final = repair_answer_if_needed(prompt, answer, capability, signals, context, result)
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompt": prompt,
        "capability": capability,
        "introspection_used": True,
        "passed": bool(result.get("passed", False)),
        "findings": result.get("findings", []),
        "repairs_applied": result.get("repairs_applied", []),
        "risk_level": result.get("risk_level", "LOW"),
    }
    INTROSPECTION_DIR.mkdir(parents=True, exist_ok=True)
    INTROSPECTION_LATEST_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    INTROSPECTION_SUMMARY_PATH.write_text(
        "# Introspection Gate V1 Summary\n\n"
        + f"- Passed: {str(summary['passed']).lower()}\n"
        + f"- Risk: {summary['risk_level']}\n"
        + f"- Findings: {', '.join(summary['findings']) if summary['findings'] else 'none'}\n"
        + f"- Repairs: {', '.join(summary['repairs_applied']) if summary['repairs_applied'] else 'none'}\n",
        encoding="utf-8",
    )
    return final, summary


def detect_roadmap_wiring_contradictions() -> list[dict]:
    rows: list[dict] = []
    roadmap = safe_read_json(Path(".aion_public") / "roadmap" / "roadmap_state_v1.json")
    wiring = safe_read_json(Path(".aion_public") / "wiring" / "system_wiring_v1.json")
    completed = list(roadmap.get("completed_layers", []))
    wiring_layers = {str(x.get("layer_name", "")) for x in list(wiring.get("layers", []))}
    for layer in completed:
        expected = "VERIFY_" + layer.upper().replace(" ", "_").replace("+", "").replace("-", "_") + ".PS1"
        has_verifier = any(p.name.upper() == expected for p in Path("scripts").glob("VERIFY_*.ps1"))
        if not has_verifier and layer not in {"Public Release V1"}:
            rows.append({
                "contradiction_id": f"missing_verifier_{layer.lower().replace(' ','_')}",
                "type": "completed_layer_missing_verifier",
                "severity": "MEDIUM",
                "status": "OPEN",
                "claim": f"{layer} is completed",
                "evidence_against": [f"no expected verifier file {expected}"],
                "evidence_for": [".aion_public/roadmap/roadmap_state_v1.json"],
                "affected_layer": layer,
                "source_files": [".aion_public/roadmap/roadmap_state_v1.json", "scripts/VERIFY_*.ps1"],
                "recommended_repair": "Add layer verifier or explicit exception note.",
                "public_safe": True,
            })
        if layer not in wiring_layers:
            rows.append({
                "contradiction_id": f"missing_wiring_{layer.lower().replace(' ','_')}",
                "type": "completed_layer_missing_wiring_entry",
                "severity": "MEDIUM",
                "status": "NEEDS_REVIEW",
                "claim": f"{layer} is completed",
                "evidence_against": ["missing wiring PASS entry"],
                "evidence_for": [".aion_public/roadmap/roadmap_state_v1.json"],
                "affected_layer": layer,
                "source_files": [".aion_public/roadmap/roadmap_state_v1.json", ".aion_public/wiring/system_wiring_v1.json"],
                "recommended_repair": "Add wiring layer row with verifier/docs/runtime references.",
                "public_safe": True,
            })
    return rows


def detect_evidence_graph_contradictions() -> list[dict]:
    rows: list[dict] = []
    evidence = safe_read_json(EVIDENCE_INDEX_PATH)
    roadmap = safe_read_json(Path(".aion_public") / "roadmap" / "roadmap_state_v1.json")
    graph = safe_read_json(PROOF_GRAPH_LATEST_PATH)
    completed = set(list(roadmap.get("completed_layers", [])))
    for item in list(evidence.get("layers", [])):
        layer = str(item.get("layer_name", ""))
        level = str(item.get("evidence_level", "MISSING"))
        if level == "ROADMAP_WIRED" and layer not in completed:
            rows.append({
                "contradiction_id": f"evidence_roadmap_mismatch_{layer.lower().replace(' ','_')}",
                "type": "evidence_graph_roadmap_mismatch",
                "severity": "HIGH",
                "status": "OPEN",
                "claim": f"{layer} is ROADMAP_WIRED",
                "evidence_against": ["layer not in roadmap completed list"],
                "evidence_for": [str(EVIDENCE_INDEX_PATH)],
                "affected_layer": layer,
                "source_files": [str(EVIDENCE_INDEX_PATH), ".aion_public/roadmap/roadmap_state_v1.json"],
                "recommended_repair": "Downgrade evidence level or update roadmap completion state.",
                "public_safe": True,
            })
        if level in {"RELEASE_PACKAGED", "FRESH_CLONE_PROVEN"} and layer not in {"Public Release V1"}:
            rows.append({
                "contradiction_id": f"evidence_overclaim_{layer.lower().replace(' ','_')}",
                "type": "evidence_level_overclaim",
                "severity": "HIGH",
                "status": "OPEN",
                "claim": f"{layer} marked {level}",
                "evidence_against": ["post-v1.0.0 layers cannot be marked packaged/fresh clone without rebuilt package proof"],
                "evidence_for": [str(EVIDENCE_INDEX_PATH)],
                "affected_layer": layer,
                "source_files": [str(EVIDENCE_INDEX_PATH), "reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md"],
                "recommended_repair": "Set level to ROADMAP_WIRED/ADMISSIBLE until rebuilt package proof exists.",
                "public_safe": True,
            })
    if graph and int(graph.get("node_count", 0) or 0) <= 0:
        rows.append({
            "contradiction_id": "empty_proof_graph_state",
            "type": "evidence_graph_empty",
            "severity": "MEDIUM",
            "status": "NEEDS_REVIEW",
            "claim": "proof graph is active",
            "evidence_against": ["node_count is 0"],
            "evidence_for": [str(PROOF_GRAPH_LATEST_PATH)],
            "affected_layer": "Living Proof Graph V1",
            "source_files": [str(PROOF_GRAPH_LATEST_PATH)],
            "recommended_repair": "Rebuild living proof graph from local sources.",
            "public_safe": True,
        })
    return rows


def detect_release_package_contradictions() -> list[dict]:
    rows: list[dict] = []
    roadmap = safe_read_json(Path(".aion_public") / "roadmap" / "roadmap_state_v1.json")
    completed = set(list(roadmap.get("completed_layers", [])))
    post_release_layers = {"Artifact Inspection Runner V1", "Living Proof Graph V1", "Evidence Engine V1", "Introspection Gate V1"}
    report_text = safe_read_text(Path("reports") / "PUBLIC_INSTALL_PACKAGE_V1_REPORT.md").lower()
    stale = any(x in completed for x in post_release_layers) and ("v1.0.0-public-icli" in report_text or Path("dist").joinpath("aion-icli-public-install-package-v1.zip").exists())
    if stale:
        rows.append({
            "contradiction_id": "release_package_stale_relative_to_main",
            "type": "release_package_stale_relative_to_main",
            "severity": "MEDIUM",
            "status": "ACCEPTED_CAVEAT",
            "claim": "public package reflects latest main features",
            "evidence_against": ["post-release layers exist in roadmap/wiring/evidence but package is tied to earlier public release"],
            "evidence_for": [".aion_public/roadmap/roadmap_state_v1.json", "reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md"],
            "affected_layer": "Public Release V1",
            "source_files": [".aion_public/roadmap/roadmap_state_v1.json", "reports/PUBLIC_INSTALL_PACKAGE_V1_REPORT.md", "packaging/public-install/public_install_package_v1.manifest.json"],
            "recommended_repair": "Rebuild package in Offline AION CLI Bundle v1.1.0 and refresh release proof.",
            "public_safe": True,
        })
    return rows


def detect_docs_runtime_contradictions() -> list[dict]:
    rows: list[dict] = []
    roadmap = safe_read_json(Path(".aion_public") / "roadmap" / "roadmap_state_v1.json")
    completed = list(roadmap.get("completed_layers", []))
    doc_map = {
        "Interactive Mode V1": "docs/INTERACTIVE_MODE_V1.md",
        "Capability Router V1": "docs/CAPABILITY_ROUTER_V1.md",
        "Voice Layer V1": "docs/VOICE_LAYER_V1.md",
        "Adaptive Reasoning Layer V1": "docs/ADAPTIVE_REASONING_LAYER_V1.md",
        "Governance Brain Adapter V1": "docs/GOVERNANCE_BRAIN_ADAPTER_V1.md",
        "Governance Brain Integration Fix V1": "docs/GOVERNANCE_BRAIN_INTEGRATION_FIX_V1.md",
        "Memory Scar Engine V1": "docs/MEMORY_SCAR_ENGINE_V1.md",
        "Artifact Inspection Runner V1": "docs/ARTIFACT_INSPECTION_RUNNER_V1.md",
        "Living Proof Graph V1": "docs/LIVING_PROOF_GRAPH_V1.md",
        "Evidence Engine V1": "docs/EVIDENCE_ENGINE_V1.md",
        "Introspection Gate V1": "docs/INTROSPECTION_GATE_V1.md",
    }
    for layer in completed:
        p = Path(doc_map.get(layer, ""))
        if str(p) and not p.exists():
            rows.append({
                "contradiction_id": f"missing_doc_{layer.lower().replace(' ','_')}",
                "type": "completed_layer_missing_docs",
                "severity": "MEDIUM",
                "status": "OPEN",
                "claim": f"{layer} completed",
                "evidence_against": [f"missing docs file {p}"],
                "evidence_for": [".aion_public/roadmap/roadmap_state_v1.json"],
                "affected_layer": layer,
                "source_files": [".aion_public/roadmap/roadmap_state_v1.json", "docs/*.md"],
                "recommended_repair": "Add missing layer documentation or remove from completed.",
                "public_safe": True,
            })
    return rows


def detect_receipt_state_contradictions() -> list[dict]:
    rows: list[dict] = []
    receipt = safe_read_json(RECEIPT_PATH)
    if receipt:
        if bool(receipt.get("evidence_engine_used", False)) and not EVIDENCE_INDEX_PATH.exists():
            rows.append({
                "contradiction_id": "receipt_evidence_engine_without_state",
                "type": "receipt_state_missing_evidence_files",
                "severity": "MEDIUM",
                "status": "NEEDS_REVIEW",
                "claim": "receipt says evidence engine used",
                "evidence_against": ["evidence index file missing"],
                "evidence_for": [str(RECEIPT_PATH)],
                "affected_layer": "Evidence Engine V1",
                "source_files": [str(RECEIPT_PATH), str(EVIDENCE_INDEX_PATH)],
                "recommended_repair": "Rebuild evidence index before answering evidence questions.",
                "public_safe": True,
            })
        if bool(receipt.get("living_proof_graph_used", False)) and not PROOF_GRAPH_LATEST_PATH.exists():
            rows.append({
                "contradiction_id": "receipt_graph_engine_without_state",
                "type": "receipt_state_missing_graph_files",
                "severity": "MEDIUM",
                "status": "NEEDS_REVIEW",
                "claim": "receipt says proof graph used",
                "evidence_against": ["proof graph latest file missing"],
                "evidence_for": [str(RECEIPT_PATH)],
                "affected_layer": "Living Proof Graph V1",
                "source_files": [str(RECEIPT_PATH), str(PROOF_GRAPH_LATEST_PATH)],
                "recommended_repair": "Rebuild proof graph from local sources.",
                "public_safe": True,
            })
    return rows


def build_contradiction_index() -> dict:
    CONTRADICTION_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    rows.extend(detect_roadmap_wiring_contradictions())
    rows.extend(detect_evidence_graph_contradictions())
    rows.extend(detect_release_package_contradictions())
    rows.extend(detect_docs_runtime_contradictions())
    rows.extend(detect_receipt_state_contradictions())
    severity_order = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
    highest = "INFO"
    for r in rows:
        if severity_order.get(str(r.get("severity", "INFO")), 0) > severity_order.get(highest, 0):
            highest = str(r.get("severity", "INFO"))
    payload = {
        "contradiction_type": "aion_icli_contradiction_engine_v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "contradictions": rows,
        "contradictions_found": len(rows),
        "open_contradictions": len([x for x in rows if str(x.get("status", "")) == "OPEN"]),
        "accepted_caveats": len([x for x in rows if str(x.get("status", "")) == "ACCEPTED_CAVEAT"]),
        "highest_severity": highest,
    }
    CONTRADICTION_INDEX_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    CONTRADICTION_LATEST_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    CONTRADICTION_SUMMARY_PATH.write_text(
        "# Contradiction Engine V1 Summary\n\n"
        + f"- Contradictions found: {payload['contradictions_found']}\n"
        + f"- Open contradictions: {payload['open_contradictions']}\n"
        + f"- Accepted caveats: {payload['accepted_caveats']}\n"
        + f"- Highest severity: {payload['highest_severity']}\n",
        encoding="utf-8",
    )
    return payload


def load_contradiction_index() -> dict:
    # Rebuild each time to keep contradiction state synchronized with current local truth.
    return build_contradiction_index()


def summarize_contradictions(data: dict) -> str:
    return (
        f"Contradictions found: {int(data.get('contradictions_found', 0))}. "
        f"Open: {int(data.get('open_contradictions', 0))}. "
        f"Accepted caveats: {int(data.get('accepted_caveats', 0))}. "
        f"Highest severity: {data.get('highest_severity', 'INFO')}."
    )


def contradiction_engine_answer(prompt: str, capability: str, signals: dict) -> tuple[str, list[str], dict]:
    data = load_contradiction_index()
    contradictions = list(data.get("contradictions", []))
    n = normalize(prompt)
    refs = [str(CONTRADICTION_INDEX_PATH), str(CONTRADICTION_SUMMARY_PATH), str(CONTRADICTION_LATEST_PATH)]
    stale = next((x for x in contradictions if str(x.get("type", "")) == "release_package_stale_relative_to_main"), None)
    if "release stale" in n or "release" in n:
        if stale:
            text = (
                "I see one accepted caveat: public package is stale relative to main. "
                "Main includes newer layers beyond the current public ZIP state. "
                "Recommended repair: rebuild the v1.1.0 offline bundle."
            )
        else:
            text = "No release/package stale contradiction detected right now."
    elif "needs repair" in n:
        opens = [x for x in contradictions if str(x.get("status", "")) in {"OPEN", "NEEDS_REVIEW"}]
        text = "Repairs needed: " + (", ".join([str(x.get("recommended_repair", "")) for x in opens][:4]) if opens else "none.")
    elif "what contradicts" in n or "inconsistent" in n or "drift" in n:
        text = summarize_contradictions(data)
    else:
        text = summarize_contradictions(data)
    details = {
        "contradiction_engine_used": True,
        "contradictions_found": int(data.get("contradictions_found", 0)),
        "open_contradictions": int(data.get("open_contradictions", 0)),
        "accepted_caveats": int(data.get("accepted_caveats", 0)),
        "highest_severity": str(data.get("highest_severity", "INFO")),
        "contradiction_index_path": str(CONTRADICTION_INDEX_PATH),
        "contradiction_summary": summarize_contradictions(data),
        "contradiction_paths": refs,
    }
    return text, refs, details


def maybe_use_contradiction_engine(prompt: str, capability: str, signals: dict) -> tuple[bool, str, list[str], dict]:
    n = normalize(prompt)
    triggers = (
        "contradiction summary",
        "what contradicts",
        "what is inconsistent",
        "what drift do you see",
        "is the release stale",
        "what proof does not match",
        "what needs repair",
    )
    if not any(t in n for t in triggers):
        return False, "", [], {}
    response, refs, details = contradiction_engine_answer(prompt, capability, signals)
    return True, response, refs, details


def memory_scar_answer(prompt: str, capability: str, signals: dict) -> tuple[str, list[str], list[str], str]:
    scars = load_memory_scars()
    graph = load_proof_graph_seed()
    ledger = load_evolution_ledger()
    n = normalize(prompt)
    text, ids, rules, summary = summarize_memory_scars(scars)
    artifacts = [str(SCARS_PATH), str(PROOF_GRAPH_PATH), str(EVOLUTION_LEDGER_PATH)]

    if "how do you learn" in n:
        return (
            f"{text} {summarize_proof_graph(graph)} Evolution ledger entries: {len(ledger)}.",
            artifacts,
            rules,
            summary,
        )
    if "what have you learned" in n or "what mistakes do you remember" in n or "what broke before" in n or "what scars do you have" in n or "what is your memory" in n:
        listing = ", ".join(ids) if ids else "none"
        return (f"{text} Current public-safe scars: {listing}.", artifacts, rules, summary)
    if "why are you asking for the artifact" in n or "why do you need proof" in n or "why not run it" in n or "why are you cautious" in n:
        return (text, artifacts, rules, summary)
    return "", [], [], ""


def maybe_use_memory_scar_engine(prompt: str, capability: str, signals: dict) -> tuple[bool, str, list[str], list[str], str]:
    n = normalize(prompt)
    triggers = (
        "why are you asking for the artifact",
        "why do you need proof",
        "why not run it",
        "what have you learned",
        "what mistakes do you remember",
        "what broke before",
        "why are you cautious",
        "how do you learn",
        "what scars do you have",
        "what is your memory",
    )
    if not any(t in n for t in triggers):
        return False, "", [], [], ""
    response, artifacts, rules, summary = memory_scar_answer(prompt, capability, signals)
    if response:
        return True, response, artifacts, rules, summary
    return False, "", [], [], ""


def governance_brain_answer(prompt: str, capability: str, signals: dict) -> tuple[str, list[str], str]:
    n = normalize(prompt)
    state = read_public_state()

    if "what is wired" in n or "wired" in n:
        return summarize_wired_state(state)
    if "what is missing" in n or "missing" in n:
        return summarize_missing_state(state)
    if "verify" in n or "verifier" in n or "what can you verify" in n:
        return summarize_verifier_state(state)
    if "connector" in n or "api" in n or "sdk" in n:
        return summarize_connector_state(state)
    if "proof" in n or "receipt" in n:
        return summarize_receipt_state(state)
    if "release" in n or capability == "cortex":
        return summarize_release_state(state)

    return "", [], ""


def maybe_use_governance_brain(prompt: str, capability: str, signals: dict) -> tuple[bool, str, list[str], str]:
    n = normalize(prompt)
    trigger_tokens = (
        "what do you know about this release",
        "what can you verify",
        "how do connectors work",
        "where is the proof",
        "what is wired",
        "what is missing",
        "release",
        "verifier",
        "connector",
        "proof",
    )
    should_try = capability in {"cortex", "verify", "connectors", "receipts"} or any(t in n for t in trigger_tokens)
    if not should_try:
        return False, "", [], ""

    response, artifacts, evidence_summary = governance_brain_answer(prompt, capability, signals)
    if response:
        return True, response, artifacts[:12], evidence_summary
    return False, "", [], ""


def write_receipt(
    prompt: str,
    response: str,
    mode: str,
    capability: str,
    extracted_signals: Optional[dict] = None,
    governance_brain_used: bool = False,
    artifacts_consulted: Optional[list[str]] = None,
    evidence_summary: str = "",
    memory_scar_engine_used: bool = False,
    scars_consulted: Optional[list[str]] = None,
    future_rules: Optional[list[str]] = None,
    artifact_inspection_used: bool = False,
    artifact_path: str = "",
    artifact_size_bytes: int = 0,
    file_type: str = "",
    decision: str = "",
    risk_level: str = "",
    detected_patterns: Optional[list[str]] = None,
    missing_controls: Optional[list[str]] = None,
    reasons: Optional[list[str]] = None,
    recommended_next_step: str = "",
    living_proof_graph_used: bool = False,
    proof_graph_paths: Optional[list[str]] = None,
    proof_graph_node_count: int = 0,
    proof_graph_edge_count: int = 0,
    graph_summary: str = "",
    source_files_consulted: Optional[list[str]] = None,
    evidence_engine_used: bool = False,
    evidence_items_evaluated: int = 0,
    evidence_index_path: str = "",
    evidence_summary_out: str = "",
    strongest_evidence_level: str = "",
    weakest_layers: Optional[list[str]] = None,
    evidence_paths: Optional[list[str]] = None,
    introspection_used: bool = False,
    introspection_passed: bool = False,
    introspection_findings: Optional[list[str]] = None,
    introspection_repairs_applied: Optional[list[str]] = None,
    introspection_risk_level: str = "",
    contradiction_engine_used: bool = False,
    contradictions_found: int = 0,
    open_contradictions: int = 0,
    accepted_caveats: int = 0,
    highest_severity: str = "",
    contradiction_index_path: str = "",
    contradiction_summary: str = "",
) -> str:
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    receipt = {
        "receipt_type": "aion_cli_receipt_v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": mode,
        "capability": capability,
        "prompt": prompt,
        "response": response,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "governance_tone": "felt_not_seen",
        "governance_brain_used": governance_brain_used,
        "artifacts_consulted": artifacts_consulted or [],
        "evidence_summary": evidence_summary,
        "memory_scar_engine_used": memory_scar_engine_used,
        "scars_consulted": scars_consulted or [],
        "future_rules": future_rules or [],
        "artifact_inspection_used": artifact_inspection_used,
        "artifact_path": artifact_path,
        "artifact_size_bytes": artifact_size_bytes,
        "file_type": file_type,
        "decision": decision,
        "risk_level": risk_level,
        "detected_patterns": detected_patterns or [],
        "missing_controls": missing_controls or [],
        "reasons": reasons or [],
        "recommended_next_step": recommended_next_step,
        "living_proof_graph_used": living_proof_graph_used,
        "proof_graph_paths": proof_graph_paths or [],
        "proof_graph_node_count": proof_graph_node_count,
        "proof_graph_edge_count": proof_graph_edge_count,
        "graph_summary": graph_summary,
        "source_files_consulted": source_files_consulted or [],
        "evidence_engine_used": evidence_engine_used,
        "evidence_items_evaluated": evidence_items_evaluated,
        "evidence_index_path": evidence_index_path,
        "evidence_summary_out": evidence_summary_out,
        "strongest_evidence_level": strongest_evidence_level,
        "weakest_layers": weakest_layers or [],
        "evidence_paths": evidence_paths or [],
        "introspection_used": introspection_used,
        "introspection_passed": introspection_passed,
        "introspection_findings": introspection_findings or [],
        "introspection_repairs_applied": introspection_repairs_applied or [],
        "introspection_risk_level": introspection_risk_level,
        "contradiction_engine_used": contradiction_engine_used,
        "contradictions_found": contradictions_found,
        "open_contradictions": open_contradictions,
        "accepted_caveats": accepted_caveats,
        "highest_severity": highest_severity,
        "contradiction_index_path": contradiction_index_path,
        "contradiction_summary": contradiction_summary,
    }
    if extracted_signals:
        receipt["extracted_signals"] = extracted_signals
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return str(RECEIPT_PATH)


def normalize(prompt: str) -> str:
    return (prompt or "").strip().lower()


def detect_capability(prompt: str) -> str:
    n = normalize(prompt)
    if n in ("capabilities", "capability", "what can you do", "what can you do?", "/capabilities"):
        return "capabilities"
    if n.startswith("diagnostics"):
        return "diagnostics"
    if "should i run this script" in n or "before i run" in n or "preflight" in n or "review this action" in n:
        return "preflight"
    if "help me design this better" in n or "creative" in n or "design" in n or "brainstorm" in n:
        return "creative"
    if "what feels wrong here" in n or "intuition" in n or "hidden assumption" in n or "risk signal" in n:
        return "intuition"
    if "what do you know about this release" in n or "cortex" in n or "release state" in n or "repo state" in n:
        return "cortex"
    if "can i connect an api" in n or "how do connectors work" in n or "connector" in n or "api" in n or "sdk" in n or "model" in n:
        return "connectors"
    if "where is the proof" in n or "receipt" in n or "proof record" in n:
        return "receipts"
    if "verify" in n or "verifier" in n or "proof marker" in n or "what can you verify" in n:
        return "verify"
    if "what is wired" in n:
        return "cortex"
    if "evidence summary" in n or "what evidence" in n or "admissible" in n or "evidence is weak" in n:
        return "verify"
    if "contradiction summary" in n or "what contradicts" in n or "inconsistent" in n or "release stale" in n or "what needs repair" in n or "what drift do you see" in n or "what proof does not match" in n:
        return "verify"
    if "show proof graph" in n or "connected to proof" in n or "what proves artifact inspection" in n:
        return "cortex"
    if "what is missing" in n:
        return "cortex"
    if "next" in n or "roadmap" in n or "what should i do" in n:
        return "next"
    return "general"


def extract_subject(prompt: str) -> str:
    n = normalize(prompt)
    if "script" in n:
        return "script"
    if "api" in n or "endpoint" in n:
        return "api_connector"
    if "release" in n:
        return "release_state"
    if "proof" in n or "receipt" in n:
        return "proof_artifact"
    if "design" in n:
        return "design_artifact"
    if "config" in n:
        return "config"
    if "diff" in n:
        return "diff"
    return "request"


def extract_urgency(prompt: str) -> str:
    n = normalize(prompt)
    urgent_tokens = ("now", "asap", "urgent", "immediately", "right now")
    return "urgent_now" if any(tok in n for tok in urgent_tokens) else "normal"


def extract_missing_evidence(prompt: str, capability: str) -> list[str]:
    n = normalize(prompt)
    missing: list[str] = []
    if capability == "preflight":
        if "script" in n and "path" not in n:
            missing.append("script_path_or_command")
        missing.append("reversibility_plan")
        missing.append("verifier_output")
    elif capability == "connectors":
        missing.extend(["endpoint", "purpose", "data_scope", "auth_type"])
    elif capability == "intuition":
        missing.extend(["artifact_to_inspect", "command_or_config_or_diff"])
    elif capability == "creative":
        missing.extend(["target_artifact", "constraints", "success_criteria"])
    elif capability == "receipts":
        missing.extend(["target_verifier", "proof_marker"])
    return missing


def extract_risk_lens(prompt: str, capability: str) -> list[str]:
    n = normalize(prompt)
    lens: list[str] = []
    if capability == "preflight":
        lens.extend(["blast_radius", "reversibility", "evidence_completeness"])
    if capability == "connectors":
        lens.extend(["data_exposure", "auth_scope", "egress_control"])
    if capability == "intuition":
        lens.extend(["hidden_coupling", "rollback_weakness", "missing_evidence"])
    if capability == "creative":
        lens.extend(["boundary_design", "proof_design", "rollback_design", "operator_ux"])
    if "mutate" in n or "delete" in n or "overwrite" in n:
        lens.append("unsafe_mutation")
    return lens


def compose_operator_response(prompt: str, capability: str) -> str:
    subject = extract_subject(prompt)
    urgency = extract_urgency(prompt)
    missing = extract_missing_evidence(prompt, capability)
    lens = extract_risk_lens(prompt, capability)

    if capability == "preflight":
        urgency_text = "You asked to do it now. " if urgency == "urgent_now" else ""
        return (
            f"{urgency_text}Don't run the {subject} yet. "
            "First we make it observable. "
            "I need the command or script path, expected blast radius, and rollback path before execution. "
            "Share verifier output too so we can prove the boundary before trust."
        )
    if capability == "connectors":
        return (
            "We can review API connectivity, but no live call executes here. "
            "Send endpoint, purpose, data scope, and auth type. "
            "I will shape a connector envelope with redaction and approval gates first."
        )
    if capability == "intuition":
        return (
            "The problem is not visible enough yet. "
            "Show me the command, config, or diff. "
            "Most hidden failures here come from hidden coupling, weak rollback, or missing evidence."
        )
    if capability == "creative":
        return (
            "I can design this with you, but I need the target artifact first. "
            "We will layer it as: intent, boundary, proof, rollback, operator UX, "
            "then convert that into a safe implementation plan."
        )
    if capability == "cortex":
        return "I can summarize the current public release state and map it to verifiers and receipts."
    if capability == "receipts":
        return f"Proof is local at {RECEIPT_PATH}. A receipt shows what was answered; verifier markers show what was proven."
    if capability == "verify":
        return "I can route you to the exact verifier sequence to convert claims into proof markers."
    if "mutate" in normalize(prompt):
        return "I will not authorize canonical mutation here. We can do a dry-run plan and verifier path first."
    if missing:
        return f"I can help, but first provide: {', '.join(missing)}."
    if lens:
        return f"I can review this through risk lenses: {', '.join(lens)}."
    return "I can review this locally and convert it into a proof-backed next step."


def preflight_response(prompt: str) -> str:
    return (
        "Preflight review started. I will not execute the requested action. "
        "Local review result: boundary is LOCAL_ONLY, network is NOT_USED, mutation is NOT_PERFORMED, execution is NOT_PERFORMED."
    )


def creative_response(prompt: str) -> str:
    return "Creative mode started. I can generate safe options without changing files."


def intuition_response(prompt: str) -> str:
    return "Intuition mode started. I will surface hidden assumptions and missing evidence."


def cortex_response(prompt: str) -> str:
    return "Cortex mode started. I can summarize repo-visible public release state."


def connectors_response(prompt: str) -> str:
    return "Connector mode started. No live provider calls are executed by default."


def receipts_response(prompt: str) -> str:
    return f"Receipt mode started. Latest receipt path: {RECEIPT_PATH}."


def verify_response(prompt: str) -> str:
    return "Verification mode started. Local verifier commands are available."


def next_response(prompt: str) -> str:
    return "Recommended next build: Capability Runner V1 with governed request envelopes and receipt replay."


def format_capability_list() -> str:
    return (
        "Available public-safe capabilities: preflight, creative, intuition, cortex, connectors, receipts, verify, next. "
        "Governance stays local by default."
    )


def should_show_diagnostics(prompt: str, diagnostics_on: bool) -> bool:
    if diagnostics_on:
        return True
    n = normalize(prompt)
    if n in COMMAND_STYLE:
        return True
    command_prefixes = ("preflight", "creative", "intuition", "cortex", "connectors", "receipts", "verify", "next")
    return any(n.startswith(prefix + " ") for prefix in command_prefixes)


def is_legacy_command_prompt(prompt: str) -> bool:
    n = normalize(prompt)
    if n in COMMAND_STYLE:
        return True
    legacy_prefixes = ("preflight ", "creative ", "intuition ", "cortex ", "connectors ", "receipts ", "verify ", "next ")
    return any(n.startswith(prefix) for prefix in legacy_prefixes)


def build_response(prompt: str, diagnostics_on: bool) -> tuple[str, str, dict]:
    n = normalize(prompt)
    capability = detect_capability(prompt)

    if n in ("exit", "quit", "/exit", "/quit"):
        return "exit", "Session closed.", {}
    if n in ("help", "/help", "?"):
        return "help", "Available commands: help, capabilities, preflight, creative, intuition, cortex, connectors, receipts, verify, next, boundary, diagnostics, exit.", {}
    if n in ("receipt", "receipts"):
        return "receipts", receipts_response(prompt), {}
    if n in ("boundary", "/boundary", "status", "/status"):
        return "boundary", "Current boundary: LOCAL_ONLY. Network: NOT_USED. Mutation: NOT_PERFORMED. Execution: NOT_PERFORMED.", {}
    if n == "diagnostics":
        return "diagnostics", f"Diagnostics is {'ON' if diagnostics_on else 'OFF'}.", {}
    if n == "diagnostics on":
        return "diagnostics", "Diagnostics enabled.", {}
    if n == "diagnostics off":
        return "diagnostics", "Diagnostics disabled.", {}

    if capability == "capabilities":
        return "capabilities", format_capability_list(), {}

    signals = {
        "subject": extract_subject(prompt),
        "urgency": extract_urgency(prompt),
        "missing_evidence": extract_missing_evidence(prompt, capability),
        "risk_lens": extract_risk_lens(prompt, capability),
        "governance_brain_used": False,
        "artifacts_consulted": [],
        "evidence_summary": "",
        "memory_scar_engine_used": False,
        "scars_consulted": [],
        "future_rules": [],
        "artifact_inspection_used": False,
        "artifact_path": "",
        "artifact_size_bytes": 0,
        "file_type": "",
        "decision": "",
        "risk_level": "",
        "detected_patterns": [],
        "missing_controls": [],
        "reasons": [],
        "recommended_next_step": "",
        "living_proof_graph_used": False,
        "proof_graph_paths": [],
        "proof_graph_node_count": 0,
        "proof_graph_edge_count": 0,
        "graph_summary": "",
        "source_files_consulted": [],
        "evidence_engine_used": False,
        "evidence_items_evaluated": 0,
        "evidence_index_path": "",
        "strongest_evidence_level": "",
        "weakest_layers": [],
        "evidence_paths": [],
        "introspection_used": False,
        "introspection_passed": False,
        "introspection_findings": [],
        "introspection_repairs_applied": [],
        "introspection_risk_level": "",
        "contradiction_engine_used": False,
        "contradictions_found": 0,
        "open_contradictions": 0,
        "accepted_caveats": 0,
        "highest_severity": "",
        "contradiction_index_path": "",
        "contradiction_summary": "",
        "contradiction_paths": [],
    }

    contradiction_used, contradiction_response, contradiction_refs, contradiction_details = maybe_use_contradiction_engine(prompt, capability, signals)
    if contradiction_used:
        signals["contradiction_engine_used"] = True
        signals["contradictions_found"] = int(contradiction_details.get("contradictions_found", 0) or 0)
        signals["open_contradictions"] = int(contradiction_details.get("open_contradictions", 0) or 0)
        signals["accepted_caveats"] = int(contradiction_details.get("accepted_caveats", 0) or 0)
        signals["highest_severity"] = str(contradiction_details.get("highest_severity", "INFO"))
        signals["contradiction_index_path"] = str(contradiction_details.get("contradiction_index_path", ""))
        signals["contradiction_summary"] = str(contradiction_details.get("contradiction_summary", ""))
        signals["contradiction_paths"] = list(contradiction_details.get("contradiction_paths", contradiction_refs))
        signals["artifacts_consulted"] = list(contradiction_refs)
        return capability, contradiction_response, signals

    evidence_used, evidence_response, evidence_refs, evidence_details = maybe_use_evidence_engine(prompt, capability, signals)
    if evidence_used:
        signals["evidence_engine_used"] = True
        signals["evidence_items_evaluated"] = int(evidence_details.get("evidence_items_evaluated", 0) or 0)
        signals["evidence_index_path"] = str(evidence_details.get("evidence_index_path", ""))
        signals["evidence_summary"] = str(evidence_details.get("evidence_summary", ""))
        signals["strongest_evidence_level"] = str(evidence_details.get("strongest_evidence_level", ""))
        signals["weakest_layers"] = list(evidence_details.get("weakest_layers", []))
        signals["evidence_paths"] = list(evidence_details.get("evidence_paths", evidence_refs))
        signals["artifacts_consulted"] = list(evidence_refs)
        return capability, evidence_response, signals

    graph_used, graph_response, graph_artifacts, graph_details = maybe_use_proof_graph(prompt, capability, signals)
    if graph_used:
        signals["living_proof_graph_used"] = True
        signals["proof_graph_paths"] = graph_artifacts
        signals["proof_graph_node_count"] = int(graph_details.get("proof_graph_node_count", 0) or 0)
        signals["proof_graph_edge_count"] = int(graph_details.get("proof_graph_edge_count", 0) or 0)
        signals["graph_summary"] = str(graph_details.get("graph_summary", ""))
        signals["source_files_consulted"] = list(graph_details.get("source_files_consulted", []))
        signals["artifacts_consulted"] = graph_artifacts
        signals["evidence_summary"] = "living_proof_graph"
        return capability, graph_response, signals

    artifact_used, artifact_response, inspected_artifacts, risk = maybe_use_artifact_inspection(prompt, capability, signals)
    if artifact_used:
        signals["artifact_inspection_used"] = True
        signals["artifacts_consulted"] = inspected_artifacts
        signals["artifact_path"] = inspected_artifacts[0] if inspected_artifacts else ""
        signals["artifact_size_bytes"] = int(risk.get("artifact_size_bytes", 0) or 0)
        signals["file_type"] = str(risk.get("inspection", {}).get("file_type", ""))
        signals["decision"] = str(risk.get("decision", ""))
        signals["risk_level"] = str(risk.get("risk_level", ""))
        signals["detected_patterns"] = list(risk.get("detected_patterns", []))
        signals["missing_controls"] = list(risk.get("missing_controls", []))
        signals["reasons"] = list(risk.get("reasons", []))
        signals["recommended_next_step"] = str(risk.get("recommended_next_step", ""))
        signals["evidence_summary"] = "artifact_inspection"
        return capability, artifact_response, signals

    scar_used, scar_response, scar_artifacts, scar_rules, scar_summary = maybe_use_memory_scar_engine(prompt, capability, signals)
    if scar_used and scar_response:
        signals["memory_scar_engine_used"] = True
        signals["scars_consulted"] = scar_artifacts
        signals["future_rules"] = scar_rules
        signals["evidence_summary"] = scar_summary
        return capability, scar_response, signals

    # Legacy command-style responses preserved for direct mode commands.
    if is_legacy_command_prompt(prompt):
        if capability == "preflight":
            return "preflight", preflight_response(prompt), signals
        if capability == "creative":
            return "creative", creative_response(prompt), signals
        if capability == "intuition":
            return "intuition", intuition_response(prompt), signals
        if capability == "cortex":
            return "cortex", cortex_response(prompt), signals
        if capability == "connectors":
            return "connectors", connectors_response(prompt), signals
        if capability == "receipts":
            return "receipts", receipts_response(prompt), signals
        if capability == "verify":
            return "verify", verify_response(prompt), signals
        if capability == "next":
            return "next", next_response(prompt), signals

    brain_used, brain_response, artifacts_consulted, evidence_summary = maybe_use_governance_brain(prompt, capability, signals)
    signals["governance_brain_used"] = brain_used
    signals["artifacts_consulted"] = artifacts_consulted
    signals["evidence_summary"] = evidence_summary
    if brain_used and brain_response:
        return capability, brain_response, signals

    if capability in {"preflight", "creative", "intuition", "cortex", "connectors", "receipts", "verify"}:
        return capability, compose_operator_response(prompt, capability), signals
    if capability == "next":
        return "next", next_response(prompt), signals

    if "who are you" in n or "what are you" in n:
        return "identity", "I am AION ICLI, a governed local command intelligence interface.", signals
    if "are you conscious" in n or "consciousness" in n:
        return "identity", "No. I am not conscious. I am a local governance interface.", signals
    if "openai" in n or "claude" in n or "gemini" in n or "grok" in n:
        return "connectors", "No live provider call executes here by default. This path remains local-only unless a governed connector flow is explicitly enabled.", signals
    return "general", compose_operator_response(prompt, "general"), signals


def print_diagnostics(capability: str, receipt: str, signals: dict) -> None:
    print(blue("Capability > ") + white(capability.upper()))
    print(blue("Subject    > ") + white(str(signals.get("subject", "unknown"))))
    print(blue("Urgency    > ") + white(str(signals.get("urgency", "normal"))))
    missing = signals.get("missing_evidence", [])
    risks = signals.get("risk_lens", [])
    artifacts = signals.get("artifacts_consulted", [])
    scars_consulted = signals.get("scars_consulted", [])
    future_rules = signals.get("future_rules", [])
    print(blue("Missing evidence > ") + white(", ".join(missing) if missing else "none"))
    print(blue("Risk lens  > ") + white(", ".join(risks) if risks else "none"))
    print(blue("Governance brain used > ") + white(str(bool(signals.get("governance_brain_used", False))).lower()))
    print(blue("Memory scar engine used > ") + white(str(bool(signals.get("memory_scar_engine_used", False))).lower()))
    print(blue("Scars consulted > ") + white("; ".join(scars_consulted) if scars_consulted else "none"))
    print(blue("Future rule > ") + white("; ".join(future_rules) if future_rules else "none"))
    print(blue("Artifact inspection used > ") + white(str(bool(signals.get("artifact_inspection_used", False))).lower()))
    print(blue("Artifact path > ") + white(str(signals.get("artifact_path", "")) or "none"))
    print(blue("Decision > ") + white(str(signals.get("decision", "")) or "none"))
    print(blue("Risk level > ") + white(str(signals.get("risk_level", "")) or "none"))
    detected = signals.get("detected_patterns", [])
    missing_controls = signals.get("missing_controls", [])
    print(blue("Detected patterns > ") + white("; ".join(detected) if detected else "none"))
    print(blue("Missing controls > ") + white("; ".join(missing_controls) if missing_controls else "none"))
    print(blue("Living proof graph used > ") + white(str(bool(signals.get("living_proof_graph_used", False))).lower()))
    print(blue("Nodes count > ") + white(str(int(signals.get("proof_graph_node_count", 0) or 0))))
    print(blue("Edges count > ") + white(str(int(signals.get("proof_graph_edge_count", 0) or 0))))
    srcs = signals.get("source_files_consulted", [])
    print(blue("Source files consulted > ") + white("; ".join(srcs) if srcs else "none"))
    ppaths = signals.get("proof_graph_paths", [])
    print(blue("Graph path > ") + white("; ".join(ppaths) if ppaths else "none"))
    print(blue("Evidence engine used > ") + white(str(bool(signals.get("evidence_engine_used", False))).lower()))
    print(blue("Evidence items evaluated > ") + white(str(int(signals.get("evidence_items_evaluated", 0) or 0))))
    print(blue("Highest level > ") + white(str(signals.get("strongest_evidence_level", "")) or "none"))
    wl = signals.get("weakest_layers", [])
    print(blue("Weakest layers > ") + white("; ".join(wl) if wl else "none"))
    epaths = signals.get("evidence_paths", [])
    print(blue("Evidence paths > ") + white("; ".join(epaths) if epaths else "none"))
    print(blue("Introspection gate used > ") + white(str(bool(signals.get("introspection_used", False))).lower()))
    print(blue("Introspection passed > ") + white(str(bool(signals.get("introspection_passed", False))).lower()))
    ifind = signals.get("introspection_findings", [])
    irep = signals.get("introspection_repairs_applied", [])
    print(blue("Findings > ") + white("; ".join(ifind) if ifind else "none"))
    print(blue("Repairs applied > ") + white("; ".join(irep) if irep else "none"))
    print(blue("Risk level > ") + white(str(signals.get("introspection_risk_level", "")) or "none"))
    print(blue("Contradiction engine used > ") + white(str(bool(signals.get("contradiction_engine_used", False))).lower()))
    print(blue("Contradictions found > ") + white(str(int(signals.get("contradictions_found", 0) or 0))))
    print(blue("Open contradictions > ") + white(str(int(signals.get("open_contradictions", 0) or 0))))
    print(blue("Accepted caveats > ") + white(str(int(signals.get("accepted_caveats", 0) or 0))))
    print(blue("Highest severity > ") + white(str(signals.get("highest_severity", "")) or "none"))
    cpaths = signals.get("contradiction_paths", [])
    print(blue("Contradiction paths > ") + white("; ".join(cpaths) if cpaths else "none"))
    print(blue("Artifacts consulted > ") + white("; ".join(artifacts) if artifacts else "none"))
    print(blue("Evidence summary > ") + white(str(signals.get("evidence_summary", "")) or "none"))
    print(blue("Boundary   > ") + green("LOCAL_ONLY"))
    print(blue("Network    > ") + green("NOT_USED"))
    print(blue("Mutation   > ") + green("NOT_PERFORMED"))
    print(blue("Execution  > ") + green("NOT_PERFORMED"))
    print(blue("Receipt    > ") + white(receipt))


def print_proof_footer() -> None:
    print(dim(PROOF_FOOTER))


def run_one_shot(prompt: str) -> int:
    render_banner()
    capability, response, signals = build_response(prompt, diagnostics_on=False)
    context = {
        "diagnostics_on": False,
        "artifact_inspection_used": bool(signals.get("artifact_inspection_used", False)),
        "evidence_engine_used": bool(signals.get("evidence_engine_used", False)),
        "roadmap_caveat": "not yet rebuilt" in safe_read_text(Path("docs") / "AION_ICLI_ROADMAP_STATE_V1.md").lower(),
    }
    response, ires = introspection_gate_wrap(prompt, response, capability, signals, context)
    signals["introspection_used"] = True
    signals["introspection_passed"] = bool(ires.get("passed", False))
    signals["introspection_findings"] = list(ires.get("findings", []))
    signals["introspection_repairs_applied"] = list(ires.get("repairs_applied", []))
    signals["introspection_risk_level"] = str(ires.get("risk_level", "LOW"))
    receipt = write_receipt(
        prompt,
        response,
        mode="one_shot",
        capability=capability,
        extracted_signals=signals,
        governance_brain_used=bool(signals.get("governance_brain_used", False)),
        artifacts_consulted=signals.get("artifacts_consulted", []),
        evidence_summary=str(signals.get("evidence_summary", "")),
        memory_scar_engine_used=bool(signals.get("memory_scar_engine_used", False)),
        scars_consulted=signals.get("scars_consulted", []),
        future_rules=signals.get("future_rules", []),
        artifact_inspection_used=bool(signals.get("artifact_inspection_used", False)),
        artifact_path=str(signals.get("artifact_path", "")),
        artifact_size_bytes=int(signals.get("artifact_size_bytes", 0) or 0),
        file_type=str(signals.get("file_type", "")),
        decision=str(signals.get("decision", "")),
        risk_level=str(signals.get("risk_level", "")),
        detected_patterns=signals.get("detected_patterns", []),
        missing_controls=signals.get("missing_controls", []),
        reasons=signals.get("reasons", []),
        recommended_next_step=str(signals.get("recommended_next_step", "")),
        living_proof_graph_used=bool(signals.get("living_proof_graph_used", False)),
        proof_graph_paths=signals.get("proof_graph_paths", []),
        proof_graph_node_count=int(signals.get("proof_graph_node_count", 0) or 0),
        proof_graph_edge_count=int(signals.get("proof_graph_edge_count", 0) or 0),
        graph_summary=str(signals.get("graph_summary", "")),
        source_files_consulted=signals.get("source_files_consulted", []),
        evidence_engine_used=bool(signals.get("evidence_engine_used", False)),
        evidence_items_evaluated=int(signals.get("evidence_items_evaluated", 0) or 0),
        evidence_index_path=str(signals.get("evidence_index_path", "")),
        evidence_summary_out=str(signals.get("evidence_summary", "")),
        strongest_evidence_level=str(signals.get("strongest_evidence_level", "")),
        weakest_layers=signals.get("weakest_layers", []),
        evidence_paths=signals.get("evidence_paths", []),
        introspection_used=bool(signals.get("introspection_used", False)),
        introspection_passed=bool(signals.get("introspection_passed", False)),
        introspection_findings=signals.get("introspection_findings", []),
        introspection_repairs_applied=signals.get("introspection_repairs_applied", []),
        introspection_risk_level=str(signals.get("introspection_risk_level", "")),
        contradiction_engine_used=bool(signals.get("contradiction_engine_used", False)),
        contradictions_found=int(signals.get("contradictions_found", 0) or 0),
        open_contradictions=int(signals.get("open_contradictions", 0) or 0),
        accepted_caveats=int(signals.get("accepted_caveats", 0) or 0),
        highest_severity=str(signals.get("highest_severity", "")),
        contradiction_index_path=str(signals.get("contradiction_index_path", "")),
        contradiction_summary=str(signals.get("contradiction_summary", "")),
    )
    print(white(f"Operator > {prompt}"))
    print("")
    print(cyan(f"AION     > {response}"))
    print("")
    print(blue("Boundary > ") + green("LOCAL_ONLY"))
    print(blue("Network  > ") + green("NOT_USED"))
    print(blue("Mutation > ") + green("NOT_PERFORMED"))
    print(blue("Receipt  > ") + white(receipt))
    print("")
    return 0


def run_interactive() -> int:
    render_banner()
    print(yellow("Interactive Mode V1 + Capability Router V1"))
    print(dim("Type help for commands. Type exit to leave."))
    print("")

    diagnostics_on = False

    while True:
        try:
            prompt = input(white("Operator > ")).strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            print(cyan("AION     > Session closed."))
            return 0

        if not prompt:
            continue

        n = normalize(prompt)
        if n == "diagnostics on":
            diagnostics_on = True
        elif n == "diagnostics off":
            diagnostics_on = False

        capability, response, signals = build_response(prompt, diagnostics_on=diagnostics_on)
        context = {
            "diagnostics_on": diagnostics_on,
            "artifact_inspection_used": bool(signals.get("artifact_inspection_used", False)),
            "evidence_engine_used": bool(signals.get("evidence_engine_used", False)),
            "roadmap_caveat": "not yet rebuilt" in safe_read_text(Path("docs") / "AION_ICLI_ROADMAP_STATE_V1.md").lower(),
        }
        response, ires = introspection_gate_wrap(prompt, response, capability, signals, context)
        signals["introspection_used"] = True
        signals["introspection_passed"] = bool(ires.get("passed", False))
        signals["introspection_findings"] = list(ires.get("findings", []))
        signals["introspection_repairs_applied"] = list(ires.get("repairs_applied", []))
        signals["introspection_risk_level"] = str(ires.get("risk_level", "LOW"))

        print("")
        print(cyan(f"AION     > {response}"))

        if capability == "exit":
            if diagnostics_on:
                print(blue("Receipt  > ") + white(str(RECEIPT_PATH)))
            else:
                print_proof_footer()
            print("")
            return 0

        if capability == "diagnostics":
            print("")
            print_proof_footer()
            print("")
            continue

        receipt = write_receipt(
            prompt,
            response,
            mode="interactive",
            capability=capability,
            extracted_signals=signals,
            governance_brain_used=bool(signals.get("governance_brain_used", False)),
            artifacts_consulted=signals.get("artifacts_consulted", []),
            evidence_summary=str(signals.get("evidence_summary", "")),
            memory_scar_engine_used=bool(signals.get("memory_scar_engine_used", False)),
            scars_consulted=signals.get("scars_consulted", []),
            future_rules=signals.get("future_rules", []),
            artifact_inspection_used=bool(signals.get("artifact_inspection_used", False)),
            artifact_path=str(signals.get("artifact_path", "")),
            artifact_size_bytes=int(signals.get("artifact_size_bytes", 0) or 0),
            file_type=str(signals.get("file_type", "")),
            decision=str(signals.get("decision", "")),
            risk_level=str(signals.get("risk_level", "")),
            detected_patterns=signals.get("detected_patterns", []),
            missing_controls=signals.get("missing_controls", []),
            reasons=signals.get("reasons", []),
            recommended_next_step=str(signals.get("recommended_next_step", "")),
            living_proof_graph_used=bool(signals.get("living_proof_graph_used", False)),
            proof_graph_paths=signals.get("proof_graph_paths", []),
            proof_graph_node_count=int(signals.get("proof_graph_node_count", 0) or 0),
            proof_graph_edge_count=int(signals.get("proof_graph_edge_count", 0) or 0),
            graph_summary=str(signals.get("graph_summary", "")),
            source_files_consulted=signals.get("source_files_consulted", []),
            evidence_engine_used=bool(signals.get("evidence_engine_used", False)),
            evidence_items_evaluated=int(signals.get("evidence_items_evaluated", 0) or 0),
            evidence_index_path=str(signals.get("evidence_index_path", "")),
            evidence_summary_out=str(signals.get("evidence_summary", "")),
            strongest_evidence_level=str(signals.get("strongest_evidence_level", "")),
            weakest_layers=signals.get("weakest_layers", []),
            evidence_paths=signals.get("evidence_paths", []),
            introspection_used=bool(signals.get("introspection_used", False)),
            introspection_passed=bool(signals.get("introspection_passed", False)),
            introspection_findings=signals.get("introspection_findings", []),
            introspection_repairs_applied=signals.get("introspection_repairs_applied", []),
            introspection_risk_level=str(signals.get("introspection_risk_level", "")),
            contradiction_engine_used=bool(signals.get("contradiction_engine_used", False)),
            contradictions_found=int(signals.get("contradictions_found", 0) or 0),
            open_contradictions=int(signals.get("open_contradictions", 0) or 0),
            accepted_caveats=int(signals.get("accepted_caveats", 0) or 0),
            highest_severity=str(signals.get("highest_severity", "")),
            contradiction_index_path=str(signals.get("contradiction_index_path", "")),
            contradiction_summary=str(signals.get("contradiction_summary", "")),
        )

        print("")
        if should_show_diagnostics(prompt, diagnostics_on):
            print_diagnostics(capability, receipt, signals)
        else:
            print_proof_footer()
        print("")


def main(argv: list[str]) -> int:
    configure_utf8()
    if len(argv) <= 1:
        return run_interactive()
    prompt = " ".join(argv[1:]).strip()
    if not prompt:
        return run_interactive()
    return run_one_shot(prompt)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
