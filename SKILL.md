---
name: closing-code-ai
description: "Use when analyzing sales calls, preparing closers pre-call, or generating post-call coaching reports. Integrates with Closing Code AI backend for AI-powered sales intelligence."
version: 1.3.2
author: Closing Code AI
license: proprietary
copyright: "© 2026 The Closing Code AI. All rights reserved."
redistribution: false
terms_url: https://skill.closingcodeai.online/terms.html
methodology: "Closing Cuántico™ QC_4.1"
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [sales, closing, coaching, call-analysis, closing-code-ai, whisper, post-call, pre-call]
    related_skills: [hermes-sales-engine, methodology-alignment]
    post_install_message: |
      ✅ Closing Code AI skill installed.
      
      Try it now with a real call:
      "Generate the QC 4.1 for this call"
      
      If it doesn't respond:
      1. Check that HERMES_CLOSING_CODE_API_KEY is configured
      2. Confirm you're on the correct profile
      3. Try again with: "Analyze this sales call"
---

# Closing Code AI — Sales Engine Skill for Hermes Agent

> ⚠️ **LEGAL WARNING:** This skill implements the proprietary Closing Cuántico™ QC_4.1 methodology.
> Commercial use without an active license is prohibited. © 2026 The Closing Code AI. All rights reserved.
> Terms: https://skill.closingcodeai.online/terms.html

## Overview

Closing Code AI is the premium sales skill for Hermes Agent. Connects your Hermes agent with the Closing Code AI backend to analyze sales calls, generate pre-call briefs, and deliver post-call reports with a 0-70 score based on the proprietary Closing Cuántico™ QC_4.1 methodology.

**Stack:** Closing Code AI API (transcription + analysis) + Hermes Agent (delivery + coaching)

## When to Use (Triggers)

Use any of these exact phrases to activate the skill:

1. **"Analiza esta llamada de ventas"** / **"Analyze this sales call"**
2. **"Genera el QC 4.1 de esta llamada"** / **"Generate the QC 4.1 for this call"**
3. **"Dame el score de cierre de esta grabación"** / **"Give me the closing score of this recording"**
4. **"Qué hizo mal el closer aquí"** / **"What did the closer do wrong here"**
5. **"Haz coaching sobre esta llamada"** / **"Coach me on this call"**

Also works with variations like:
- "review my call", "feedback on the call"
- "prepare the closer", "pre-call brief"
- "what archetype is this prospect"
- Post-call automatic via Closing Code AI webhook

## Do Not Use For:
- Calls that are not sales (technical support, HR, etc.)
- Analysis without available audio/transcription
- Coaching in unsupported languages (English and Spanish supported)

---

## Product Tiers

### Tier 1: Signal Lite (Free)
Basic pre-call brief via Telegram/WhatsApp.
- Buyer profiling (public data on the prospect)
- 3 probable pains of the prospect
- Recommended opening questions
- Suggested 30-minute agenda

### Tier 2: Closer Engine ($197/mo)
Full post-call analysis against Closing Cuántico™ QC_4_1.
- Transcription with timestamps (Closing Code AI Whisper)
- Score 0-70 with 6 quantum dimensions (A-F) + Dimension G (Ejecución de Cierre)
- Three-dimensional profiling: Friction + Decision + Monetary
- The 12 Deadly Sins with exact timestamps
- Black Holes detected/confronted
- Recommended closing system (1 of 10)
- Suggested Reality Collapse for the profile
- Auto follow-up brief (email/WhatsApp ready)
- Comparison vs call history
- **Premium HTML report** — raw LLM markdown rendered to HTML without filtering. The full richness of the QC_4.1 analysis (evidence, scripts, mission, audit) is preserved. Not a summary — the client gets every insight the LLM generated.

### Tier 3: Closing Code Pro ($497/mo)
Closer Engine × multiple closers + advanced intelligence.
- Everything in Closer Engine
- Multi-closer: individual tracking per seller
- Weekly team pattern report
- Advanced buyer profiling via Closing Code AI API
- Integrated ML deal prediction
- Intent signals
- CRM sync: GHL, HubSpot, Salesforce, Twenty

---

## Workflow

### Pre-call (Signal Lite)

