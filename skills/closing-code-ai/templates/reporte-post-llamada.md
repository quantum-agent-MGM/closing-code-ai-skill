# 🎙️ Sales Call Analysis Report — Closing Code AI

**Closer**: {{closer_name}}  
**Prospect**: {{prospect_name}}  
**Empresa**: {{company}}  
**Fecha**: {{date}} | **Duración**: {{duration}} | **Score**: {{score}}/70 | **Grado**: {{grade}} | **Veredicto**: {{veredicto}}

---

## 🎯 Resumen Ejecutivo
{{summary}}

## 📊 Score Cuántico por Dimensión
| Dimensión | Score | Máximo | Ponderado |
|---|---|---|---|
| A — Gravedad Cero | {{score_a}}/10 | 10 | {{score_a}} |
| B — Arquitectura (6 Pasos) | {{score_b}}/10 | 10 | {{score_b}} |
| C — Escaneo Core (Nivel Dolor) | {{score_c}}/10 | 10 | {{score_c}} |
| D — Diagnóstico Tridimensional | {{score_d}}/10 | 10 | {{score_d}} |
| E — Errores Inverso (12 Pecados) | {{score_e}}/10 | 10 | {{score_e}} |
| F — Absorción de Fricción | {{score_f}}/10 | 10 | {{score_f}} |
| G — No Cierre (Ética) | {{score_g}}/10 | 10 | {{score_g}} |
| **TOTAL** | **{{score}}**/70 | 70 | |

## 👤 Perfilado del Prospecto
| Eje | Perfil Detectado |
|---|---|
| **Fricción** | {{arquetipo}} — {{arquetipo_desc}} |
| **Decisión** | {{perfil_decision}} — {{perfil_decision_desc}} |
| **Monetario** | {{perfil_monetario}} — {{perfil_monetario_desc}} |
| **Nivel de Dolor Alcanzado** | {{nivel_dolor}} — {{nivel_dolor_desc}} |
| **Sistema de Cierre Recomendado** | {{sistema_cierre}} |

## 😱 Momento WOW — ¿Cómo supimos esto?

> **Arquetipo detectado:** {{arquetipo_emoji}} **{{arquetipo_nombre}}**
>
> **Lo que este prospecto hará en las próximas 48h si no cierras hoy:**
> > "{{prediccion_48h}}"
>
> **El único sistema que funciona con este arquetipo:**
> > **{{sistema_recomendado}}** — Score mínimo requerido: {{score_minimo}}/70
>
> **Por qué falló tu enfoque actual:**
> > {{porque_fallo}}

---

## ⚠️ Los 12 Pecados Capitales
{{#pecados}}
**[#{{numero}}] {{nombre}}** — [{{timestamp}}]
- Evidencia: "{{evidencia}}"
- Fix: {{fix}}

{{/pecados}}
{{^pecados}}
_¡Sin pecados capitales detectados! 🎉_
{{/pecados}}

## 🕳 Agujeros Negros
{{#agujeros_negros}}
- {{.}}
{{/agujeros_negros}}
{{^agujeros_negros}}
_Sin agujeros negros detectados._
{{/agujeros_negros}}

## 💰 Momentos Clave
{{#momentos}}
{{emoji}} **[{{timestamp}}]** {{descripcion}}
{{/momentos}}
{{^momentos}}
_Sin momentos destacados._
{{/momentos}}

## ✅ Lo Que Hiciste Bien
{{#fortalezas}}
- {{.}}
{{/fortalezas}}

## 📝 Brief de Follow-up

**{{canal}} (enviar en {{tiempo}}):**

{{mensaje_followup}}

**Sistema de cierre a practicar:** {{sistema_practicar}}

## 📈 Comparativa vs Historial
- Tu promedio: {{promedio}}/70
- Tu mejor llamada: {{mejor}}/70
- Tendencia: {{tendencia}}

## 🎯 Acciones para la Próxima Llamada
{{#acciones}}
{{numero}}. {{accion}}
{{/acciones}}

## 🎯 Colapso de Realidad Recomendado
**{{colapso_nombre}}** ({{colapso_apodo}})

{{colapso_descripcion}}

---

*Generado por Closing Code AI — {{tier_name}}*
*Metodología: Closing Cuántico™ QC_4_0*
*Confidencial — solo para uso del closer y su manager*
