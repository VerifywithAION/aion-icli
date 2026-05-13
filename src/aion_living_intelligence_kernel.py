import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

try:
    from aion_dynamic_cognition_engine import analyze_dynamic_cognition
except Exception:
    analyze_dynamic_cognition = None

ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "living_intelligence"
ENGINE = "AION_LIVING_INTELLIGENCE_KERNEL_V1"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    tmp.replace(path)


def _tokens(text: str) -> List[str]:
    return re.findall(r"[a-z0-9_]+", (text or "").lower())


def _detect_intent(prompt: str) -> str:
    p = prompt.lower()
    if "ship" in p or "release" in p:
        return "release_admissibility"
    if "core truth" in p:
        return "truth_extraction"
    if "what am i missing" in p:
        return "gap_detection"
    if "next best question" in p:
        return "question_optimization"
    if "investigate" in p or "analyze" in p or "deep" in p:
        return "root_cause_investigation"
    return "governed_reflection"


def _hidden_assumptions(prompt: str) -> List[str]:
    p = prompt.lower()
    a: List[str] = []
    if "ship" in p:
        a.append("Assumes readiness can be claimed before verifier-backed admissibility evidence.")
    if "wallet" in p:
        a.append("Assumes signature/funds-at-risk paths can be trusted without explicit human-review gates.")
    if "wrong answers" in p:
        a.append("Assumes confidence correlates with truth under weak governance constraints.")
    if not a:
        a.append("Assumes style quality is equivalent to evidence quality.")
    return a


def _contradictions(prompt: str) -> List[str]:
    p = prompt.lower()
    c: List[str] = []
    if "ship" in p:
        c.append("Ready-to-ship claim conflicts with missing-control possibility (verifier/rollback/dry-run).")
    if "wrong answers" in p:
        c.append("High confidence can coexist with low evidence completeness.")
    if "toy" in p:
        c.append("Perceived capability may exceed proven end-to-end admissibility chain.")
    if not c:
        c.append("Evidence may be partial; certainty must remain bounded.")
    return c


def _root_cause(prompt: str) -> str:
    p = prompt.lower()
    if "wrong answers" in p:
        return "Root cause is governance-light inference: confidence emitted before contradiction/evidence gates finish." 
    if "toy" in p:
        return "Root cause is proof-surface thinness: chain exists, but visible end-to-end demonstrations may be underemphasized."
    return "Root cause is claim-evidence compression: statements are made faster than admissibility checks are communicated."


def _counterfactuals(prompt: str) -> List[str]:
    return [
        "If verifier + receipt gates were mandatory before any readiness claim, false positives would drop.",
        "If contradiction checks were surfaced first, confident-but-weak answers would be downgraded earlier.",
        "If proof graph gaps were shown inline, next steps would be clearer and safer.",
    ]


def _next_best_question(prompt: str) -> str:
    p = prompt.lower()
    if "ship" in p:
        return "Which verifier marker and receipt chain prove this is admissible, not just plausible?"
    if "toy" in p:
        return "Which missing proof surface, if added now, would most increase real admissibility confidence?"
    if "wrong answers" in p:
        return "At which governance gate did confidence outrun evidence, and what control closes that gap?"
    return "What is the single highest-leverage missing control blocking admissibility right now?"


def _dynamic_update(intent: str, contradictions: List[str]) -> str:
    return (
        f"Theory update: prioritize {intent} under contradiction-aware governance. "
        f"Current uncertainty remains bounded across {len(contradictions)} contradiction/uncertainty signal(s)."
    )


def analyze_living_request(prompt: str) -> Dict[str, Any]:
    dynamic = None
    if analyze_dynamic_cognition is not None:
        try:
            dynamic = analyze_dynamic_cognition(prompt, context={"caller": ENGINE})
        except Exception:
            dynamic = None

    intent = _detect_intent(prompt)
    assumptions = dynamic.get("hidden_assumptions") if isinstance(dynamic, dict) else _hidden_assumptions(prompt)
    contradictions = [dynamic.get("contradiction_pressure")] if isinstance(dynamic, dict) else _contradictions(prompt)
    root = dynamic.get("strongest_theory", {}).get("theory") if isinstance(dynamic, dict) else _root_cause(prompt)
    counterfactuals = (
        [x.get("theory") for x in dynamic.get("competing_theories", []) if isinstance(x, dict)]
        if isinstance(dynamic, dict)
        else _counterfactuals(prompt)
    )
    next_q = dynamic.get("next_best_question") if isinstance(dynamic, dict) else _next_best_question(prompt)
    update = _dynamic_update(intent, contradictions)

    direct_truth = (
        "Direct truth: admissibility is a governance property, not a style property; "
        "without verifier/evidence continuity, confidence is insufficient."
    )
    if isinstance(dynamic, dict):
        theory = dynamic.get("strongest_theory", {}).get("theory", "")
        if theory:
            direct_truth = "Direct truth: " + theory

    governed_answer = dynamic.get("governed_answer") if isinstance(dynamic, dict) else (
        "Governed answer: treat this as a constrained decision problem. "
        "Surface missing controls, downgrade claim certainty, and require verifier/receipt evidence before trust escalation."
    )
    if governed_answer and not governed_answer.lower().startswith("governed answer"):
        governed_answer = "Governed answer: " + governed_answer

    next_move = (
        "Next admissible move: run the matching verifier path, attach receipt evidence, "
        "and re-evaluate contradiction state before any execution or release claim."
    )

    result: Dict[str, Any] = {
        "engine": ENGINE,
        "generated_at_utc": _now(),
        "direct_truth": direct_truth,
        "detected_intent": intent,
        "hidden_assumptions": assumptions,
        "contradictions_or_uncertainties": contradictions,
        "root_cause_hypothesis": root,
        "counterfactuals": counterfactuals,
        "next_best_question": next_q,
        "dynamic_theory_update": update,
        "governed_answer": governed_answer,
        "nonobvious_insight": dynamic.get("nonobvious_insight") if isinstance(dynamic, dict) else "",
        "dynamic_reframe": dynamic.get("dynamic_reframe") if isinstance(dynamic, dict) else "",
        "continuity_update": dynamic.get("continuity_update") if isinstance(dynamic, dict) else "",
        "next_admissible_move": next_move,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }

    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    rid = f"aion_living_intel_{uuid.uuid4().hex[:12]}"
    stamp = _now()
    rel = Path("receipts") / "living_intelligence" / f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    abs_path = ROOT / rel
    receipt = {
        "receipt_type": "aion_living_intelligence_kernel_receipt_v1",
        "engine": ENGINE,
        "timestamp_utc": stamp,
        "prompt": prompt,
        "result": result,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }
    _atomic_write(abs_path, json.dumps(receipt, indent=2))

    result.update(
        {
            "receipt_id": rid,
            "receipt_path": str(rel).replace("\\", "/"),
            "receipt_abs_path": str(abs_path),
            "receipt_written": abs_path.exists(),
            "receipt_sha256": hashlib.sha256(abs_path.read_bytes()).hexdigest(),
            "repo_root": str(ROOT),
        }
    )
    return result


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="AION Living Intelligence Kernel V1")
    parser.add_argument("--input", required=True, help="Path to JSON file with {'prompt': '...'}")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    prompt = str(payload.get("prompt") or "").strip()
    print(json.dumps(analyze_living_request(prompt), indent=2))


if __name__ == "__main__":
    _cli()