1. User says: *"prepare brief for my call with [Name] from [Company]"*
2. Hermes detects intent → activates skill
3. Skill searches public data on the prospect (LinkedIn, web, CRM if connected)
4. Generates pre-call brief with `brief-pre-llamada.md` template
5. Sends via Telegram/WhatsApp to the closer

### Post-call (Closer Engine / Pro)

1. User uploads audio or call ends → Backend ingests via `POST /v1/calls/ingest`
2. Backend transcribes (Groq Whisper with chunked processing for calls >20 min)
3. Backend analyzes with Closing Cuántico™ QC_4.1 methodology (analyzer)
4. Backend generates **premium HTML report** — raw LLM markdown rendered to HTML without filtering:
   - The LLM analyzer outputs rich markdown analysis (evidence paragraphs, scripts, mission, audit details)
   - The backend renderer converts this raw markdown directly to HTML without truncating or templating
   - **Rich in content**: 83 minutes of analysis looks like 83 minutes of analysis, not a summary
   - **3 tiers for readability**: Executive summary (top), Coaching details (middle), Technical breakdown (collapsible)
   - **Report URL**: `https://skill.closingcodeai.online/reports/{call_id}.html`
   - The full depth of the Closing Cuántico™ QC_4.1 system prompt is reflected in the HTML output
5. Skill fetches summary via `GET /v1/calls/{id}/analysis`
6. Skill delivers report link + score summary via Telegram/WhatsApp to closer + manager

> **Webhook outbound is NOW AVAILABLE** ✅ (deployed 2026-05-20)
>
> The Closing Code AI backend sends a webhook to your configured URL when analysis completes.
> Payload: `{event: "call.analysis.completed", call_id, score, verdict, report_url, ...}`
>
> **To configure:** Set `webhook_url` on your client record via `PUT /v1/clients/{id}` or contact support.
>
> **Fallback:** If webhook is not configured, poll `GET /v1/calls/{id}/analysis` for `analysis_status = "completed"`.

---

## Installation

Install the skill in the Hermes profile you use for sales:

```bash
hermes skills install https://github.com/quantum-agent-MGM/closing-code-ai-skill
```

> **Profile recommendation:** Install in the profile you actually use for sales.
> If you use multiple profiles, install the skill only where you need it and
> configure the API key in that same profile to avoid confusion.

## Configuration

The skill requires `HERMES_CLOSING_CODE_AI_API_KEY` in the environment of the profile.

### Step 1: Get your API key

Activate your free tier at:
**https://skill.closingcodeai.online**

You will receive an API key after activation.

### Step 2: Configure in Hermes

Add the API key to your profile's environment:

```bash
# In your Hermes profile .env file:
HERMES_CLOSING_CODE_API_KEY=ccai_tu_api_key_aqui
```

Or set it via Hermes CLI:
```bash
hermes config set HERMES_CLOSING_CODE_API_KEY ccai_tu_api_key_aqui
```

### Step 3: Verify

Test with the smoke test below.

---

## ⚠️ Important

**No `activate` command exists.**

These commands do NOT exist and will fail:
```bash
hermes closing-code-ai activate --tier signal-lite      # ❌ Does not exist
hermes closing-code-ai activate --tier closer-engine    # ❌ Does not exist
hermes closing-code-ai analyze recording.mp3            # ❌ Does not exist
hermes closing-code-ai brief "Name" "Company"           # ❌ Does not exist
hermes closing-code-ai history                          # ❌ Does not exist
```

The skill becomes available automatically when:
1. It is installed in the correct profile
2. The API key is configured correctly
3. You use one of the trigger phrases listed above

---

## Smoke Test (30 seconds)

Run this test to confirm the skill is ready:

1. **Install the skill:**
   ```bash
   hermes skills install https://github.com/quantum-agent-MGM/closing-code-ai-skill
   ```

2. **Configure your API key:**
   ```bash
   hermes config set HERMES_CLOSING_CODE_API_KEY ccai_tu_api_key_aqui
   ```

3. **Test with a trigger:**
   In Hermes, type or say:
   ```
   Genera el QC 4.1 de esta llamada
   ```

**Expected result:**
- Hermes enters the analysis flow
- Recognizes you want to evaluate a real call
- Asks for the audio file or processes it if already attached
- Responds with analysis intent, not generic chat

