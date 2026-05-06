import json
import os
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


def write_receipt(prompt: str, response: str, mode: str, capability: str, extracted_signals: Optional[dict] = None) -> str:
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
    if "can i connect an api" in n or "connector" in n or "api" in n or "sdk" in n or "model" in n:
        return "connectors"
    if "where is the proof" in n or "receipt" in n or "proof record" in n:
        return "receipts"
    if "verify" in n or "verifier" in n or "proof marker" in n:
        return "verify"
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
    }

    if should_show_diagnostics(prompt, diagnostics_on):
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

    if capability in {"preflight", "creative", "intuition", "cortex", "connectors", "receipts", "verify"}:
        return capability, compose_operator_response(prompt, capability), signals
    if capability == "next":
        return "next", next_response(prompt), signals

    if "who are you" in n or "what are you" in n:
        return "identity", "I am AION ICLI, a governed local command intelligence interface.", signals
    return "general", compose_operator_response(prompt, "general"), signals


def print_diagnostics(capability: str, receipt: str, signals: dict) -> None:
    print(blue("Capability > ") + white(capability.upper()))
    print(blue("Subject    > ") + white(str(signals.get("subject", "unknown"))))
    print(blue("Urgency    > ") + white(str(signals.get("urgency", "normal"))))
    missing = signals.get("missing_evidence", [])
    risks = signals.get("risk_lens", [])
    print(blue("Missing evidence > ") + white(", ".join(missing) if missing else "none"))
    print(blue("Risk lens  > ") + white(", ".join(risks) if risks else "none"))
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
    receipt = write_receipt(prompt, response, mode="one_shot", capability=capability, extracted_signals=signals)
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
        receipt = write_receipt(prompt, response, mode="interactive", capability=capability, extracted_signals=signals)

        print("")
        print(cyan(f"AION     > {response}"))

        if capability == "exit":
            if diagnostics_on:
                print(blue("Receipt  > ") + white(receipt))
            else:
                print_proof_footer()
            print("")
            return 0

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

