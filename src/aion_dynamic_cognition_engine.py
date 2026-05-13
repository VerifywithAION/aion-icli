import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
ENGINE = "AION_DYNAMIC_COGNITION_ENGINE_V1"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        f.flush()
    tmp.replace(path)


def _hidden_assumptions(prompt: str) -> List[str]:
    p = prompt.lower()
    out: List[str] = []
    if "alive" in p or "fake" in p:
        out.append("Assumes fluent language implies adaptive cognition.")
    if "ship" in p:
        out.append("Assumes feature completion is equivalent to admissible readiness.")
    if "models" in p:
        out.append("Assumes larger models remove the need for governance arbitration.")
    if not out:
        out.append("Assumes the visible question is the core bottleneck.")
    return out


def _theories(prompt: str) -> List[Dict[str, Any]]:
    p = prompt.lower()
    base = [
        {
            "theory": "Answer style is outrunning evidence-linked reasoning depth.",
            "plausibility": 0.84,
            "usefulness": 0.91,
            "reason": "Explains repetitive safe language with low strategic specificity.",
        },
        {
            "theory": "Competing hypotheses are not being explicitly ranked before final output.",
            "plausibility": 0.81,
            "usefulness": 0.89,
            "reason": "Without ranking, weaker frames leak into repetitive generalized responses.",
        },
        {
            "theory": "Contradiction pressure is detected but compressed into one default template.",
            "plausibility": 0.78,
            "usefulness": 0.88,
            "reason": "This produces consistent governance tone but weak adaptive voice variation.",
        },
    ]
    if "wallet" in p:
        base.append(
            {
                "theory": "Funds-at-risk paths are narrated as policy rather than causal consequence chains.",
                "plausibility": 0.76,
                "usefulness": 0.84,
                "reason": "Reduces strategic urgency in high-consequence decision framing.",
            }
        )
    if "fake" in p:
        base.append(
            {
                "theory": "The system hides uncertainty instead of using it to drive next-best-question selection.",
                "plausibility": 0.8,
                "usefulness": 0.9,
                "reason": "Truth-constrained systems feel alive when uncertainty is operationalized.",
            }
        )
    ranked = sorted(base, key=lambda x: x["plausibility"] + x["usefulness"], reverse=True)
    return ranked[:4]


def _next_question(prompt: str) -> str:
    p = prompt.lower()
    if "alive" in p:
        return "What contradiction would AION surface first if it optimized truth over fluency right now?"
    if "assumption" in p:
        return "Which protected assumption, if removed, would force a better architecture decision this week?"
    if "models" in p:
        return "At what gate does confidence bypass contradiction testing in your current pipeline?"
    if "fake" in p:
        return "What uncertainty is being suppressed to preserve a coherent but shallow answer?"
    return "Which proof-backed question would most reduce strategic uncertainty in the next build step?"


def analyze_dynamic_cognition(prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    context = context or {}
    theories = _theories(prompt)
    strongest = theories[0]
    rejected = [
        {
            "theory": theories[-1]["theory"],
            "rejection_reason": "Lower combined plausibility and usefulness than strongest theory.",
        }
    ]
    next_q = _next_question(prompt)
    p = prompt.lower()
    insight = (
        "AION feels fake when it answers the asked question but does not expose the governing tradeoff underneath it."
        if ("fake" in p or "alive" in p)
        else "The hidden blocker is usually arbitration quality between theories, not raw model capability."
    )
    reframe = (
        "Reframe from answer quality to decision quality under contradiction pressure and evidence constraints."
    )

    result: Dict[str, Any] = {
        "engine": ENGINE,
        "detected_surface_question": prompt.strip(),
        "inferred_hidden_goal": "governed_truth_inquiry",
        "hidden_assumptions": _hidden_assumptions(prompt),
        "competing_theories": theories,
        "strongest_theory": strongest,
        "rejected_theories": rejected,
        "contradiction_pressure": "High pressure between fluent outputs and admissible evidence chain requirements.",
        "nonobvious_insight": insight,
        "dynamic_reframe": reframe,
        "next_best_question": next_q,
        "governed_answer": (
            f"For this question ('{prompt.strip()[:60]}'), prioritize '{strongest['theory']}', expose its contradiction implications, "
            "and block execution until verifier-backed evidence closes the highest-risk gap."
        ),
        "continuity_update": (
            f"Carry forward strongest theory '{strongest['theory']}' and next question '{next_q}' for subsequent turns."
        ),
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }

    rid = f"aion_dynamic_cognition_{uuid.uuid4().hex[:12]}"
    stamp = _now()
    rel = Path("receipts") / "dynamic_cognition" / f"{stamp.replace(':', '').replace('-', '')}_{rid}.json"
    abs_path = ROOT / rel
    receipt = {
        "receipt_type": "aion_dynamic_cognition_receipt_v1",
        "engine": ENGINE,
        "timestamp_utc": stamp,
        "prompt": prompt,
        "context": context,
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

    parser = argparse.ArgumentParser(description="AION Dynamic Cognition Engine V1")
    parser.add_argument("--input", required=True, help="JSON path containing prompt/context")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    prompt = str(payload.get("prompt") or "").strip()
    context = payload.get("context") if isinstance(payload.get("context"), dict) else {}
    print(json.dumps(analyze_dynamic_cognition(prompt, context=context), indent=2))


if __name__ == "__main__":
    _cli()
