# Closing Code AI — Sales Engine Skill for Hermes Agent

Tu capa de coaching para llamadas de ventas dentro de Hermes.

Closing Code AI analiza grabaciones, detecta errores críticos y genera reportes QC_4.0 para que el closer sepa exactamente qué corregir en la próxima llamada.

---

## Quickstart (< 2 minutos)

### 1. Consigue tu API key (gratis)

Activa tu tier gratuito aquí:
**https://skill.closingcodeai.online**

Recibirás una API key tipo `ccai_...` después de activar.

### 2. Instala el skill

```bash
hermes skills install https://github.com/quantum-agent-MGM/closing-code-ai-skill
```

> Instálalo en el **perfil que usas para ventas**. Si usas varios perfiles, instálalo solo donde harás análisis y configura la API key en ese mismo perfil.

### 3. Configura tu API key

```bash
hermes config set HERMES_CLOSING_CODE_API_KEY ccai_tu_api_key_aqui
```

### 4. Prueba con una llamada real

En Hermes, escribe:
```
Genera el QC 4.0 de esta llamada
```

**¿Funcionó?** → El skill está listo.
**¿No respondió?** → Revisa la sección Troubleshooting abajo.

---

## Cómo usar (5 triggers exactos)

Di cualquiera de estas frases para activar el skill:

1. **"Analiza esta llamada de ventas"**
2. **"Genera el QC 4.0 de esta llamada"**
3. **"Dame el score de cierre de esta grabación"**
4. **"Qué hizo mal el closer aquí"**
5. **"Haz coaching sobre esta llamada de ventas"**

---

## Qué obtienes

Cada análisis puede devolverte:

- 📊 **Score QC_4.0** (0-70) con dimensiones A-G
- 👤 **Perfil del prospecto**: Shark, Pufferfish, Dolphin, Oyster
- ⚠️ **12 Deadly Sins** con timestamps exactos
- 💰 **Predicción**: "Este prospecto hará X en 48h si no cierras hoy"
- 📝 **Guion sugerido** para la próxima llamada
- 🚀 **Sistema de cierre recomendado** para cada perfil

---

## 3 Tiers

| Tier | Precio | Qué incluye | Activar |
|------|--------|-------------|---------|
| **Signal Lite** | **Gratis** | Brief pre-llamada con buyer profiling | [skill.closingcodeai.online](https://skill.closingcodeai.online) |
| **Closer Engine** | **$197/mes** | Análisis post-llamada completo + score + follow-up | [whop.com](https://whop.com/checkout/plan_rY3E9SKYb61XI/) |
| **Closing Code Pro** | **$497/mes** | Multi-closer + ML + CRM sync + reportes semanales | [whop.com](https://whop.com/checkout/plan_I8OXKp52wzdpV/) |

---

## ⚠️ Importante

**No existe un comando `activate`.**

Estos comandos NO funcionan:
```bash
hermes closing-code-ai activate --tier signal-lite      # ❌ No existe
hermes closing-code-ai activate --tier closer-engine    # ❌ No existe
hermes closing-code-ai analyze recording.mp3            # ❌ No existe
```

El skill queda listo automáticamente cuando:
1. Está instalado en tu perfil
2. La API key está configurada
3. Lo invocas con uno de los 5 triggers de arriba

---

## Prueba rápida (smoke test)

Si no estás seguro de que quedó listo:

1. Verifica que el skill está instalado:
   ```bash
   hermes skills list
   ```

2. Verifica tu API key:
   ```bash
   hermes config get HERMES_CLOSING_CODE_API_KEY
   ```

3. Prueba el trigger:
   ```
   Dame el score de cierre de esta llamada
   ```

**Resultado esperado:** Hermes entra al flujo de análisis y reconoce que quieres evaluar una llamada.

---

## Troubleshooting

### "El skill no responde"
Revisa en orden:
1. ¿Estás en el perfil correcto?
2. ¿El skill aparece en `hermes skills list`?
3. ¿`HERMES_CLOSING_CODE_API_KEY` está configurada?
4. ¿La API key es válida? (consíguela en [skill.closingcodeai.online](https://skill.closingcodeai.online))

### "Me aparece unknown command"
No hay comando `activate`. Usa triggers naturales como los 5 de arriba.

### "Uso varios perfiles"
Instálalo solo en el perfil donde harás análisis de ventas. La API key debe estar en ese mismo perfil.

---

## Stack

- **Backend**: Closing Code AI API (transcription + analysis)
- **Agent**: Hermes Agent (delivery + coaching)
- **Methodology**: Closing Cuántico™ QC_4.0 (proprietary)

## Requisitos

- Hermes Agent ≥0.13.0
- Python ≥3.11
- `HERMES_CLOSING_CODE_API_KEY` (para Closer Engine y Pro tiers)

## Licencia

Proprietary © 2026 The Closing Code AI. All rights reserved.
Commercial use without active license prohibited.

---

**Built for high-ticket closers worldwide · English & Spanish supported**
