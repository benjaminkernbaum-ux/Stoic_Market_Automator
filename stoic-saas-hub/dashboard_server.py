#!/usr/bin/env python3
"""
Stoic Market Dashboard – Backend Server
Zero external dependencies. Uses Python stdlib only.
Run:  python dashboard_server.py
Port: 8080
"""

import json
import random
import time
import math
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from urllib.parse import urlparse, parse_qs

PORT = 8080

# ──────────────────────────────────────────────────────────────────────────────
# Fake data generators (replace with real API calls as needed)
# ──────────────────────────────────────────────────────────────────────────────

def _jitter(base, pct=0.01):
    return round(base * (1 + random.uniform(-pct, pct)), 2)

def market_snapshot():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "assets": [
            {"symbol": "HK50",    "price": _jitter(16589.2, 0.005), "change_pct": round(random.uniform(-1.5, 2.0), 2)},
            {"symbol": "S&P 500", "price": _jitter(5088.8,  0.003), "change_pct": round(random.uniform(-0.8, 1.2), 2)},
            {"symbol": "NASDAQ",  "price": _jitter(17962.1, 0.004), "change_pct": round(random.uniform(-1.0, 2.0), 2)},
            {"symbol": "VIX",     "price": _jitter(13.45,   0.02),  "change_pct": round(random.uniform(-5.0, 5.0), 2)},
            {"symbol": "BTC/USD", "price": _jitter(62104.0, 0.01),  "change_pct": round(random.uniform(-3.0, 5.0), 2)},
            {"symbol": "XAU/USD", "price": _jitter(2034.5,  0.003), "change_pct": round(random.uniform(-0.5, 0.5), 2)},
        ]
    }

def signals():
    now = datetime.now(timezone.utc)
    return {
        "timestamp": now.isoformat(),
        "active_signals": [
            {
                "id": 1,
                "symbol": "HK50",
                "timeframe": "H1",
                "direction": "BUY",
                "entry": _jitter(16580.0),
                "sl": round(_jitter(16580.0) - 80, 1),
                "tp": round(_jitter(16580.0) + 160, 1),
                "checklist": {"historico": True, "hook": True, "cross_ema": True, "trend_ok": True},
                "age_minutes": random.randint(120, 360)
            },
            {
                "id": 2,
                "symbol": "BTCUSD",
                "timeframe": "H4",
                "direction": "SELL",
                "entry": _jitter(62100.0, 0.005),
                "sl": round(_jitter(62100.0, 0.005) + 800, 1),
                "tp": round(_jitter(62100.0, 0.005) - 1600, 1),
                "checklist": {"historico": True, "hook": True, "cross_ema": False, "trend_ok": True},
                "age_minutes": random.randint(240, 600)
            }
        ]
    }

def members_stats():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_members": 847 + random.randint(0, 3),
        "vip_members": 312 + random.randint(0, 2),
        "active_today": 203 + random.randint(-5, 5),
        "revenue_mrr": 30264.0 + round(random.uniform(-100, 100), 2),
        "growth_pct": round(random.uniform(2.1, 4.8), 1)
    }

def whatsapp_stats():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "messages_sent_today": random.randint(180, 250),
        "messages_delivered": random.randint(170, 245),
        "messages_read": random.randint(140, 200),
        "replies_received": random.randint(60, 100),
        "conversion_rate_pct": round(random.uniform(28.0, 45.0), 1),
        "pipeline_value": round(random.uniform(8000, 15000), 2)
    }

def wa_inbox():
    names = ["João Silva", "Marcos Andrade", "Amanda R.", "Carlos E.", "Fernanda Lima"]
    msgs = [
        "Quando é a próxima live?",
        "Quero assinar o plano VIP",
        "O indicador deu sinal agora?",
        "Consigo parcelar a assinatura?",
        "Qual é o WhatsApp do suporte?"
    ]
    inbox = []
    for i in range(5):
        inbox.append({
            "id": i + 1,
            "contact": names[i % len(names)],
            "phone": f"+55119{random.randint(10000000, 99999999)}",
            "message": msgs[i % len(msgs)],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": random.choice(["unread", "pending", "replied"])
        })
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "messages": inbox}

def wa_reply_status():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "queue_size": random.randint(0, 8),
        "auto_reply_active": True,
        "last_sent": datetime.now(timezone.utc).isoformat(),
        "ai_model": "GPT-4o",
        "avg_response_time_sec": round(random.uniform(3.0, 12.0), 1)
    }

def session_info():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": f"sess_{int(time.time())}",
        "user": "Benjamin",
        "role": "admin",
        "permissions": ["read", "write", "admin"],
        "expires_in_sec": 3600
    }

def dialer_stats():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "calls_made_today": random.randint(45, 80),
        "calls_answered": random.randint(30, 60),
        "avg_duration_sec": random.randint(90, 300),
        "conversions_today": random.randint(5, 15),
        "pipeline_added": round(random.uniform(3000, 8000), 2)
    }

def status_check():
    return {
        "status": "ok",
        "service": "Stoic Market Dashboard Backend",
        "version": "1.0.0",
        "uptime_sec": int(time.time() - START_TIME),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

START_TIME = time.time()

# ──────────────────────────────────────────────────────────────────────────────
# Route table
# ──────────────────────────────────────────────────────────────────────────────

ROUTES = {
    "/api/status":         status_check,
    "/api/market":         market_snapshot,
    "/api/signals":        signals,
    "/api/members":        members_stats,
    "/api/whatsapp_stats": whatsapp_stats,
    "/api/wa_inbox":       wa_inbox,
    "/api/wa_reply_status":wa_reply_status,
    "/api/session":        session_info,
    "/api/dialer_stats":   dialer_stats,
}

# ──────────────────────────────────────────────────────────────────────────────
# HTTP Handler
# ──────────────────────────────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] {fmt % args}")

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        handler_fn = ROUTES.get(path)
        if handler_fn:
            self._send_json(handler_fn())
        elif path == "/":
            self._send_json({"message": "Stoic Market API", "endpoints": list(ROUTES.keys())})
        else:
            self._send_json({"error": "Not found", "path": path}, status=404)

    def do_POST(self):
        # For future webhook endpoints
        self.do_GET()


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"""
╔══════════════════════════════════════════════════════╗
║  🗿 Stoic Market Dashboard Backend                   ║
║  Listening on http://localhost:{PORT}                  ║
║  Press Ctrl+C to stop                               ║
╚══════════════════════════════════════════════════════╝
Available endpoints:""")
    for route in ROUTES:
        print(f"  GET http://localhost:{PORT}{route}")
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[Backend] Shutting down...")
        server.server_close()
