import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
try:
    from aion_living_voice_adapter import generate_living_voice_response
except Exception:
    generate_living_voice_response = None
try:
    from aion_living_intelligence_kernel import analyze_living_request
except Exception:
    analyze_living_request = None

REPO_ROOT = Path(__file__).resolve().parent.parent
RECEIPT_PATH = REPO_ROOT / "receipts" / "local" / "aion_cli_receipt_v1.json"

DIAGNOSTICS = False
VOICE_MEMORY_TURNS = []

AION_LOGO = r"""
█████╗ ██╗ ██████╗ ███╗   ██╗
██╔══██╗██║██╔═══██╗████╗  ██║
███████║██║██║   ██║██╔██╗ ██║
██╔══██║██║██║   ██║██║╚██╗██║
██║  ██║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

""".strip("\n")

AION_NEON_LOGO = [
    "█████╗ ██╗ ██████╗ ███╗   ██╗",
    "██╔══██╗██║██╔═══██╗████╗  ██║",
    "███████║██║██║   ██║██╔██╗ ██║",
    "██╔══██║██║██║   ██║██║╚██╗██║",
    "██║  ██║██║╚██████╔╝██║ ╚████║",
    "╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝",
]

ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_CYAN = "\033[96m"
ANSI_BLUE = "\033[94m"
ANSI_WHITE = "\033[97m"
ANSI_GREEN = "\033[92m"

def supports_ansi():
    if os.environ.get("NO_COLOR"):
        return False
    term = os.environ.get("TERM", "")
    wt = os.environ.get("WT_SESSION", "")
    vscode = os.environ.get("TERM_PROGRAM", "")
    return bool(wt or vscode == "vscode" or "xterm" in term.lower() or os.name != "nt")

def neon(text, color):
    if supports_ansi():
        return f"{color}{ANSI_BOLD}{text}{ANSI_RESET}"
    return text

def render_neon_logo():
    if not supports_ansi():
        print(AION_LOGO)
        return
    colors = [ANSI_WHITE, ANSI_CYAN, ANSI_CYAN, ANSI_BLUE, ANSI_BLUE, ANSI_WHITE]
    for line, color in zip(AION_NEON_LOGO, colors):
        print(neon(line, color))

MEMORY_SCARS = [
    {
        "scar_id": "judging_without_artifact",
        "lesson": "No artifact, no judgment.",
        "future_rule": "When a user asks whether to run a script without a path, request the artifact path first."
    },
    {
        "scar_id": "proofless_claims",
        "lesson": "No verifier, no lock.",
        "future_rule": "Claims require receipts, verifier markers, or local evidence."
    }
]

SAFE_EXTENSIONS = {
    ".ps1", ".py", ".js", ".ts", ".tsx", ".html", ".htm", ".css",
    ".json", ".md", ".txt", ".yaml", ".yml", ".cmd", ".bat", ".sh"
}

FORBIDDEN_PARTS = {
    ".git", ".env", "node_modules", "__pycache__", ".venv", "venv", "private", "secrets", ".codara"
}

RISK_PATTERNS = {
    "network": [
        "invoke-webrequest", "invoke-restmethod", "curl ", "wget ", "requests.", "fetch(", "axios",
        "http://", "https://"
    ],
    "mutation": [
        "set-content", "add-content", "remove-item", "new-item", "copy-item", "move-item",
        "write_text", "open(", "fs.writefile", "git commit", "git push"
    ],
    "execution": [
        "start-process", "subprocess", "os.system", "powershell -file", "cmd.exe", "node ", "python ", "npm run"
    ],
    "secret": [
        "api_key", "secret", "token", "private_key", "seed phrase", "password"
    ],
    "governance": [
        "verifier", "verify_", "receipt", "dry-run", "dry run", "rollback", "local_only", "not_used"
    ]
}


def configure_utf8():
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def rel(path):
    try:
        return str(Path(path).resolve().relative_to(REPO_ROOT))
    except Exception:
        return str(path)


