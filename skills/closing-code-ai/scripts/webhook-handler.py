#!/usr/bin/env python3
"""
Closing Code AI — Webhook Handler v1.1.0
Recibe webhooks de Closing Code AI, genera reporte con score QC_4.0 (0-70),
y envía por Telegram/WhatsApp. La metodología se obtiene vía API privada.
"""

import os
import sys
import json
import datetime
import argparse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

# ── Config ──
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = Path(os.environ.get("CLOSING_CODE_DATA", str(SKILL_DIR / "data")))

for d in [DATA_DIR, DATA_DIR / "calls", DATA_DIR / "reports"]:
    d.mkdir(parents=True, exist_ok=True)

CLOSING_CODE_AI_BASE = os.environ.get("CLOSING_CODE_AI_BASE_URL", "https://api.closingcodeai.online")
CLOSING_CODE_AI_KEY = os.environ.get("CLOSING_CODE_AI_API_KEY", "")
TELEGRAM_BOT = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.environ.get("TELEGRAM_CHAT_ID", "")
WHATSAPP_URL = os.environ.get("WHATSAPP_WEBHOOK_URL", "")


def _api(method: str, path: str, payload: dict = None) -> dict:
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


def fetch_methodology() -> dict:
    """Fetch Closing Cuántico methodology from private backend."""
    if not CLOSING_CODE_AI_KEY:
        print("[!] No CLOSING_CODE_AI_API_KEY — cannot fetch methodology")
        return {}
    return _api("GET", "/v1/methodology/closing-cuantico")


def fetch_scoring_rubric() -> dict:
    """Fetch scoring rubric from private backend."""
    if not CLOSING_CODE_AI_KEY:
        return {}
    return _api("GET", "/v1/methodology/scoring-rubric")


# ── Scoring Engine QC_4.0 ──

def calculate_score_qc40(analysis_data: dict) -> dict:
    """Calculate QC_4.0 score (0-70) from Closing Code AI analysis output."""
    qc = analysis_data.get("qc_analysis", {})
    scores = qc.get("scores", {})
    
    # Dimensiones A-F (0-10 cada una)
    score_a = scores.get("A_gravedad_cero", 0)
    score_b = scores.get("B_arquitectura", 0)
    score_c = scores.get("C_escaneo_core", 0)
    score_d = scores.get("D_diagnostico_tridimensional", 0)
    score_e = scores.get("E_errores_inverso", 0)
    score_f = scores.get("F_absorcion_friccion", 0)
    score_g = scores.get("G_no_cierre", 0)
    
    total = score_a + score_b + score_c + score_d + score_e + score_f + score_g
    
    # Grado
    if total >= 60:
        grade = "🟢 Excelente"
        veredicto = "PROCESO_CORRECTO_CON_SISTEMA"
    elif total >= 45:
        grade = "🟡 Buena"
        veredicto = "PROCESO_CORRECTO_SIN_CIERRE"
    elif total >= 28:
        grade = "🟠 Necesita trabajo"
        veredicto = "PROCESO_CON_ERRORES"
    else:
        grade = "🔴 Débil"
        veredicto = "PROCESO_DESCONECTADO"
    
    return {
        "score": total,
        "grade": grade,
        "veredicto": veredicto,
        "dimensions": {
            "A": score_a, "B": score_b, "C": score_c,
            "D": score_d, "E": score_e, "F": score_f, "G": score_g,
        },
    }


# ── Report Generation ──

