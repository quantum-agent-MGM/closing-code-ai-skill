---
name: closing-code-ai
description: "Use when analyzing sales calls, preparing closers pre-call, or generating post-call coaching reports. Integrates with Closing Code AI backend for AI-powered sales intelligence."
version: 1.2.0
author: Closing Code AI
license: proprietary
copyright: "© 2026 The Closing Code AI. Todos los derechos reservados."
redistribution: false
terms_url: https://closingcodeai.com/terms
methodology: "Closing Cuántico™ QC_4.0"
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sales, closing, coaching, call-analysis, closing-code-ai, whisper, post-call, pre-call]
    related_skills: [hermes-sales-engine, methodology-alignment]
---

# Closing Code AI — Sales Engine Skill for Hermes Agent

> ⚠️ **ADVERTENCIA LEGAL:** Esta skill implementa la metodología propietaria Closing Cuántico™ QC_4.0.
> Uso comercial sin licencia activa prohibido. © 2026 The Closing Code AI. Todos los derechos reservados.
> Ver términos: https://closingcodeai.com/terms

## Overview

Closing Code AI es la skill premium de ventas para Hermes Agent. Conecta tu agente Hermes con el backend de Closing Code AI para analizar llamadas de ventas, generar briefs pre-llamada, y entregar reportes post-llamada con score 0-70 basado en la metodología propietaria Closing Cuántico™ QC_4.0.

**Stack:** Closing Code AI API (transcripción + análisis) + Hermes Agent (delivery + coaching)

## When to Use

- El usuario dice *"analiza esta llamada"*, *"revisa mi llamada"*, *"dame feedback de la call"*
- El usuario dice *"prepara al closer"*, *"genera brief pre-llamada"*, *"brief para el closer"*
- El usuario dice *"genera reporte post-llamada"*, *"score de la llamada"*, *"qué tal cerré"*
- Post-call automático vía webhook de Closing Code AI

## No usar para:
- Llamadas que no son de ventas (soporte técnico, RH, etc.)
- Análisis sin audio/transcripción disponible
- Coaching en idiomas no soportados (español e inglés soportados)

---

## Tiers de Producto

### Tier 1: Signal Lite (Gratuito)
Brief pre-llamada básico vía Telegram/WhatsApp.
- Buyer profiling (datos públicos del prospect)
- 3 pains probables del prospect
- Preguntas de apertura recomendadas
- Agenda sugerida de 30 minutos

### Tier 2: Closer Engine ($197/mes)
Análisis post-llamada completo contra Closing Cuántico™ QC_4_0.
- Transcripción con timestamps (Closing Code AI Whisper)
- Score 0-70 con 6 dimensiones cuánticas (A-F) + Dimensión G
- Perfilado tridimensional: Fricción + Decisión + Monetario
- Los 12 Pecados Capitales con timestamps exactos
- Agujeros Negros detectados/confrontados
- Sistema de cierre recomendado (1 de 10)
- Colapso de Realidad sugerido para el perfil
- Brief de follow-up automático (email/WhatsApp listo)
- Comparativa vs historial de llamadas

### Tier 3: Closing Code Pro ($497/mes)
Closer Engine × múltiples closers + inteligencia avanzada.
- Todo lo de Closer Engine
- Multi-closer: tracking individual por vendedor
- Reporte semanal de patrones del equipo
- Buyer profiling avanzado vía Closing Code AI API
- Deal prediction ML integrado
- Intent signals
- CRM sync: GHL, HubSpot, Salesforce, Twenty

---

## Flujo de Trabajo

### Pre-llamada (Signal Lite)

1. Usuario dice: *"prepara brief para mi llamada con [Nombre] de [Empresa]"*
2. Hermes detecta intención → activa skill
3. Skill busca datos públicos del prospect (LinkedIn, web, CRM si conectado)
4. Genera brief pre-llamada con template `brief-pre-llamada.md`
5. Envía por Telegram/WhatsApp al closer

### Post-llamada (Closer Engine / Pro)

1. Llamada termina → Closing Code AI ingiere audio vía `POST /v1/calls/ingest`
2. Closing Code AI transcribe (faster-whisper-server :8100)
3. Closing Code AI analiza con CQ_3_3 methodology (analyzer :8002)
4. Webhook dispara → skill recibe payload
5. Skill genera reporte estructurado con template `reporte-post-llamada.md`
6. Envía por Telegram/WhatsApp al closer + manager

