# Closing Code AI — Sales Engine Skill for Hermes Agent

```bash
hermes skills tap add quantum-agent-MGM/closing-code-ai-skill
```

**La única skill de ventas con metodología propietaria de closing en español.**

---

## ¿Qué hace?

Analiza tus llamadas de ventas automáticamente y te dice **exactamente** qué hiciste mal, qué hiciste bien, y cómo cerrar la próxima vez.

- 📊 **Score 0-70** con 6 dimensiones cuánticas
- 👤 **Perfilado del prospecto**: ¿Tiburón? ¿Pez Globo? ¿Delfín? ¿Ostra?
- ⚠️ **12 Pecados Capitales del Closing** con timestamps
- 💰 **Predicción**: "Este prospecto hará X en 48h si no cierras hoy"
- 📝 **Brief de follow-up** automático
- 🚀 **Sistema de cierre recomendado** para cada perfil

## 3 Tiers

| Tier | Precio | Qué incluye |
|------|--------|-------------|
| **Signal Lite** | **Gratis** | Brief pre-llamada con buyer profiling |
| **Closer Engine** | **$197/mes** | Análisis post-llamada completo + score + follow-up |
| **Closing Code Pro** | **$497/mes** | Multi-closer + ML + CRM sync + reportes semanales |

## Instalación

```bash
# 1. Agregar el tap
hermes skills tap add quantum-agent-MGM/closing-code-ai-skill

# 2. Activar tier gratuito
hermes closing-code-ai activate --tier signal-lite

# 3. (Opcional) Activar tier pago con API key
export CLOSING_CODE_AI_API_KEY="tu-api-key"
hermes closing-code-ai activate --tier closer-engine
```

## Uso

```bash
# Analizar una llamada manualmente
hermes closing-code-ai analyze grabacion.mp3

# Generar brief pre-llamada
hermes closing-code-ai brief "Juan Pérez" "Acme Corp"

# Ver historial
hermes closing-code-ai history
```

## Stack

- **Backend**: Closing Code AI API (transcripción + análisis)
- **Agente**: Hermes Agent (delivery + coaching)
- **Metodología**: Closing Cuántico™ QC_4.0 (propietaria)

## Requisitos

- Hermes Agent ≥0.13.0
- Python ≥3.11
- `CLOSING_CODE_AI_API_KEY` (para tiers Closer Engine y Pro)

## Licencia

Proprietary © 2026 The Closing Code AI. Todos los derechos reservados.
Uso comercial sin licencia activa prohibido.

---

**Creado en Perú 🇵🇪 para closers de habla hispana.**
