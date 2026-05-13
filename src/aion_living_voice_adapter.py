import hashlib
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

ENGINE = "AION_LIVING_VOICE_ADAPTER_V1"
STYLES = ["direct", "reframe", "builder", "nonobvious", "plain"]


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9_]+", (text or "").lower())


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _style_scores(prompt: str) -> Dict[str, int]:
    q = " ".join(_tokenize(prompt))
    scores = {s: 0 for s in STYLES}

    builder_terms = ["build", "architecture", "system", "layer", "route", "design", "governance", "proof"]
    nonobvious_terms = ["genius", "brilliant", "non-obvious", "insight", "strategic"]
    reframe_terms = ["why", "really", "meaning", "underlying", "actually"]
    plain_terms = ["simple", "plain", "clear", "explain"]
    direct_terms = ["next", "do", "should", "now", "how"]

    for t in builder_terms:
        if t in q:
            scores["builder"] += 4
    for t in nonobvious_terms:
        if t in q:
            scores["nonobvious"] += 4
    for t in reframe_terms:
        if t in q:
            scores["reframe"] += 3
    for t in plain_terms:
        if t in q:
            scores["plain"] += 3
    for t in direct_terms:
        if t in q:
            scores["direct"] += 2

    scores["direct"] += 1
    return scores


def _pick_style(prompt: str) -> str:
    scores = _style_scores(prompt)
    ranked = sorted(scores.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return ranked[0][0]


def _continuity_line(memory_state: Dict[str, Any]) -> str:
    turns = memory_state.get("recent_turns", []) if isinstance(memory_state, dict) else []
    if not turns:
        return "Continuity note: starting from the current governed prompt context."
    last_prompt = str(turns[-1].get("prompt", "")).strip()
    if not last_prompt:
        return "Continuity note: starting from the current governed prompt context."
    return f"Continuity note: your previous turn was '{last_prompt[:80]}'."


def _truth_guard(prompt: str, draft: str) -> str:
    lower = prompt.lower()
    if any(x in lower for x in ["guarantee", "certain", "always"]):
        return draft + " I cannot guarantee outcomes; I can only provide governed, evidence-aware guidance."
    return draft


def _framed_answer(style: str, prompt: str, context: Dict[str, Any]) -> str:
    base_truth = "AION answers from governed continuity: boundary, controls, evidence, and consequences before style."
    uncertainty = "Where evidence is partial, I will mark uncertainty instead of pretending certainty."

    if style == "builder":
        return (
            "Builder framing: start from constraints, then choose the smallest admissible next move. "
            + base_truth
            + " "
            + uncertainty
        )
    if style == "reframe":
        return (
            "Reframe: the core question is not whether an action sounds smart; it is whether it is admissible before consequence. "
            + base_truth
            + " "
            + uncertainty
        )
    if style == "nonobvious":
        return (
            "Non-obvious insight: stronger governance constraints usually produce better strategic answers, not weaker ones. "
            + base_truth
            + " "
            + uncertainty
        )
    if style == "plain":
        return "Plain framing: provide artifact, controls, and verifier path first; then decide. " + uncertainty
    return "Direct framing: no artifact/no verifier means no trust escalation. " + uncertainty


def generate_living_voice_response(prompt: str, memory_state: Optional[Dict[str, Any]] = None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    memory_state = memory_state or {}
    context = context or {}

    style = _pick_style(prompt)
    continuity_line = _continuity_line(memory_state)
    draft = _framed_answer(style, prompt, context)
    if continuity_line:
        draft = continuity_line + " " + draft
    final = _truth_guard(prompt, draft)

    payload = {
        "engine": ENGINE,
        "generated_at_utc": _now(),
        "style": style,
        "adaptive_framing_active": True,
        "continuity_aware": bool(continuity_line),
        "memory_shaping_active": bool(memory_state.get("recent_turns")),
        "truth_preserving_language": True,
        "heuristic_confidence": "BOUNDED",
        "response": final,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
    }
    payload["response_hash"] = hashlib.sha256(final.encode("utf-8", errors="ignore")).hexdigest()
    return payload
