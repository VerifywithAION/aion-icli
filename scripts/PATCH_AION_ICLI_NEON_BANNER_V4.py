from pathlib import Path

path = Path("src/aion_cli_entry.py")
text = path.read_text(encoding="utf-8-sig")

insert_after = 'AION_LOGO = r"""'
if "AION_NEON_LOGO" in text:
    print("NEON_ALREADY_PRESENT")
else:
    marker = '""".strip("\\n")\n\nMEMORY_SCARS = ['
    idx = text.find(marker)
    if idx == -1:
        raise SystemExit("Could not find AION_LOGO end marker")

    helpers = r'''
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

MEMORY_SCARS = ['''

    text = text[:idx] + helpers + text[idx + len(marker):]

old_banner = '''def render_banner():
    print("")
    print(AION_LOGO)
    print("")
    print("AION ICLI")
    print("Interactive Command Line Intelligence")
    print("Governed Local Mode")
    print("Offline-capable by design")
    print("No external APIs by default")
    print("")
    print("What I can do offline:")
    print("- Answer from local rules and local project context")
    print("- Evaluate actions before execution")
    print("- Produce receipts and proof traces")
    print("- Keep risky actions in review mode before execution")
    print("- Preserve evidence for replay and audit")
    print("")
'''

new_banner = '''def render_banner():
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
'''

if old_banner not in text:
    raise SystemExit("Could not find original render_banner block")

text = text.replace(old_banner, new_banner, 1)
path.write_text(text, encoding="utf-8")
print("PATCH_OK")
