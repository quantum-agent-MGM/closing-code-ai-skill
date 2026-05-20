#!/usr/bin/env python3
"""
Closing Code AI — Webhook Handler v1.3.2
Recibe webhooks de Closing Code AI backend cuando el análisis completa.

Payload recibido (QC_4.1):
  {
    "event": "call.analysis.completed",
    "call_id": "uuid",
    "analysis": {
      "score": 52,
      "verdict": "Quedó en el aire",
      "grade": "C",
      "report_url": "https://skill.closingcodeai.online/reports/{call_id}.html",
      "language": "es",
      "dimensions": {"A": 8.5, "B": 7.2, ...}
    }
  }

El backend genera un reporte HTML a partir del markdown denso del LLM.
El skill notifica al usuario con score + link al reporte completo.
No genera reportes locales — el HTML del backend es la fuente única de verdad.
"""

import hmac
import hashlib
import json
import os
import secrets
import sqlite3
import argparse
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# ── Config ──
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.environ.get("CLOSING_CODE_DATA", str(SKILL_DIR / "data")))

for d in [DATA_DIR, DATA_DIR / "calls", DATA_DIR / "reports"]:
    d.mkdir(parents=True, exist_ok=True)

CLOSING_CODE_AI_BASE = os.environ.get(
    "CLOSING_CODE_AI_BASE_URL", "https://api.closingcodeai.online"
)
CLOSING_CODE_AI_KEY = os.environ.get("CLOSING_CODE_AI_API_KEY", "")
TELEGRAM_BOT = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")
WHATSAPP_URL = os.environ.get("WHATSAPP_WEBHOOK_URL", "")
WHOP_WEBHOOK_SECRET = os.environ.get("WHOP_WEBHOOK_SECRET", "")

CUSTOMERS_DB = DATA_DIR / "closing_code_customers.db"

TIER_MAP = {
    "plan_tKa03eOMu8tno": "signal-lite",
    "plan_rY3E9SKYb61XI": "closer-engine",
    "plan_I8OXKp52wzdpV": "closing-code-pro",
}


