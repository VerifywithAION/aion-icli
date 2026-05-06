import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


AION_LOGO = r"""
█████╗ ██╗ ██████╗ ███╗   ██╗
██╔══██╗██║██╔═══██╗████╗  ██║
███████║██║██║   ██║██╔██╗ ██║
██╔══██║██║██║   ██║██║╚██╗██║
██║  ██║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
""".strip("\n")

RECEIPT_PATH = Path("receipts") / "local" / "aion_cli_receipt_v1.json"


CAPABILITY_MAP = {
    "preflight": {
        "name": "Preflight",
        "purpose": "Review an intended action before execution.",
        "does": [
            "classifies the request",
            "checks visible boundaries",
            "keeps execution off by default",
            "returns a local review result",
            "writes a receipt",
        ],
        "does_not": [
            "execute the action",
            "call external APIs",
            "mutate files",
            "approve hidden operations",
        ],
    },
    "creative": {
        "name": "Creative",
        "purpose": "Generate safe options, designs, naming, UX, docs, and implementation directions.",
        "does": [
            "produces structured ideas",
            "keeps proposals non-destructive",
            "separates options from execution",
            "writes a receipt",
        ],
        "does_not": [
            "silently modify the project",
            "claim implementation happened",
            "use external APIs by default",
        ],
    },
    "intuition": {
        "name": "Intuition",
        "purpose": "Surface hidden assumptions, uncertainty, risk signals, and missing evidence.",
        "does": [
            "flags what feels under-proven",
            "identifies uncertainty",
            "asks what evidence is missing",
            "keeps conclusions provisional",
            "writes a receipt",
        ],
        "does_not": [
            "pretend uncertainty is proof",
            "execute actions",
            "invent evidence",
        ],
    },
    "cortex": {
        "name": "Cortex",
        "purpose": "Summarize local public repo state from docs, reports, release metadata, and receipts.",
        "does": [
            "reports known public package state",
            "summarizes available docs and verifiers",
            "points to local receipts",
            "keeps analysis local",
            "writes a receipt",
        ],
        "does_not": [
            "read private systems",
            "call connected services",
            "claim full internal memory is wired",
        ],
    },
    "connectors": {
        "name": "Connectors",
        "purpose": "Explain safe connector, API, model, and SDK request-envelope patterns.",
        "does": [
            "describes public connector contracts",
            "points to examples",
            "keeps requests in dry-run review by default",
            "writes a receipt",
        ],
        "does_not": [
            "call live providers",
            "use provider keys",
            "execute integrations by default",
        ],
    },
    "receipts": {
        "name": "Receipts",
        "purpose": "Explain and locate local proof records.",
        "does": [
            "shows receipt path",
            "explains receipt fields",
            "records prompt and response",
            "records boundary/network/mutation/execution status",
        ],
        "does_not": [
            "upload receipts",
            "hide execution details",
            "replace independent verification",
        ],
    },
    "verify": {
        "name": "Verify",
        "purpose": "Explain how to run local proof/verifier scripts.",
        "does": [
            "lists verifier commands",
            "describes expected markers",
            "keeps verification local",
        ],
        "does_not": [
            "forge proof markers",
            "skip verifiers",
            "claim success without marker output",
        ],
    },
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
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("AION_NO_COLOR"):
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
    print(white("What I can do offline:"))
    print(cyan("- Answer from local rules and local project context"))
    print(cyan("- Evaluate actions before execution"))
    print(cyan("- Produce receipts and proof traces"))
    print(cyan("- Keep risky actions in review mode before execution"))
    print(cyan("- Route public capabilities: preflight, creative, intuition, cortex, connectors, receipts, verify"))
    print(cyan("- Preserve evidence for replay and audit"))
    print("")


def write_receipt(prompt: str, response: str, mode: str = "one_shot", capability: str = "general") -> str:
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

    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return str(RECEIPT_PATH)


def normalize(prompt: str) -> str:
    return (prompt or "").strip().lower()


def detect_capability(prompt: str) -> str:
    n = normalize(prompt)

    if n in ("capabilities", "capability", "what can you do", "what can you do?", "/capabilities"):
        return "capabilities"
    if "preflight" in n or "before execution" in n or "before i run" in n or "review this action" in n:
        return "preflight"
    if "creative" in n or "design" in n or "brainstorm" in n or "idea" in n or "name" in n:
        return "creative"
    if "intuition" in n or "feel wrong" in n or "hidden assumption" in n or "risk signal" in n or "uncertain" in n:
        return "intuition"
    if "cortex" in n or "repo state" in n or "release state" in n or "package state" in n or "remember" in n:
        return "cortex"
    if "connector" in n or "api" in n or "sdk" in n or "model" in n:
        return "connectors"
    if "receipt" in n or "proof record" in n:
        return "receipts"
    if "verify" in n or "verifier" in n or "proof marker" in n:
        return "verify"
    if "next" in n or "roadmap" in n or "what should i do" in n:
        return "next"
    return "general"


def format_capability_list() -> str:
    return (
        "Available public-safe capabilities: "
        "preflight, creative, intuition, cortex, connectors, receipts, verify, next. "
        "Each capability stays local by default, does not use the network, does not mutate files, "
        "does not execute actions, and writes a receipt."
    )


def format_capability_detail(key: str) -> str:
    info = CAPABILITY_MAP[key]
    does = "; ".join(info["does"])
    does_not = "; ".join(info["does_not"])
    return (
        f"{info['name']} mode — {info['purpose']} "
        f"It can: {does}. "
        f"It will not: {does_not}."
    )


def preflight_response(prompt: str) -> str:
    return (
        "Preflight review started. I will not execute the requested action. "
        "Local review result: boundary is LOCAL_ONLY, network is NOT_USED, mutation is NOT_PERFORMED, "
        "execution is NOT_PERFORMED. Next safe step: convert the action into a dry-run plan, then verify evidence before execution."
    )


def creative_response(prompt: str) -> str:
    return (
        "Creative mode started. I can generate public-safe options without changing files. "
        "Suggested structure: define the goal, list constraints, propose 3 options, mark risks, choose one next dry-run step, then write a receipt."
    )


def intuition_response(prompt: str) -> str:
    return (
        "Intuition mode started. My provisional read: check for hidden assumptions, missing evidence, unclear execution boundary, "
        "unverified claims, and anything that sounds helpful but has no receipt. This is not proof; it is a risk-sensing layer."
    )


def cortex_response(prompt: str) -> str:
    return (
        "Cortex mode started. Public repo state known to ICLI: release tag v1.0.0-public-icli exists, "
        "public ZIP package exists, User Guide V1 exists, Interactive Mode V1 is on main, and local verifiers are available. "
        "This public Cortex mode summarizes repo-visible state only."
    )


def connectors_response(prompt: str) -> str:
    return (
        "Connector mode started. AION can review API, SDK, and model request envelopes locally before live execution. "
        "Use the connector policy, safe API dry-run, safe model dry-run, and SDK examples. By default, no provider call, no network, and no mutation happens."
    )


def receipts_response(prompt: str) -> str:
    return (
        f"Receipt mode started. Latest receipt path: {RECEIPT_PATH}. "
        "Receipts record prompt, response, capability, boundary, network, mutation, execution, timestamp, and governance tone."
    )


def verify_response(prompt: str) -> str:
    return (
        "Verification mode started. Run these from PowerShell: "
        "scripts\\VERIFY_PUBLIC_SAFE.ps1; scripts\\VERIFY_CONNECTOR_POLICY_V2.ps1; "
        "scripts\\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1; scripts\\VERIFY_USER_GUIDE_V1.ps1; "
        "scripts\\VERIFY_INTERACTIVE_MODE_V1.ps1. Expected markers include AION_ICLI_PUBLIC_SAFE_VERIFY_OK and AION_INTERACTIVE_MODE_V1_VERIFY_OK."
    )


def next_response(prompt: str) -> str:
    return (
        "Recommended next build: Capability Runner V1. It should let ICLI load request-envelope JSON files, route them through preflight/connectors, "
        "produce governed decisions, and write capability-specific receipts while staying local and non-destructive by default."
    )


def answer(prompt: str) -> tuple[str, str]:
    n = normalize(prompt)
    capability = detect_capability(prompt)

    if n in ("help", "/help", "?"):
        return (
            "help",
            "Available commands: help, capabilities, preflight, creative, intuition, cortex, connectors, receipts, verify, next, boundary, exit. "
            "You can also ask normal questions about AION, APIs, SDKs, models, receipts, local governance, or release state."
        )

    if n in ("exit", "quit", "/exit", "/quit"):
        return ("exit", "Session closed. Receipts remain local for review.")

    if n in ("boundary", "/boundary", "status", "/status"):
        return (
            "boundary",
            "Current boundary: LOCAL_ONLY. Network: NOT_USED. Mutation: NOT_PERFORMED. Execution: NOT_PERFORMED."
        )

    if capability == "capabilities":
        return ("capabilities", format_capability_list())
    if capability == "preflight":
        return ("preflight", preflight_response(prompt))
    if capability == "creative":
        return ("creative", creative_response(prompt))
    if capability == "intuition":
        return ("intuition", intuition_response(prompt))
    if capability == "cortex":
        return ("cortex", cortex_response(prompt))
    if capability == "connectors":
        return ("connectors", connectors_response(prompt))
    if capability == "receipts":
        return ("receipts", receipts_response(prompt))
    if capability == "verify":
        return ("verify", verify_response(prompt))
    if capability == "next":
        return ("next", next_response(prompt))

    if "who are you" in n or "what are you" in n:
        return (
            "identity",
            "I am AION ICLI, a governed command-line intelligence interface. "
            "I help evaluate actions, route public-safe capabilities, expose boundaries, preserve receipts, "
            "and make proof visible before trust."
        )

    if "what is preflight" in n:
        return ("preflight", format_capability_detail("preflight"))
    if "what is creative" in n:
        return ("creative", format_capability_detail("creative"))
    if "what is intuition" in n:
        return ("intuition", format_capability_detail("intuition"))
    if "what is cortex" in n:
        return ("cortex", format_capability_detail("cortex"))

    return (
        "general",
        "I can help review this locally first. Try: capabilities, preflight, creative, intuition, cortex, connectors, receipts, verify, or next. "
        "I will keep network use, mutation, and execution off by default while preserving a receipt for later review."
    )


def print_exchange(prompt: str, response: str, receipt: str) -> None:
    print(white(f"Operator > {prompt}"))
    print("")
    print(cyan(f"AION     > {response}"))
    print("")
    print(blue("Boundary > ") + green("LOCAL_ONLY"))
    print(blue("Network  > ") + green("NOT_USED"))
    print(blue("Mutation > ") + green("NOT_PERFORMED"))
    print(blue("Receipt  > ") + white(receipt))
    print("")


def run_one_shot(prompt: str) -> int:
    render_banner()
    capability, response = answer(prompt)
    receipt = write_receipt(prompt, response, mode="one_shot", capability=capability)
    print_exchange(prompt, response, receipt)
    return 0


def run_interactive() -> int:
    render_banner()
    print(yellow("Interactive Mode V1 + Capability Router V1"))
    print(dim("Type help for commands. Type exit to leave."))
    print("")

    while True:
        try:
            prompt = input(white("Operator > ")).strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            print(cyan("AION     > Session closed."))
            return 0

        if not prompt:
            continue

        capability, response = answer(prompt)
        receipt = write_receipt(prompt, response, mode="interactive", capability=capability)

        print("")
        print(cyan(f"AION     > {response}"))

        if capability == "exit":
            print(blue("Receipt  > ") + white(receipt))
            print("")
            return 0

        print("")
        print(blue("Capability > ") + white(capability.upper()))
        print(blue("Boundary   > ") + green("LOCAL_ONLY"))
        print(blue("Network    > ") + green("NOT_USED"))
        print(blue("Mutation   > ") + green("NOT_PERFORMED"))
        print(blue("Execution  > ") + green("NOT_PERFORMED"))
        print(blue("Receipt    > ") + white(receipt))
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
