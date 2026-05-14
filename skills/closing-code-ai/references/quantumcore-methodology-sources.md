# QuantumCore Methodology — Source Files

When updating or extending the Closing Code AI skill, these are the canonical source files for the Closing Cuántico™ methodology. Do NOT guess or invent methodology details — read these files.

## Constitution (Metodology + Reasoning)

**File:** `/root/closing-code-ai/apps/quantumcore-analyzer/prompts/constitution_v3_3.md`
**Contains:**
- Confidence Score protocol
- 6 Dimensiones Cuánticas (A-F)
- 4 Niveles Subatómicos de Dolor (1-4)
- 4 Arquetipos de Fricción (Tiburón, Pez Globo, Delfín, Ostra)
- 4 Perfiles de Decisión + 3 Perfiles Monetarios
- Los 12 Pecados Capitales
- Agujeros Negros (Red Flags de Ghosting)
- Fórmula ACP + Diálogo Socrático
- 5 Colapsos de Realidad

## Output Contract (Format + Rubric)

**File:** `/root/closing-code-ai/apps/quantumcore-analyzer/prompts/output_v4_0.md`
**Contains:**
- JSON contract v4.0 (7 blocks: metadata, profiling, objection, audit, training, scores, mission)
- Scoring: A_gravedad_cero, B_arquitectura, C_escaneo_core, D_diagnostico_tridimensional, E_errores_inverso, F_absorcion_friccion, G_no_cierre
- Score max: 70
- Verdict algorithm (4 deterministic verdicts)
- Critical consistency rules

## Methodology Registry

**File:** `/root/closing-code-ai/shared/methodology_registry.py`
**Contains:**
- Supported methodology versions: v3_3 (CQ_3_3, score_max=60) and v4_0 (QC_4_0, score_max=70)
- Default: v4_0
- Prompt file naming convention

## Closing Systems

**File:** `/root/closing-code-ai/knowledge/methodology/closing_systems.yaml`
**Contains:**
- 10 Sistemas de Cierre (Garantía, Calibración, Activación de Recursos, Secuencia de Fusión, Contraste de Caminos, Análisis Decisional, Referente de Identidad, Constatación Empírica, Reserva Estratégica, Capacidad Progresiva)
- Perfil → Sistema mapping table
- Scripts and error patterns per system

## Live Coach Scoring

**File:** `/root/closing-code-ai/apps/reporting-api/services/live_coach/adherence_report.py`
**Contains:**
- Canon Section 11 — 7 KPIs evaluated post-call
- CanonKPIScores dataclass
- Quality score computation

## Scoring Engine

**File:** `/root/closing-code-ai/apps/quantumcore-analyzer/services/scoring_engine.py`
**Contains:**
- Framework label: "Closing Cuantico CQ_3_3"
- Dimension score extraction from QuantumCore output

---

## Quick Discovery Commands

```bash
# Find methodology files
cd /root/closing-code-ai
find . -name "*methodology*" -o -name "*scoring*" -o -name "*canon*" | grep -v __pycache__

# Search for key terms in codebase
grep -ri "closing.*cuantico\|CQ_.*methodology\|score.*0-70" apps/ shared/ --include="*.py" --include="*.md"

# Read constitution and output contract
head -200 apps/quantumcore-analyzer/prompts/constitution_v3_3.md
head -200 apps/quantumcore-analyzer/prompts/output_v4_0.md
```

---

*Reference for closing-code-ai skill maintainers.*
*Last verified: 2026-05-14*