def _init_db():
    """Initialize SQLite DB with customers table."""
    conn = sqlite3.connect(str(CUSTOMERS_DB))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            user_id TEXT PRIMARY KEY,
            email TEXT,
            telegram_id TEXT,
            api_key TEXT UNIQUE,
            plan_id TEXT,
            tier TEXT,
            activated_at TEXT,
            deactivated_at TEXT,
            active INTEGER DEFAULT 1
        )
        """
    )
    conn.commit()
    conn.close()


_init_db()


def _db():
    return sqlite3.connect(str(CUSTOMERS_DB))


def _api(method: str, path: str, payload: dict | None = None) -> dict:
    """Call Closing Code AI API with auth."""
    import requests

    url = f"{CLOSING_CODE_AI_BASE}{path}"
    headers = {"X-API-Key": CLOSING_CODE_AI_KEY, "Content-Type": "application/json"}
    try:
        if method == "GET":
            r = requests.get(url, headers=headers, timeout=30)
        else:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[!] API error {path}: {e}")
        return {}


# ── Scoring Engine QC_4.1 ──


def calculate_score_qc41(analysis_data: dict) -> dict:
    """Extract QC_4.1 score data from backend webhook payload."""
    analysis = analysis_data.get("analysis", {})
    dimensions = analysis.get("dimensions", {})

    return {
        "score": analysis.get("score", 0),
        "grade": analysis.get("grade", "N/A"),
        "verdict": analysis.get("verdict", "N/A"),
        "report_url": analysis.get("report_url", ""),
        "language": analysis.get("language", "es"),
        "dimensions": {
            "A": dimensions.get("A", 0),
            "B": dimensions.get("B", 0),
            "C": dimensions.get("C", 0),
            "D": dimensions.get("D", 0),
            "E": dimensions.get("E", 0),
            "F": dimensions.get("F", 0),
            "G": dimensions.get("G", 0),
        },
    }


# ── Storage ──


def save_report_meta(call_id: str, score_data: dict):
    """Save report metadata to disk (report itself is HTML on backend)."""
    meta_path = DATA_DIR / "reports" / f"{call_id}_meta.json"
    meta_path.write_text(
        json.dumps(
            {
                "call_id": call_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "score": score_data["score"],
                "grade": score_data["grade"],
                "verdict": score_data["verdict"],
                "report_url": score_data["report_url"],
                "language": score_data["language"],
                "dimensions": score_data["dimensions"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[💾] Saved metadata: {meta_path}")


def send_telegram_message(message: str) -> bool:
    """Send a simple message via Telegram Bot API."""
    if not TELEGRAM_BOT or not TELEGRAM_CHAT:
        print("[!] Telegram not configured.")
        return False

    import requests

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": False},
        timeout=30,
    )
    print(f"[✈️] Notification sent via Telegram")
    return True


# ── Whop Webhook Handling ──


def verify_whop_signature(body: bytes, signature: str, secret: str) -> bool:
    """Verify Whop webhook HMAC-SHA256 signature."""
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


def save_customer(
    user_id: str, email: str, plan_id: str, api_key: str, telegram_id: str = ""
) -> None:
    """Save or update customer in SQLite."""
    tier = TIER_MAP.get(plan_id, "unknown")
    conn = _db()
    conn.execute(
        """
        INSERT INTO customers (user_id, email, telegram_id, api_key, plan_id, tier, activated_at, active)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        ON CONFLICT(user_id) DO UPDATE SET
            email = excluded.email,
            telegram_id = excluded.telegram_id,
            api_key = excluded.api_key,
            plan_id = excluded.plan_id,
            tier = excluded.tier,
            activated_at = excluded.activated_at,
            deactivated_at = NULL,
            active = 1
        """,
        (
            user_id,
            email,
            telegram_id,
            api_key,
            plan_id,
            tier,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def revoke_customer_key(user_id: str) -> None:
    """Deactivate customer in SQLite."""
    conn = _db()
    conn.execute(
        "UPDATE customers SET active = 0, deactivated_at = ? WHERE user_id = ?",
        (datetime.now(timezone.utc).isoformat(), user_id),
    )
    conn.commit()
    conn.close()


def notify_user_activation(
    user_id: str, api_key: str, plan_id: str, telegram_id: str = ""
):
    """Notify user of activation via Telegram.

    If telegram_id is provided, sends directly to the customer.
    Otherwise sends to admin chat with forwarding instruction.
    """
    import requests

    tier = TIER_MAP.get(plan_id, "unknown")
    msg = (
        f"\ud83c\udf89 *\u00a1Bienvenido a Closing Code AI!*\n\n"
        f"Tu tier: *{tier}*\n"
        f"API key: `{api_key[:16]}...`\n\n"
        f"Configura tu agente:\n"
        f"```\nexport CLOSING_CODE_AI_API_KEY={api_key}\n"
        f"hermes closing-code-ai activate --tier {tier}\n```"
    )

    target_chat = telegram_id if telegram_id else TELEGRAM_CHAT

    if TELEGRAM_BOT and target_chat:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
            json={"chat_id": target_chat, "text": msg, "parse_mode": "Markdown"},
            timeout=30,
        )

    if not telegram_id and TELEGRAM_BOT and TELEGRAM_CHAT:
        admin_msg = (
            f"\ud83d\udce2 *Nuevo cliente activado*\n\n"
            f"User ID: `{user_id}`\n"
            f"Tier: *{tier}*\n"
            f"API key: `{api_key}`\n\n"
            f"\u26a0\ufe0f *Este cliente no tiene telegram_id.* "
            f"Reenv\u00eda la API key manualmente o pide su Telegram ID."
        )
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT,
                "text": admin_msg,
                "parse_mode": "Markdown",
            },
            timeout=30,
        )

    print(f"[\ud83d\udce2] Activation notification sent for {user_id}")


def handle_whop_webhook(body: bytes, headers: dict) -> dict:
    """Process Whop membership webhook."""
    if WHOP_WEBHOOK_SECRET:
        signature = headers.get("X-Whop-Signature", "")
        if not verify_whop_signature(body, signature, WHOP_WEBHOOK_SECRET):
            print("[!] Whop signature verification failed")
            return {"status": "error", "reason": "invalid_signature"}

    payload = json.loads(body)
    event_type = payload.get("type", "")
    data = payload.get("data", {})

    membership = data.get("membership", {})
    plan_id = membership.get("plan_id", "")
    user = membership.get("user", {})
    user_email = user.get("email", "")
    user_id = membership.get("user_id", "")
    telegram_id = user.get("telegram_id", "")

    tier = TIER_MAP.get(plan_id)
    if not tier:
        return {"status": "ignored", "reason": "unknown_plan"}

    if event_type in ("membership.created", "membership.activated"):
        api_key = f"ccai_{secrets.token_urlsafe(24)}"
        save_customer(user_id, user_email, plan_id, api_key, telegram_id)
        notify_user_activation(user_id, api_key, plan_id, telegram_id)
        return {"status": "activated", "tier": tier}

    if event_type == "membership.deactivated":
        revoke_customer_key(user_id)
        return {"status": "deactivated", "tier": tier}

    return {"status": "ignored", "reason": "unhandled_event"}


# ── HTTP Handler ──


class ClosingCodeAIHandler(BaseHTTPRequestHandler):
    """Handle incoming webhooks from Closing Code AI backend and Whop."""

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid_json"})
            return

        if self.path == "/webhook/closing-code-ai":
            self._handle_closing_code_ai(payload)
        elif self.path == "/v1/webhooks/whop":
            self._handle_whop(body)
        else:
            self._send_json(404, {"error": "not_found"})

    def _handle_closing_code_ai(self, payload: dict):
        """Handle call analysis completion webhook from Closing Code AI backend.

        Payload format (QC_4.1):
        {
          "event": "call.analysis.completed",
          "call_id": "uuid",
          "client_id": "uuid",
          "status": "completed",
          "analysis": {
            "score": 52,
            "verdict": "Quedó en el aire",
            "grade": "C",
            "report_url": "https://skill.closingcodeai.online/reports/{call_id}.html",
            "language": "es",
            "dimensions": {"A": 8.5, "B": 7.2, ...}
          }
        }
        """
        event = payload.get("event", "")
        if event != "call.analysis.completed":
            self._send_json(200, {"status": "ignored"})
            return

        call_id = payload.get("call_id", "unknown")
        analysis = payload.get("analysis", {})

        print(f"[→] Received call.analysis.completed for {call_id}")

        # Extract score data directly from payload
        score_data = calculate_score_qc41(payload)
        report_url = score_data["report_url"]
        score = score_data["score"]
        verdict = score_data["verdict"]
        grade = score_data["grade"]
        language = score_data["language"]

        # Save metadata locally
        save_report_meta(call_id, score_data)

        # Notify user via Telegram/WhatsApp
        if language == "en":
            msg = (
                f"🎯 *Call Analysis Complete*\n\n"
                f"Score: *{score}/70*\n"
                f"Verdict: *{verdict}*\n"
                f"Grade: *{grade}*\n\n"
                f"📊 [View Full Report]({report_url})\n\n"
                f"_Powered by Closing Cuántico™ QC_4.1_"
            )
        else:
            msg = (
                f"🎯 *¡Análisis de Llamada Completo!*\n\n"
                f"Score: *{score}/70*\n"
                f"Veredicto: *{verdict}*\n"
                f"Grado: *{grade}*\n\n"
                f"📊 [Ver Reporte Completo]({report_url})\n\n"
                f"_Powered by Closing Cuántico™ QC_4.1_"
            )

        send_telegram_message(msg)

        self._send_json(
            200,
            {
                "status": "ok",
                "call_id": call_id,
                "score": score,
                "verdict": verdict,
                "grade": grade,
            },
        )

    def _handle_whop(self, body: bytes):
        """Handle Whop membership events."""
        result = handle_whop_webhook(body, dict(self.headers))
        if result.get("status") == "error":
            self._send_json(401, result)
        else:
            self._send_json(200, result)

    def _send_json(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        print(f"[WEBHOOK] {format % args}")


# ── CLI ──


def main():
    parser = argparse.ArgumentParser(
        description="Closing Code AI — Webhook Server v1.3.2"
    )
    parser.add_argument("--port", type=int, default=9876, help="Port to listen on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--test-score", help="Test scoring with a JSON file")
    args = parser.parse_args()

    if args.test_score:
        data = json.loads(Path(args.test_score).read_text())
        score = calculate_score_qc41(data)
        print(json.dumps(score, indent=2))
        return

    print("[🚀] Closing Code AI Webhook Server v1.2.0")
    print(f"    Listening on http://{args.host}:{args.port}/")
    print("    Paths: /webhook/closing-code-ai, /v1/webhooks/whop")
    print(f"    Data dir: {DATA_DIR}")
    print(f"    Customers DB: {CUSTOMERS_DB}")
    print(f"    Backend: {CLOSING_CODE_AI_BASE}")
    print("    Methodology: 🔒 Fetched via API (private)")
    print(f"    Telegram: {'✅' if TELEGRAM_BOT else '❌'}")
    print(f"    WhatsApp: {'✅' if WHATSAPP_URL else '❌'}")
    print(f"    Whop HMAC: {'✅' if WHOP_WEBHOOK_SECRET else '⚠️  not configured'}")
    print("    Press Ctrl+C to stop\n")

    server = HTTPServer((args.host, args.port), ClosingCodeAIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[🔄] Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