def generate_report(call_data: dict, score_data: dict, methodology: dict) -> str:
    """Generate structured Markdown report from Closing Code AI QC_4.0 data."""
    
    prospect = call_data.get("prospect", {})
    closer = call_data.get("closer", {})
    analysis = call_data.get("analysis", {})
    qc = analysis.get("qc_analysis", {})
    profiling = qc.get("profiling", {})
    audit = qc.get("audit", {})
    training = qc.get("training", {})
    mission = qc.get("mission", {})
    
    scores = score_data["dimensions"]
    
    # Arquetipo info
    arquetipo = profiling.get("friction_profile", "Desconocido")
    arquetipo_map = {
        "Tiburon": ("🦈", "Tiburón", "Confrontativo, interrumpe, ego explícito"),
        "Pez_Globo": ("🐡", "Pez Globo", "Escéptico, pide pruebas, teme equivocarse"),
        "Delfin": ("🐬", "Delfín", "Hablador, social, se desvía"),
        "Ostra": ("🦪", "Ostra", "Tímido, monosílabos, cede fácil"),
    }
    emoji, nombre, desc = arquetipo_map.get(arquetipo, ("❓", arquetipo, ""))
    
    # Sistema de cierre
    sistema = audit.get("correct_closing_system", "Desconocido")
    
    # Predicción 48h (momento wow)
    predicciones = {
        "Tiburon": "Pedirá más información, comparará con 2 competidores, y decidirá que 'necesita pensarlo'.",
        "Pez_Globo": "Investigará en Google, leerá 3 reseñas negativas, y concluirá que 'es muy bueno para ser verdad'.",
        "Delfin": "Contará a 5 amigos, 3 dirán 'suena bien', 2 dirán 'cuidado', y nunca decidirá.",
        "Ostra": "Dirá 'sí' a todo, nunca pagará, y dejará de responder en 72 horas.",
    }
    prediccion = predicciones.get(arquetipo, "Perderá interés gradualmente sin decisión concreta.")
    
    # Por qué falló
    fallos = {
        "Tiburon": "Usaste lógica en vez de takeaway. El Tiburón respeta autoridad, no argumentos.",
        "Pez_Globo": "No mostraste evidencia. El Pez Globo no compra con palabras, compra con pruebas.",
        "Delfin": "Perdiste control de la conversación. El Delfín necesita que le cortes amablemente.",
        "Ostra": "Fuerzaste el cierre. La Ostra necesita tiempo y confianza, no presión.",
    }
    porque_fallo = fallos.get(arquetipo, "El enfoque no calibró con el perfil de fricción del prospecto.")
    
    # Pecados
    pecados = audit.get("critical_errors", [])
    pecados_md = ""
    for p in pecados[:5]:
        pecados_md += f"\n**[#{p.get('error_number', '?')}] {p.get('error_code', '').replace('_', ' ')}** — [{p.get('timestamp', '??:??')}]\n"
        pecados_md += f"- Evidencia: \"{p.get('evidence', '')}\"\n"
    if not pecados_md:
        pecados_md = "_¡Sin pecados capitales detectados! 🎉_\n"
    
    # Agujeros negros
    agujeros = audit.get("black_holes_detected", [])
    agujeros_md = "\n".join(f"- {a}" for a in agujeros) if agujeros else "_Sin agujeros negros detectados._\n"
    
    # Fortalezas
    strengths = analysis.get("strengths", [])
    strengths_md = "\n".join(f"- {s}" for s in strengths[:5]) if strengths else "_Sin fortalezas destacadas._\n"
    
    # Follow-up
    followup = training.get("closing_script", "")
    if not followup:
        followup = f"Email: Hola {prospect.get('name', '')}, gracias por tu tiempo. ¿Podemos agendar la demo para esta semana?"
    
    # Colapso
    colapso = training.get("recommended_closing_system", "")
    
    # Acciones
    acciones = [
        f"Practicar sistema: {sistema}",
        f"Estudiar colapso: {colapso}",
        "Revisar Pecado #1 (certeza tonal) en grabaciones pasadas",
    ]
    acciones_md = "\n".join(f"{i+1}. {a}" for i, a in enumerate(acciones))
    
    # Historial
    history = call_data.get("history", {})
    avg_score = history.get("avg_score", score_data["score"])
    best_score = history.get("best_score", score_data["score"])
    trend = "⬆️ Mejorando" if score_data["score"] > avg_score + 5 else "⬇️ Bajando" if score_data["score"] < avg_score - 5 else "➡️ Estable"
    
    report = f"""# 🎙️ Sales Call Analysis Report — Closing Code AI

**Closer**: {closer.get('name', 'N/A')}  
**Prospect**: {prospect.get('name', 'N/A')}  
**Empresa**: {prospect.get('company', 'N/A')}  
**Fecha**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | **Score**: {score_data['score']}/70 | **Grado**: {score_data['grade']} | **Veredicto**: {score_data['veredicto']}

---

## 🎯 Resumen Ejecutivo
{analysis.get('summary', 'Análisis completado vía Closing Code AI backend.')}

## 📊 Score Cuántico por Dimensión
| Dimensión | Score | Máximo | Ponderado |
|---|---|---|---|
| A — Gravedad Cero | {scores['A']}/10 | 10 | {scores['A']} |
| B — Arquitectura (6 Pasos) | {scores['B']}/10 | 10 | {scores['B']} |
| C — Escaneo Core (Nivel Dolor) | {scores['C']}/10 | 10 | {scores['C']} |
| D — Diagnóstico Tridimensional | {scores['D']}/10 | 10 | {scores['D']} |
| E — Errores Inverso (12 Pecados) | {scores['E']}/10 | 10 | {scores['E']} |
| F — Absorción de Fricción | {scores['F']}/10 | 10 | {scores['F']} |
| G — No Cierre (Ética) | {scores['G']}/10 | 10 | {scores['G']} |
| **TOTAL** | **{score_data['score']}**/70 | 70 | |

## 👤 Perfilado del Prospecto
| Eje | Perfil Detectado |
|---|---|
| **Fricción** | {arquetipo} — {desc} |
| **Decisión** | {profiling.get('decision_profile', 'N/A')} |
| **Monetario** | {profiling.get('monetary_profile', 'N/A')} |
| **Nivel de Dolor Alcanzado** | {profiling.get('core_level_name', 'N/A')} (Nivel {profiling.get('core_level_reached', 0)}) |
| **Sistema de Cierre Recomendado** | {sistema} |

## 😱 Momento WOW — ¿Cómo supimos esto?

> **Arquetipo detectado:** {emoji} **{nombre}**
>
> **Lo que este prospecto hará en las próximas 48h si no cierras hoy:**
> > "{prediccion}"
>
> **El único sistema que funciona con este arquetipo:**
> > **{sistema}** — Score mínimo requerido: 45/70
>
> **Por qué falló tu enfoque actual:**
> > {porque_fallo}

---

## ⚠️ Los 12 Pecados Capitales
{pecados_md}

## 🕳 Agujeros Negros
{agujeros_md}

## ✅ Lo Que Hiciste Bien
{strengths_md}

## 📝 Brief de Follow-up

**Email/WhatsApp (enviar en 2h):**

{followup}

**Sistema de cierre a practicar:** {sistema}

## 📈 Comparativa vs Historial
- Tu promedio: {avg_score}/70
- Tu mejor llamada: {best_score}/70
- Tendencia: {trend}

## 🎯 Acciones para la Próxima Llamada
{acciones_md}

## 🎯 Colapso de Realidad Recomendado
**{colapso}**

{training.get('socratic_question', '')}

---

*Generado por Closing Code AI — Closer Engine*
*Metodología: Closing Cuántico™ QC_4_0*
*Confidencial — solo para uso del closer y su manager*
"""
    return report


