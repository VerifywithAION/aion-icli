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
    print(cyan("- Preserve evidence for replay and audit"))
    print("")


def write_receipt(prompt: str, response: str, mode: str = "one_shot") -> str:
    RECEIPT_PATH.parent.mkdir(parents=True, exist_ok=True)

    receipt = {
        "receipt_type": "aion_cli_receipt_v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": mode,
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


def answer(prompt: str) -> str:
    normalized = (prompt or "").strip().lower()

    if normalized in ("help", "/help", "?"):
        return (
            "Available commands: help, receipt, boundary, verify, exit. "
            "You can also ask normal questions about AION, APIs, SDKs, models, receipts, or local governance."
        )

    if normalized in ("receipt", "/receipt", "show receipt", "latest receipt"):
        return (
            f"Latest receipt path: {RECEIPT_PATH}. "
            "Open it to inspect prompt, response, boundary, network, mutation, execution, and governance tone."
        )

    if normalized in ("boundary", "/boundary", "status", "/status"):
        return (
            "Current boundary: LOCAL_ONLY. Network: NOT_USED. Mutation: NOT_PERFORMED. "
            "Execution: NOT_PERFORMED."
        )

    if normalized in ("verify", "/verify", "verifiers"):
        return (
            "Run verifiers from PowerShell: "
            "scripts\\VERIFY_PUBLIC_SAFE.ps1, scripts\\VERIFY_CONNECTOR_POLICY_V2.ps1, "
            "scripts\\VERIFY_PUBLIC_INSTALL_PACKAGE_V1.ps1, scripts\\VERIFY_USER_GUIDE_V1.ps1."
        )

    if "who are you" in normalized or "what are you" in normalized:
        return (
            "I am AION ICLI, a governed command-line intelligence interface. "
            "I help evaluate actions, expose boundaries, preserve receipts, "
            "and make proof visible before trust."
        )

    if "api" in normalized or "sdk" in normalized or "model" in normalized:
        return (
            "I can review API, SDK, or model request envelopes locally before live execution. "
            "By default I do not call providers, use the network, or mutate files."
        )

    if "receipt" in normalized:
        return (
            "A receipt is a local proof record. It shows what was requested, what AION answered, "
            "whether the action stayed local, whether the network was used, whether mutation happened, "
            "and whether execution was performed."
        )

    if "governance" in normalized or "governed" in normalized:
        return (
            "Governance means the action is reviewed with visible boundaries and receipts before trust. "
            "In AION ICLI, governance is local-first and non-destructive by default."
        )

    return (
        "I can help review this locally first. I will keep network use, mutation, "
        "and execution off by default while preserving a receipt for later review."
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
    response = answer(prompt)
    receipt = write_receipt(prompt, response, mode="one_shot")
    print_exchange(prompt, response, receipt)
    return 0


def run_interactive() -> int:
    render_banner()
    print(yellow("Interactive Mode V1"))
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

        if prompt.lower() in ("exit", "quit", "/exit", "/quit"):
            response = "Session closed. Receipts remain local for review."
            receipt = write_receipt(prompt, response, mode="interactive")
            print("")
            print(cyan(f"AION     > {response}"))
            print(blue("Receipt  > ") + white(receipt))
            print("")
            return 0

        response = answer(prompt)
        receipt = write_receipt(prompt, response, mode="interactive")
        print("")
        print(cyan(f"AION     > {response}"))
        print("")
        print(blue("Boundary > ") + green("LOCAL_ONLY"))
        print(blue("Network  > ") + green("NOT_USED"))
        print(blue("Mutation > ") + green("NOT_PERFORMED"))
        print(blue("Receipt  > ") + white(receipt))
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
