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


def configure_utf8() -> None:
    """Best-effort UTF-8 console hardening for Windows and cross-platform terminals."""
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


def write_receipt(prompt: str, response: str) -> str:
    receipt_dir = Path("receipts") / "local"
    receipt_dir.mkdir(parents=True, exist_ok=True)

    receipt_path = receipt_dir / "aion_cli_receipt_v1.json"

    receipt = {
        "receipt_type": "aion_cli_receipt_v1",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompt": prompt,
        "response": response,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "governance_tone": "felt_not_seen",
    }

    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return str(receipt_path)


def answer(prompt: str) -> str:
    normalized = (prompt or "").strip().lower()

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

    return (
        "I can help review this locally first. I will keep network use, mutation, "
        "and execution off by default while preserving a receipt for later review."
    )


def main(argv: list[str]) -> int:
    configure_utf8()

    prompt = " ".join(argv[1:]).strip()
    if not prompt:
        prompt = "Who are you, AION?"

    render_banner()

    response = answer(prompt)
    receipt = write_receipt(prompt, response)

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


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