def render_banner():
    print("")
    render_neon_logo()
    print("")
    print(neon("AION ICLI", ANSI_CYAN))
    print(neon("Interactive Command Line Intelligence", ANSI_WHITE))
    print(neon("Governed Local Mode", ANSI_CYAN))
    print(neon("Offline-capable by design", ANSI_WHITE))
    print(neon("No external APIs by default", ANSI_GREEN))
    print("")
    print(neon("What I can do offline:", ANSI_CYAN))
    print("- Answer from local rules and local project context")
    print("- Evaluate actions before execution")
    print("- Produce receipts and proof traces")
    print("- Keep risky actions in review mode before execution")
    print("- Preserve evidence for replay and audit")
    print("")


def write_receipt(prompt, response, capability, inspection=None, artifacts=None):
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)

    receipt = {
        "receipt_type": "aion_cli_receipt_v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompt": prompt,
        "response": response,
        "capability": capability,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "governance_tone": "felt_not_seen",
        "governance_brain_used": capability in ["release_evidence", "verify", "wired", "missing"],
        "memory_scar_engine_used": capability == "memory_scar",
        "artifact_inspection_used": capability == "artifact_inspection",
        "artifacts_consulted": artifacts or [],
        "inspection": inspection,
        "next_pointer": "Public Release v1.2.0 Demo Gate"
    }

    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return rel(RECEIPT_PATH)


def norm(text):
    return (text or "").strip().lower()


def maybe_living_voice(prompt):
    if generate_living_voice_response is None:
        return None
    memory_state = {"recent_turns": VOICE_MEMORY_TURNS[-3:]}
    return generate_living_voice_response(prompt, memory_state=memory_state, context={"runtime": "aion_cli_entry"})


def should_use_living_intelligence(prompt):
    n = norm(prompt)
    triggers = [
        "ask aion",
        "think",
        "investigate",
        "what is the core truth",
        "what am i missing",
        "what is the next best question",
        "analyze this deeply",
    ]
    return any(n.startswith(t) for t in triggers)


def local_exists(path_text):
    return (REPO_ROOT / path_text).exists()


def read_json(path_text):
    p = REPO_ROOT / path_text
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return None


def discover_release_evidence():
    artifacts = []
    facts = []

    candidates = [
        ("proof_demo_pack/AION_ICLI_PROOF_DEMO_PACK_V1.json", "Proof Demo Pack V1"),
        ("release/AION_ICLI_RELEASE_EVIDENCE_INDEX_V1.json", "Release Evidence Index V1"),
        ("reports/AION_ICLI_RELEASE_EVIDENCE_INDEX_V1_REPORT.md", "Release Evidence Index report"),
        ("proof_demo_pack/reports/AION_ICLI_PROOF_DEMO_PACK_V1_REPORT.md", "Proof Demo Pack report"),
        ("dist/aion-public-demo-release-pack-v1.zip", "Public Demo Release Pack ZIP"),
        ("dist/aion-icli-offline-bundle-v1.1.0.zip", "Offline Bundle v1.1.0 ZIP"),
        ("scripts/VERIFY_AION_ICLI_PROOF_DEMO_PACK_V1.ps1", "Proof Demo Pack verifier"),
        ("scripts/VERIFY_AION_ICLI_RELEASE_EVIDENCE_INDEX_V1.ps1", "Release Evidence Index verifier"),
        ("scripts/VERIFY_PUBLIC_DEMO_RELEASE_PACK_V1.ps1", "Public Demo Release Pack verifier"),
        ("scripts/VERIFY_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1.ps1", "Fresh Clone Acceptance verifier"),
    ]

    for path_text, label in candidates:
        if local_exists(path_text):
            artifacts.append(path_text)
            facts.append(label)

    evidence = read_json("release/AION_ICLI_RELEASE_EVIDENCE_INDEX_V1.json")
    if evidence:
        head = evidence.get("current_head")
        if head:
            facts.append("current head recorded in evidence index")
        offline = evidence.get("offline_bundle", {})
        if isinstance(offline, dict) and offline.get("sha256"):
            facts.append("offline bundle SHA256 recorded")
        demo = evidence.get("public_demo_release_pack", {})
        if isinstance(demo, dict) and demo.get("sha256"):
            facts.append("public demo release pack SHA256 recorded")

    return facts, artifacts


def get_next_pointer():
    data = read_json(".aion_public/roadmap/roadmap_state_v1.json")
    if isinstance(data, dict):
        pointer = data.get("next_build_pointer")
        if pointer:
            return pointer
    return "Public Release v1.2.0 Demo Gate"


