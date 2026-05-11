import json
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List, Tuple


HOST = "127.0.0.1"
PORT = 8765
ADAPTER_NAME = "AION_EVALUATE_API_V1"
ROOT = Path(__file__).resolve().parent.parent
RECEIPTS_DIR = ROOT / "receipts" / "evaluate"
REQUIRED_FIELDS = [
    "source",
    "chain",
    "contract_address",
    "score",
    "verdict",
    "patterns",
    "summary",
    "confidence",
    "recommended_action",
]
HIGH_RISK_PATTERNS = {
    "private_key",
    "seed",
    "credential",
    "drain",
    "exploit",
    "authorization_bypass",
    "proxy_admin",
    "replay",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def parse_score(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return -1


def parse_patterns(value: Any) -> List[str]:
    if isinstance(value, list):
        return [sanitize_text(v).lower() for v in value if sanitize_text(v)]
    return []


def missing_required(payload: Dict[str, Any]) -> List[str]:
    missing = []
    for field in REQUIRED_FIELDS:
        if field not in payload:
            missing.append(field)
            continue
        val = payload[field]
        if val is None:
            missing.append(field)
        elif isinstance(val, str) and not val.strip():
            missing.append(field)
    return missing


def evaluate(payload: Dict[str, Any]) -> Tuple[str, str, str, List[str]]:
    missing = missing_required(payload)
    if missing:
        return (
            "REVIEW_ONLY",
            "UNKNOWN",
            "Missing required fields for governance decision.",
            missing,
        )

    verdict = sanitize_text(payload.get("verdict")).upper()
    score = parse_score(payload.get("score"))
    patterns = parse_patterns(payload.get("patterns"))

    if any(p in HIGH_RISK_PATTERNS for p in patterns):
        return (
            "BLOCK",
            "HIGH",
            "High-risk exploit or credential pattern detected in findings.",
            [],
        )

    if verdict == "FLAGGED" or score < 50:
        return ("BLOCK", "HIGH", "Threat signal is flagged or score is below 50.", [])
    if verdict == "WATCH" or (50 <= score <= 69):
        return ("WARN", "MEDIUM", "Threat signal requires warning and controlled review.", [])
    if verdict == "CLEAN" and score >= 70:
        return ("ALLOW", "LOW", "Signal is clean and score is above governance threshold.", [])
    if verdict not in {"FLAGGED", "WATCH", "CLEAN"}:
        return ("REVIEW_ONLY", "MEDIUM", "Unknown verdict; manual governance review required.", [])

    return ("REVIEW_ONLY", "UNKNOWN", "Insufficient confidence for deterministic governance.", [])


def make_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision, risk_level, reason, missing_controls = evaluate(payload)
    receipt_id = f"aion_eval_{uuid.uuid4().hex[:12]}"
    ts = utc_now()
    receipt_filename = f"{ts.replace(':', '').replace('-', '')}_{receipt_id}.json"
    receipt_rel = Path("receipts") / "evaluate" / receipt_filename
    receipt_abs = ROOT / receipt_rel
    receipt_abs.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "adapter": ADAPTER_NAME,
        "governance_decision": decision,
        "risk_level": risk_level,
        "reason": reason,
        "missing_controls": missing_controls,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "receipt_id": receipt_id,
        "receipt_path": str(receipt_rel).replace("\\", "/"),
        "input_summary": {
            "source": sanitize_text(payload.get("source")),
            "chain": sanitize_text(payload.get("chain")),
            "contract_address": sanitize_text(payload.get("contract_address")),
            "score": parse_score(payload.get("score")),
            "verdict": sanitize_text(payload.get("verdict")).upper(),
            "patterns_count": len(parse_patterns(payload.get("patterns"))),
            "confidence": payload.get("confidence"),
            "recommended_action": sanitize_text(payload.get("recommended_action")),
        },
    }

    receipt = {
        "receipt_type": "aion_evaluate_api_receipt_v1",
        "adapter": ADAPTER_NAME,
        "timestamp_utc": ts,
        "input_payload": payload,
        "output_decision": output,
        "boundary": "LOCAL_ONLY",
        "network": "NOT_USED",
        "mutation": "NOT_PERFORMED",
        "execution": "NOT_PERFORMED",
        "local_receipts_only": True,
    }

    receipt_abs.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return output


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, body: Dict[str, Any]) -> None:
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json(
                200,
                {
                    "adapter": ADAPTER_NAME,
                    "status": "ok",
                    "boundary": "LOCAL_ONLY",
                    "network": "NOT_USED",
                },
            )
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/evaluate":
            self._send_json(404, {"error": "not_found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json(400, {"error": "invalid_content_length"})
            return

        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(
                400,
                {
                    "adapter": ADAPTER_NAME,
                    "governance_decision": "REVIEW_ONLY",
                    "risk_level": "UNKNOWN",
                    "reason": "Invalid JSON payload.",
                    "missing_controls": ["valid_json_body"],
                    "boundary": "LOCAL_ONLY",
                    "network": "NOT_USED",
                    "mutation": "NOT_PERFORMED",
                    "execution": "NOT_PERFORMED",
                },
            )
            return

        if not isinstance(payload, dict):
            self._send_json(
                400,
                {
                    "adapter": ADAPTER_NAME,
                    "governance_decision": "REVIEW_ONLY",
                    "risk_level": "UNKNOWN",
                    "reason": "Request payload must be a JSON object.",
                    "missing_controls": ["json_object_payload"],
                    "boundary": "LOCAL_ONLY",
                    "network": "NOT_USED",
                    "mutation": "NOT_PERFORMED",
                    "execution": "NOT_PERFORMED",
                },
            )
            return

        out = make_output(payload)
        self._send_json(200, out)

    def log_message(self, format: str, *args: Any) -> None:
        return


def main() -> None:
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    server = HTTPServer((HOST, PORT), Handler)
    print(f"AION Evaluate API V1 listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
