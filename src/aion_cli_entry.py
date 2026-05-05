import json
import os
import sys
from datetime import datetime, timezone


def force_utf8_stdio() -> None:
    """Keep Unicode banner stable under Windows pipes, redirected output, and CI."""
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


force_utf8_stdio()


AION_LOGO = r"""
█████╗ ██╗ ██████╗ ███╗   ██╗
██╔══██╗██║██╔═══██╗████╗  ██║
███████║██║██║   ██║██╔██╗ ██║
██╔══██║██║██║   ██║██║╚██╗██║
██║  ██║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
""".strip("\n")


def repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def receipt_path() -> str:
    return os.path.join(repo_root(), "receipts", "local", "aion_cli_receipt_v1.json")


def write_receipt(prompt: str, response: str) -> str:
    path = receipt_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    receipt = {
        "schema": "aion.icli.local_receipt.v1",
        "repo": "aion-icli",
        "status": "PASS",
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompt": prompt,
        "response_class": "LOCAL_GOVERNED_REPLY",
        "runtime_boundaries": {
            "offline_mode": True,
            "network_used": False,
            "external_api_called": False,
            "autonomous_execution_performed": False,
            "mutation_performed": False,
            "local_receipts_only": True,
        },
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    return os.path.relpath(path, repo_root())


def render_banner() -> None:
    print()
    print(AION_LOGO)
    print()
    print("AION ICLI")
    print("Interactive Command Line Intelligence")
    print("Governed Local Mode")
    print("Offline-capable by design")
    print("No external APIs by default")
    print()
    print("What I can do offline:")
    print("- Answer from local rules and local project context")
    print("- Evaluate actions before execution")
    print("- Produce receipts and proof traces")
    print("- Block unsafe or unproven operations")
    print("- Preserve evidence for replay and audit")
    print()


def answer(prompt: str) -> str:
    normalized = (prompt or "").strip().lower()

    if "who are you" in normalized:
        return (
            "I am not an LLM. I am a governed execution layer that can talk through this interface. "
            "I help evaluate actions, expose boundaries, produce receipts, and make proof visible before trust."
        )

    if normalized in ("/help", "help", "--help", "-h"):
        return (
            "Use AION ICLI to ask local governed questions. "
            "This public interface runs offline by default and produces a local receipt."
        )

    return "I can help. Rephrase with objective, constraints, and expected proof outcome."


def main(argv: list[str]) -> int:
    prompt = " ".join(argv[1:]).strip() if len(argv) > 1 else "Who are you, AION?"

    render_banner()

    if prompt:
        print(f"Operator > {prompt}")
        print()

    response = answer(prompt)
    print(f"AION     > {response}")
    print()

    rel_receipt = write_receipt(prompt, response)

    print("Boundary > LOCAL_ONLY")
    print("Network  > NOT_USED")
    print("Mutation > NOT_PERFORMED")
    print(f"Receipt  > {rel_receipt}")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))