def extract_path_from_prompt(prompt):
    text = prompt.strip()
    lowered = text.lower()

    prefixes = [
        "should i run ",
        "inspect ",
        "review ",
        "analyze "
    ]

    for prefix in prefixes:
        if lowered.startswith(prefix):
            raw = text[len(prefix):].strip()
            raw = raw.strip("\"'` ")
            raw = raw.rstrip("?").strip()
            return raw

    match = re.search(r"([A-Za-z0-9_\-./\\]+?\.(ps1|py|js|ts|tsx|json|md|txt|yaml|yml|cmd|bat|sh))", text, re.I)
    if match:
        return match.group(1)

    return ""


def inspect_artifact(path_text):
    if not path_text:
        return {
            "allowed": False,
            "reason": "missing_artifact_path"
        }

    raw = path_text.strip().strip("\"'`")
    target = (REPO_ROOT / raw).resolve()

    try:
        target.relative_to(REPO_ROOT)
    except Exception:
        return {
            "allowed": False,
            "reason": "outside_repo_root",
            "path": raw
        }

    parts_lower = {p.lower() for p in target.parts}
    if parts_lower.intersection(FORBIDDEN_PARTS):
        return {
            "allowed": False,
            "reason": "forbidden_path",
            "path": rel(target)
        }

    if not target.exists():
        return {
            "allowed": False,
            "reason": "artifact_not_found",
            "path": raw
        }

    if not target.is_file():
        return {
            "allowed": False,
            "reason": "not_a_file",
            "path": rel(target)
        }

    if target.suffix.lower() not in SAFE_EXTENSIONS:
        return {
            "allowed": False,
            "reason": "unsupported_file_type",
            "path": rel(target)
        }

    size = target.stat().st_size
    if size > 262144:
        return {
            "allowed": False,
            "reason": "too_large",
            "path": rel(target),
            "size_bytes": size
        }

    text = target.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()

    detected = {}
    for category, patterns in RISK_PATTERNS.items():
        hits = []
        for pattern in patterns:
            if pattern in lower:
                hits.append(pattern)
        if hits:
            detected[category] = hits

    risk = "LOW"
    decision = "SAFE_TO_READ"
    reasons = []

    if detected.get("secret"):
        risk = "HIGH"
        decision = "REVIEW_ONLY"
        reasons.append("secret-like terms detected")
    if detected.get("execution"):
        risk = "HIGH"
        decision = "REVIEW_ONLY"
        reasons.append("execution indicators detected")
    if detected.get("mutation"):
        risk = "HIGH"
        decision = "REVIEW_ONLY"
        reasons.append("mutation indicators detected")
    if risk != "HIGH" and detected.get("network"):
        risk = "MEDIUM"
        decision = "DRY_RUN_REVIEW"
        reasons.append("network indicators detected")
    if detected.get("governance"):
        reasons.append("governance/verifier/receipt indicators detected")

    if not reasons:
        reasons.append("no high-risk indicators detected in quick read-only scan")

    missing_controls = []
    if risk in ["MEDIUM", "HIGH"]:
        if "rollback" not in lower:
            missing_controls.append("rollback")
        if "dry-run" not in lower and "dry run" not in lower:
            missing_controls.append("dry-run")
        if "verify" not in lower and "verifier" not in lower:
            missing_controls.append("verifier")

    return {
        "allowed": True,
        "path": rel(target),
        "size_bytes": size,
        "file_type": target.suffix.lower(),
        "decision": decision,
        "risk_level": risk,
        "detected_patterns": detected,
        "missing_controls": missing_controls,
        "reasons": reasons,
        "recommended_next_step": "Review the file and run only the matching verifier/dry-run path. Do not auto-execute."
    }


def format_inspection_response(inspection):
    if not inspection.get("allowed"):
        reason = inspection.get("reason", "unknown")
        if reason == "missing_artifact_path":
            return "I need the artifact path before judging it. No artifact, no judgment."
        return f"I could not inspect the artifact safely. Reason: {reason}."

    detected = inspection.get("detected_patterns") or {}
    detected_names = ", ".join(detected.keys()) if detected else "none"
    missing = inspection.get("missing_controls") or []
    missing_text = ", ".join(missing) if missing else "none"

    return (
        f"I inspected the local artifact read-only: {inspection['path']}. "
        f"Decision: {inspection['decision']}. Risk: {inspection['risk_level']}. "
        f"Detected pattern groups: {detected_names}. Missing controls: {missing_text}. "
        f"I did not execute it, did not use the network, and did not mutate files."
    )


