# Bundle Architecture: QuantumCore Backend + Hermes Skill Frontend

Source: Claude Sonnet 4.6 analysis, 2026-05-14.

## Philosophy

The backend (QuantumCore) stays invisible. The client installs ONE line. The agent does everything. The technology is yours, the interface is theirs.

## Product Name

> "Closing Code AI — Sales Engine Skill"
> *Para Hermes Agent*

## The 3-Tier Architecture

| Tier | Name | Price | Activation | What Unlocks |
|------|------|-------|------------|--------------|
| **Free** | Signal Lite | $0 | `hermes skills tap add` | Brief pre-llamada básico vía Telegram. Hook de adquisición. |
| **Premium** | Closer Engine | $197/mes | Stripe webhook | Post-call analysis + score 0-100 + timestamps + auto follow-up. |
| **Agency** | Closing Code Pro | $497/mes | Stripe webhook | Multi-closer + weekly patterns + buyer profiling + deal prediction ML. |

## Free Tier as Distribution Moat

Los primeros 20 sellers en Skills Hub establecen el estándar. Si entras con un free tier bien hecho, capturas la comunidad antes que cualquier competidor.

## Monetization Loop

```
Cliente instala tap gratuito
       ↓
Usa Signal Lite 2-3 semanas
       ↓
Hermes le dice: "Esta función requiere Closer Engine"
       ↓
Compra $197/mes vía Stripe webhook
       ↓
Skill desbloquea endpoints de QuantumCore via API key
       ↓
Hermes ejecuta análisis autónomo post-llamada
       ↓
Closer recibe reporte por WhatsApp con tu marca
```

Cero intervención tuya después de la venta. El cliente nunca ve Docker ni QuantumCore — solo ve "Closing Code AI".

## Distribution Channels

1. **Hermes Skills Hub** (tap privado) — `hermes skills tap add user/repo`
2. **ClawHub** (`clawhub.ai`) — cross-distribution
3. **aiskill.market** — orgánica cruzada
4. **r/hermesagent** — comunidad early adopters
5. **Comunidades de closers LatAm** — dolor real, cero competencia en español

## Technical Integration

### QuantumCore → Hermes Webhook

QuantumCore envía webhook cuando `call.analysis.completed`:

```bash
# Configurar en QuantumCore portal
curl -X POST https://api.closingcodeai.online/v1/webhooks \
  -H "X-API-Key: $QUANTUMCORE_API_KEY" \
  -d '{"url": "http://localhost:9876/webhook/quantumcore",
       "events": ["call.analysis.completed"]}'
```

### Skill Script

`scripts/webhook-quantumcore.py` expone servidor HTTP en `:9876`:
- Recibe payload de QuantumCore
- Calcula score 0-100 con rúbrica Closing Cuántico
- Genera reporte Markdown
- Envía por Telegram/WhatsApp
- Guarda en `data/reports/`

### Tier Gating

```python
# En el script
TIER = os.environ.get("CLOSING_CODE_TIER", "signal-lite")

if TIER == "signal-lite":
    features = ["pre-call-brief"]
elif TIER == "closer-engine":
    features = ["pre-call-brief", "post-call-analysis", "score", "followup"]
elif TIER == "closing-code-pro":
    features = ["*"]  # all
```

## Pricing Psychology

- **$0** free tier → removes friction, builds habit
- **$197/mes** → priced as tool, not as agency. Affordable for solo closers.
- **$497/mes** → priced as team multiplier. Justifiable for 3+ closers.

## Timeline de Construcción

| Día | Tarea |
|-----|-------|
| 1 | SKILL.md + skill.yaml + closing-cuantico.md |
| 2 | Publicar tap en GitHub, registrar en Skills Hub y ClawHub |
| 3 | Lanzar free tier en r/hermesagent y comunidades de closers LatAm |