### Comando manual

```bash
# Analizar llamada manualmente
hermes closing-code-ai analyze <audio_url_or_file>

# Generar brief pre-llamada
hermes closing-code-ai brief <prospect_name> <company>

# Ver historial
hermes closing-code-ai history
```

---

## Estructura de Archivos

```
closing-code-ai/
├── SKILL.md                          → Este archivo (interfaz pública)
├── skill.yaml                        → Manifest con tiers y pricing
├── README.md                         → Instalación pública
├── .gitignore                        → Excluye private/ y references/
├── references/
│   ├── hermes-skill-standard.md      → Format requirements para Skills Hub
│   ├── methodology-sources.md        → Referencias a archivos fuente del backend
│   ├── whop-subscription-webhook.md  → Patrón de webhook para suscripciones
│   ├── brand-abstraction-pattern.md  → Cómo ocultar el nombre del backend
│   └── webhook-handler-patterns.md   → Patrones probados: SQLite, HMAC, dual handlers
├── templates/
│   ├── brief-pre-llamada.md          → Template brief pre-call
│   └── reporte-post-llamada.md       → Template reporte post-call
└── scripts/
    └── webhook-handler.py            → Webhook handler + API client + Whop handler
```

> 🔒 **La metodología Closing Cuántico™ QC_4.0 NO está en este repositorio.**
> La skill pública es solo la interfaz. La metodología completa (dimensiones A-G,
> 12 Pecados, 10 Sistemas de Cierre, 4 Arquetipos, 5 Colapsos) vive en el
> backend privado de Closing Code AI y se accede vía API con CLOSING_CODE_AI_API_KEY.
> Sin API key válida y tier activo, la skill no puede generar análisis.
---

## Integración con Closing Code AI

### Endpoints Utilizados

| Endpoint | Método | Uso | Tier |
|----------|--------|-----|------|
| `/health` | GET | Health check | Todos |
| `/v1/calls/ingest` | POST | Ingestar audio de llamada | Closer+ |
| `/v1/clients/{id}/analysis/latest` | GET | Último análisis | Closer+ |
| `/v1/live-coach/suggestions` | POST | Suggestions live coach | Pro |
| `/v1/deals/predict` | POST | Deal prediction ML | Pro |
| `/v1/intent-signals/score` | POST | Intent scoring | Pro |
| `/v1/buyer-profiling/profile` | POST | Buyer profiling | Pro |
| `/v1/calls/{id}/analysis` | GET | Análisis QC_4_0 completo con scores A-G | Closer+ |

### Autenticación

La skill requiere `CLOSING_CODE_AI_API_KEY` en el environment. El usuario obtiene su API key desde el portal de Closing Code AI (`https://app.closingcodeai.online/settings`).

### Webhook

Closing Code AI envía webhooks a la URL configurada cuando un análisis termina. La skill expone un servidor webhook local en `http://localhost:9876/webhook/closing-code-ai` (configurable).

```bash
# Configurar webhook en Closing Code AI
curl -X POST https://api.closingcodeai.online/v1/webhooks \
  -H "X-API-Key: $CLOSING_CODE_AI_API_KEY" \
  -d '{"url": "http://localhost:9876/webhook/closing-code-ai", "events": ["call.analysis.completed"]}'
```

---

## Reglas de la Skill

1. **Directo y accionable** — sin fluff. Usar lenguaje de closer.
2. **Honesto pero constructivo** — si la llamada fue mala, decirlo con solución concreta.
3. **Confidencial** — nunca compartir transcripciones ni datos del prospect fuera del usuario.
4. **Rápido** — brief pre-llamada <30s, reporte post-llamada <5 min tras recepción de webhook.
5. **En español por defecto** — inglés si el usuario lo solicita explícitamente.

---

## Prompt Triggers (Auto-activation)

La skill se activa automáticamente cuando el usuario dice:

- "analiza esta llamada", "revisa mi llamada", "feedback de la call"
- "prepara al closer", "brief para", "brief pre-llamada"
- "genera reporte", "score de la llamada", "qué tal cerré"
- "cuál es mi score cuántico", "qué pecados cometí"
- "qué arquetipo era este prospecto", "cómo manejar objeciones"
- "diagnóstico de la llamada", "reporte QC_4_0"
- "cómo mejorar mi closing", "coaching de ventas"

---

## Common Pitfalls

1. **Sin CLOSING_CODE_AI_API_KEY**: La skill falla silenciosamente. Siempre verificar que la key está configurada.
2. **Audio muy largo (>2h)**: Whisper puede truncar. Recomendar segmentación para calls >90 min.
3. **Webhook no configurado**: El post-call automático no funciona. El usuario debe ejecutar análisis manualmente.
4. **Tier incorrecto**: Si el usuario tiene Signal Lite gratis pero pide análisis post-llamada, sugerir upgrade a Closer Engine.
5. **Prospect sin datos públicos**: El brief pre-llamada será genérico. Usar preguntas abiertas como fallback.
6. **Exponer nombre del backend en la skill**: NUNCA usar el nombre real del backend (QuantumCore) en archivos públicos. Usar siempre la marca visible (Closing Code AI). Ver `references/brand-abstraction-pattern.md`.

---

## Verification Checklist

- [ ] CLOSING_CODE_AI_API_KEY configurado
- [ ] CLOSING_CODE_AI_BASE_URL apunta al backend correcto
- [ ] Webhook configurado en Closing Code AI portal
- [ ] Telegram/WhatsApp gateway de Hermes activo
- [ ] Tier del usuario verificado (Signal/Closer/Pro)
- [ ] Reporte generado con score 0-70 (dimensiones A-G) + grade
- [ ] Brief de follow-up incluye próximo paso concreto + sistema de cierre sugerido
- [ ] Transcripción no compartida fuera del usuario

---

## Instalación

```bash
# Instalar vía tap privado (método recomendado)
hermes skills tap add quantum-agent-MGM/closing-code-ai-skill

# O instalar manualmente
git clone https://github.com/quantum-agent-MGM/closing-code-ai-skill.git \
  ~/.hermes/skills/devops/closing-code-ai
```

## Activación de Tier

```bash
# Signal Lite (gratis) — brief pre-llamada
hermes closing-code-ai activate --tier signal-lite

# Closer Engine ($197/mes) — análisis post-llamada
hermes closing-code-ai activate --tier closer-engine --key $CLOSING_CODE_AI_API_KEY

# Closing Code Pro ($497/mes) — todo + multi-closer + ML
hermes closing-code-ai activate --tier closing-code-pro --key $CLOSING_CODE_AI_API_KEY
```

> ⚡ **Análisis completo requiere Closer Engine ($197/mes)**
> → Activa en: [whop.com/checkout/plan_rY3E9SKYb61XI](https://whop.com/checkout/plan_rY3E9SKYb61XI/)
> → Recibirás tu API key por Telegram en menos de 2 minutos.

## Distribución y Monetización

### Canales de Distribución

1. **Hermes Skills Hub** — `hermes skills tap add quantum-agent-MGM/closing-code-ai-skill`
2. **ClawHub** (`clawhub.ai`)
3. **aiskill.market**
4. **r/hermesagent** — early adopters
5. **Comunidades de closers LatAm**

### Loop de Monetización

```
Cliente instala tap gratuito → Usa Signal Lite 2-3 semanas →
Hermes sugiere upgrade → Compra $197/mes → Skill desbloquea Closing Code AI →
Hermes ejecuta análisis autónomo → Closer recibe reporte por WhatsApp
```

### Stripe Webhook para Activación

```bash
# Configurar webhook de Stripe para desbloquear tier
stripe webhook_endpoints create \
  --url https://api.closingcodeai.online/v1/skills/activate \
  --events checkout.session.completed
```

## Changelog

- v1.2.0 (2026-05-14): SQLite + HMAC + Whop handler + bug fixes (score-0-70, typo)
- v1.1.0 (2026-05-14): Skill completa con tiers, scoring, webhook, distribución
- v1.0.0 (2026-05-13): Lanzamiento inicial — análisis + reporte

---

*Closing Code AI — Sales Engine Skill v1.2.0*
*Powered by Closing Code AI backend + Hermes Agent*
*https://closingcodeai.online*