If this works, the skill is correctly configured.

---

## File Structure

```
closing-code-ai/
├── SKILL.md                          → This file (public interface)
├── skill.yaml                        → Manifest with tiers and pricing
├── README.md                         → Public installation guide
├── .gitignore                        → Excludes private/ and references/
├── references/
│   ├── hermes-skill-standard.md      → Format requirements for Skills Hub
│   ├── methodology-sources.md        → References to backend source files
│   ├── whop-subscription-webhook.md  → Webhook pattern for subscriptions
│   ├── brand-abstraction-pattern.md  → How to hide backend name
│   └── webhook-handler-patterns.md   → Proven patterns: SQLite, HMAC, dual handlers
├── templates/
│   ├── brief-pre-llamada.md          → Pre-call brief template
│   └── reporte-post-llamada.md       → Post-call report reference (HTML generated by backend)
└── scripts/
    └── webhook-handler.py            → Webhook handler + API client + Whop handler
```

> 🔒 **The Closing Cuántico™ QC_4.1 methodology is NOT in this repository.**
> The public skill is only the interface. The complete methodology (dimensions A-G,
> 12 Deadly Sins, 10 Closing Systems, 4 Archetypes, 5 Collapses) lives in the
> private Closing Code AI backend and is accessed via API with HERMES_CLOSING_CODE_API_KEY.
> Without a valid API key and active tier, the skill cannot generate analysis.
> The premium HTML reports are rendered server-side by the Closing Code AI backend.

---

## Integration with Closing Code AI

### Endpoints Used

| Endpoint | Method | Use | Tier |
|----------|--------|-----|------|
| `/health` | GET | Health check | All |
| `/v1/calls/ingest` | POST | Ingest call audio | Closer+ |
| `/v1/clients/{id}/analysis/latest` | GET | Latest analysis | Closer+ |
| `/v1/live-coach/suggestions` | POST | Live coach suggestions | Pro |
| `/v1/deals/predict` | POST | ML deal prediction | Pro |
| `/v1/intent-signals/score` | POST | Intent scoring | Pro |
| `/v1/buyer-profiling/profile` | POST | Buyer profiling | Pro |
| `/v1/calls/{id}/analysis` | GET | Full QC_4_1 analysis with A-G scores + HTML report URL | Closer+ |

### Authentication

The skill requires `HERMES_CLOSING_CODE_API_KEY` in the environment. The user gets their API key from the Closing Code AI portal (`https://skill.closingcodeai.online`).

### Webhook