# ── Delivery ──

def send_telegram(report: str, call_id: str, score: int):
    """Send report via Telegram Bot API."""
    if not TELEGRAM_BOT or not TELEGRAM_CHAT:
        print("[!] Telegram not configured.")
        return False
    
    import requests
    
    header = f"🎙️ *Sales Call Analysis*\n📊 Score: *{score}/70*\n🆔 `{call_id}`"
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT, "text": header, "parse_mode": "Markdown"},
        timeout=30
    )
    
    chunks = [report[i:i+4000] for i in range(0, len(report), 4000)]
    for chunk in chunks:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT, "text": chunk, "parse_mode": "Markdown"},
            timeout=30
        )
    
    print(f"[✈️] Report sent via Telegram to chat {TELEGRAM_CHAT}")
    return True


def send_whatsapp(report: str, phone: str):
    """Send report via WhatsApp webhook."""
    if not WHATSAPP_URL:
        print("[!] WhatsApp not configured.")
        return False
    
    import requests
    summary = report[:500] + "..." if len(report) > 500 else report
    
    requests.post(WHATSAPP_URL, json={
        "to": phone,
        "message": f"🎙️ Sales Call Analysis\n\n{summary}\n\nVer reporte completo en tu dashboard."
    }, timeout=30)
    
    print(f"[✈️] WhatsApp notification sent to {phone}")
    return True