def answer(prompt):
    global DIAGNOSTICS

    n = norm(prompt)

    if should_use_living_intelligence(prompt) and analyze_living_request is not None:
        kernel = analyze_living_request(prompt)
        insight = kernel.get("nonobvious_insight", "")
        reframe = kernel.get("dynamic_reframe", "")
        response = (
            kernel.get("direct_truth", "")
            + "\n\n"
            + ("Non-obvious insight: " + insight + "\n\n" if insight else "")
            + ("Dynamic reframe: " + reframe + "\n\n" if reframe else "")
            + "Next best question: "
            + kernel.get("next_best_question", "")
            + "\n\n"
            + kernel.get("governed_answer", "")
            + "\n\n"
            + kernel.get("next_admissible_move", "")
        )
        return "living_intelligence", response, kernel, []

    if n in ["exit", "quit"]:
        return "exit", "Session closed. Receipts remain local for review.", None, []

    if n in ["help", "?"]:
        return "help", "Available commands: help, receipt, boundary, verify, diagnostics on, diagnostics off, next, exit. You can also ask release/proof questions or ask whether to run a local artifact.", None, []

    if n == "diagnostics on":
        DIAGNOSTICS = True
        return "diagnostics", "Diagnostics mode enabled.", None, []

    if n == "diagnostics off":
        DIAGNOSTICS = False
        return "diagnostics", "Diagnostics mode disabled.", None, []

    if n in ["receipt", "receipts"]:
        return "receipts", f"Latest receipt path: {rel(RECEIPT_PATH)}.", None, []

    if n == "boundary":
        return "boundary", "Current boundary: LOCAL_ONLY. Network: NOT_USED. Mutation: NOT_PERFORMED. Execution: NOT_PERFORMED.", None, []

    if n == "verify" or "what should i run" in n:
        return "verify", "Run the local verifiers for this proof chain: scripts\\VERIFY_AION_ICLI_PROOF_DEMO_PACK_V1.ps1, scripts\\VERIFY_AION_ICLI_RELEASE_EVIDENCE_INDEX_V1.ps1, scripts\\VERIFY_PUBLIC_DEMO_RELEASE_PACK_V1.ps1, scripts\\VERIFY_PUBLIC_DEMO_FRESH_CLONE_ACCEPTANCE_V1.ps1.", None, []

    if n == "next":
        pointer = get_next_pointer()
        return "next", f"Next build pointer from roadmap state: {pointer}. Do not move forward without verifier evidence and synchronized roadmap/wiring artifacts.", None, [".aion_public/roadmap/roadmap_state_v1.json"]

    if "what do you know about this release" in n or "current release state" in n or "release proof" in n:
        facts, artifacts = discover_release_evidence()
        if not facts:
            return "release_evidence", "I do not see enough local release evidence yet. No evidence, no release claim.", None, artifacts
        return "release_evidence", "I can see the local release proof chain: " + "; ".join(facts) + ".", None, artifacts

    if "where is the proof" in n or "what can you verify" in n:
        facts, artifacts = discover_release_evidence()
        msg = "Proof is local: verifier scripts, release evidence JSON/report, proof demo pack, public demo release pack, fresh-clone acceptance, and receipts. "
        if artifacts:
            msg += "Artifacts consulted: " + "; ".join(artifacts) + "."
        return "verify", msg, None, artifacts

    if "what is wired" in n:
        expected = [
            "docs/GOVERNANCE_BRAIN_ADAPTER_V1.md",
            "docs/MEMORY_SCAR_ENGINE_V1.md",
            "docs/ARTIFACT_INSPECTION_RUNNER_V1.md",
            "docs/AION_ICLI_ROADMAP_STATE_V1.md",
            "scripts/VERIFY_MEMORY_SCAR_ENGINE_V1.ps1",
            "scripts/VERIFY_ARTIFACT_INSPECTION_RUNNER_V1.ps1",
            "scripts/VERIFY_AION_ICLI_ROADMAP_AND_WIRING_V1.ps1"
        ]
        found = [x for x in expected if local_exists(x)]
        return "wired", "I can see wiring artifacts for: " + "; ".join(found) + ".", None, found

    if "what is missing" in n:
        return "missing", "Missing or gated by default: live provider calls, autonomous execution, network use, mutation, hidden integrations, provider keys, signed installer/EXE, and any claim without verifier evidence.", None, []

    if "why do you need proof" in n or "why do you need the artifact" in n or "why are you cautious" in n:
        return "memory_scar", "Because prior failure patterns show that judging without visible evidence creates false confidence. No artifact, no judgment. No verifier, no lock.", None, [".aion_public/scars/scars_seed.jsonl"]

    if n.startswith("should i run") or n.startswith("inspect ") or n.startswith("review ") or n.startswith("analyze "):
        candidate = extract_path_from_prompt(prompt)
        inspection = inspect_artifact(candidate)
        return "artifact_inspection", format_inspection_response(inspection), inspection, [inspection.get("path")] if inspection.get("path") else []

    if "who are you" in n or "what are you" in n:
        return "identity", "I am AION ICLI, a governed command-line intelligence interface. I help evaluate actions, expose boundaries, preserve receipts, and make proof visible before trust.", None, []

    if "api" in n or "sdk" in n or "model" in n or "connector" in n:
        return "connectors", "I can review API, SDK, or model request envelopes locally before live execution. By default I do not call providers, use the network, or mutate files.", None, []

    living_voice_triggers = [
        "genius", "brilliant", "continuity", "governance-aware", "non-obvious",
        "uncertain", "strategic", "reframe", "insight"
    ]
    if any(t in n for t in living_voice_triggers) or True:
        voice = maybe_living_voice(prompt)
        if isinstance(voice, dict):
            return "living_voice_adapter", voice.get("response", ""), voice, []

    return "general", "I can review this locally first. Give me the artifact, claim, verifier, or release question. No artifact, no judgment; no verifier, no lock.", None, []