> **✅ Webhook outbound is NOW AVAILABLE** (deployed 2026-05-20)
>
> Closing Code AI sends webhooks to the configured URL when an analysis finishes.
> The skill exposes a local webhook server at `http://localhost:9876/webhook/closing-code-ai` (configurable).
>
> **Payload received:**
> ```json
> {
>   "event": "call.analysis.completed",
>   "call_id": "uuid",
>   "client_id": "uuid",
>   "status": "completed",
>   "analysis": {
>     "score": 52,
>     "verdict": "Quedó en el aire",
>     "grade": "C",
>     "report_url": "https://skill.closingcodeai.online/reports/{call_id}.html",
>     "language": "es",
>     "dimensions": {"A": 8.5, "B": 7.2, "C": 6.0, "D": 9.1, "E": 5.5, "F": 7.8, "G": 4.0}
>   }
> }
> ```
>
> **To configure:** Set `webhook_url` on your Closing Code AI client record.
> Contact support or use `PUT /v1/clients/{id}` with `{webhook_url: "..."}`.
>
> **Fallback:** If no webhook_url is configured, poll `GET /v1/calls/{id}/analysis`.
> ```

---

## Skill Rules

1. **Direct and actionable** — no fluff. Use closer language.
2. **Honest but constructive** — if the call was bad, say it with a concrete solution.
3. **Confidential** — never share transcripts or prospect data outside the user.
4. **Fast** — pre-call brief <30s, post-call report <5 min after webhook receipt.
5. **English & Spanish** — responds in the user's language.

---

## Common Pitfalls

1. **No HERMES_CLOSING_CODE_API_KEY**: The skill fails silently. Always verify the key is configured.
2. **Audio too long (>2h)**: Whisper may truncate. Recommend segmentation for calls >90 min.
3. **Webhook not configured**: Automatic post-call doesn't work. User must run manual analysis.
4. **Wrong tier**: If the user has free Signal Lite but asks for post-call analysis, suggest upgrade to Closer Engine.
5. **Prospect with no public data**: The pre-call brief will be generic. Use open questions as fallback.
6. **Exposing backend name in the skill**: NEVER use the real backend name (QuantumCore) in public files. Always use the visible brand (Closing Code AI). See `references/brand-abstraction-pattern.md`.
7. **"unknown command" error**: There is no `activate` or `analyze` command. Use natural language triggers instead.

---

## Verification Checklist

- [ ] HERMES_CLOSING_CODE_API_KEY configured
- [ ] CLOSING_CODE_AI_BASE_URL points to correct backend
- [ ] Webhook configured in Closing Code AI portal (or polling fallback understood)
- [ ] Telegram/WhatsApp gateway of Hermes active
- [ ] User tier verified (Signal/Closer/Pro)
- [ ] Report delivered as link to premium HTML report — raw LLM markdown rendered without filtering. Rich in content, not a summary.
- [ ] Score 0-70 with dimensions A-G (G = Ejecución de Cierre) + verdict + grade
- [ ] User understands webhook outbound is not yet available — polling or manual refresh required
- [ ] Transcription not shared outside the user
- [ ] Smoke test passed (see Smoke Test section above)

---

## Distribution and Monetization

### Distribution Channels

1. **Hermes Skills Hub** — `hermes skills install https://github.com/quantum-agent-MGM/closing-code-ai-skill`
2. **ClawHub** (`clawhub.ai`)
3. **aiskill.market**
4. **r/hermesagent** — early adopters
5. **High-ticket closer communities worldwide**

### Monetization Loop

```
Customer installs free skill → Uses Signal Lite for 2-3 weeks →
Hermes suggests upgrade → Purchases $197/mo → Skill unlocks Closing Code AI →
Hermes runs autonomous analysis → Closer receives report via WhatsApp
```

### Whop Webhook for Activation

```bash
# Configure Whop webhook to unlock tier
# Webhook URL: https://api.closingcodeai.online/v1/webhooks/whop
# Events: membership.activated, membership.deactivated
```

## Changelog

- v1.3.2 (2026-05-20): **Webhook outbound AVAILABLE** ✅
  - Backend now sends webhooks when analysis completes (`call.analysis.completed`)
  - Payload: score, verdict, report_url, dimensions A-G
  - Configure via `webhook_url` on client record
  - Fallback polling still works if webhook not configured
- v1.3.1 (2026-05-20): **Fase 1 — Reporte HTML + QC_4.1 alignment.**
  - Updated methodology: QC_4.0 → QC_4.1 (Dimension G = Ejecución de Cierre, no "No Cierre")
  - Documented that backend generates premium HTML 3-tier reports (Executive/Coach/Technical)
  - Removed claim that skill generates Markdown reports locally — backend renders HTML server-side
  - Documented webhook limitation: outbound webhooks not yet available; polling required
  - Updated post-call workflow to reflect backend-generated HTML report at `/reports/{call_id}.html`
  - Updated verification checklist for HTML report delivery
- v1.3.0 (2026-05-17): Removed fake commands (activate, analyze, brief, history). Added smoke test. Fixed API key variable name to HERMES_CLOSING_CODE_API_KEY. Added post-install message. Simplified installation.
- v1.2.2 (2026-05-14): Global repositioning — English + Spanish, languages field in skill.yaml, bilingual triggers
- v1.2.1 (2026-05-14): telegram_id in customers table, notify_user_activation sends to client if telegram_id present
- v1.2.0 (2026-05-14): SQLite + HMAC + Whop handler + bug fixes (score-0-70, typo, Mustache comment)
- v1.1.0 (2026-05-14): Complete skill with tiers, scoring, webhook, distribution
- v1.0.0 (2026-05-13): Initial launch — analysis + report

---

*Closing Code AI — Sales Engine Skill v1.3.2*
*Powered by Closing Code AI backend + Hermes Agent*
*https://closingcodeai.online*