# ── Storage ──

def save_report(call_id: str, report: str, score_data: dict):
    """Save report and metadata to disk."""
    report_path = DATA_DIR / "reports" / f"{call_id}.md"
    meta_path = DATA_DIR / "reports" / f"{call_id}_meta.json"
    
    report_path.write_text(report, encoding="utf-8")
    meta_path.write_text(json.dumps({
        "call_id": call_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "score": score_data["score"],
        "grade": score_data["grade"],
        "veredicto": score_data["veredicto"],
        "dimensions": score_data["dimensions"],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"[💾] Saved: {report_path}")


# ── HTTP Handler ──

class ClosingCodeAIHandler(BaseHTTPRequestHandler):
    """Handle incoming webhooks from Closing Code AI."""
    
    def do_POST(self):
        if self.path != "/webhook/closing-code-ai":
            self.send_response(404)
            self.end_headers()
            return
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
        
        event = payload.get("event", "")
        if event != "call.analysis.completed":
            self.send_response(200)
            self.end_headers()
            return
        
        call_data = payload.get("data", {})
        call_id = call_data.get("call_id", "unknown")
        
        print(f"[→] Received webhook for call {call_id}")
        
        # Fetch methodology from private backend
        methodology = fetch_methodology()
        if not methodology:
            print("[!] Cannot fetch methodology — API key invalid or backend unreachable")
            self.send_response(503)
            self.end_headers()
            return
        
        # Calculate QC_4.0 score
        score_data = calculate_score_qc40(call_data.get("analysis", {}))
        
        # Generate report
        report = generate_report(call_data, score_data, methodology)
        
        # Save
        save_report(call_id, report, score_data)
        
        # Deliver
        closer_phone = call_data.get("closer", {}).get("phone", "")
        send_telegram(report, call_id, score_data["score"])
        if closer_phone:
            send_whatsapp(report, closer_phone)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ok",
            "call_id": call_id,
            "score": score_data["score"],
            "grade": score_data["grade"],
        }).encode())
    
    def log_message(self, format, *args):
        print(f"[WEBHOOK] {format % args}")


# ── CLI ──

def main():
    parser = argparse.ArgumentParser(description="Closing Code AI — Webhook Server")
    parser.add_argument("--port", type=int, default=9876, help="Port to listen on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--test-score", help="Test scoring with a JSON file")
    args = parser.parse_args()
    
    if args.test_score:
        data = json.loads(Path(args.test_score).read_text())
        score = calculate_score_qc40(data)
        print(json.dumps(score, indent=2))
        return
    
    print(f"[🚀] Closing Code AI Webhook Server v1.1.0")
    print(f"    Listening on http://{args.host}:{args.port}/webhook/closing-code-ai")
    print(f"    Data dir: {DATA_DIR}")
    print(f"    Backend: {CLOSING_CODE_AI_BASE}")
    print(f"    Methodology: 🔒 Fetched via API (private)")
    print(f"    Telegram: {'✅' if TELEGRAM_BOT else '❌'}")
    print(f"    WhatsApp: {'✅' if WHATSAPP_URL else '❌'}")
    print(f"    Press Ctrl+C to stop\n")
    
    server = HTTPServer((args.host, args.port), ClosingCodeAIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[🔄] Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