def print_response(capability, response, receipt, inspection=None, artifacts=None):
    print("")
    print(f"AION     > {response}")

    if DIAGNOSTICS:
        print("")
        print(f"Capability > {capability.upper()}")
        print("Boundary   > LOCAL_ONLY")
        print("Network    > NOT_USED")
        print("Mutation   > NOT_PERFORMED")
        print("Execution  > NOT_PERFORMED")
        if artifacts:
            print("Artifacts  > " + "; ".join([str(x) for x in artifacts if x]))
        if inspection:
            print("Decision   > " + str(inspection.get("decision", "N/A")))
            print("Risk       > " + str(inspection.get("risk_level", "N/A")))
        print("Receipt    > " + receipt)
    else:
        print("")
        print("Boundary > LOCAL_ONLY")
        print("Network  > NOT_USED")
        print("Mutation > NOT_PERFORMED")
        print("Receipt  > " + receipt)

    print("")


def run_one_shot(prompt):
    render_banner()
    print(f"Operator > {prompt}")
    capability, response, inspection, artifacts = answer(prompt)
    VOICE_MEMORY_TURNS.append({"prompt": prompt, "response": response, "capability": capability})
    if len(VOICE_MEMORY_TURNS) > 20:
        del VOICE_MEMORY_TURNS[:-20]
    receipt = write_receipt(prompt, response, capability, inspection, artifacts)
    print_response(capability, response, receipt, inspection, artifacts)
    return 0


def run_interactive():
    render_banner()
    print("Interactive Mode V1 + Evidence-Governed Runtime")
    print("Type help for commands. Type exit to leave.")
    print("")

    while True:
        try:
            prompt = input("Operator > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            print("AION     > Session closed.")
            return 0

        if not prompt:
            continue

        capability, response, inspection, artifacts = answer(prompt)
        VOICE_MEMORY_TURNS.append({"prompt": prompt, "response": response, "capability": capability})
        if len(VOICE_MEMORY_TURNS) > 20:
            del VOICE_MEMORY_TURNS[:-20]
        receipt = write_receipt(prompt, response, capability, inspection, artifacts)
        print_response(capability, response, receipt, inspection, artifacts)

        if capability == "exit":
            return 0


def main(argv):
    configure_utf8()
    if len(argv) > 1:
        prompt = " ".join(argv[1:]).strip()
        if prompt:
            return run_one_shot(prompt)
    return run_interactive()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))


