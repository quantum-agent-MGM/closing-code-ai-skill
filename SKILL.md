---
name: closing-code-ai
description: "Use when analyzing sales calls, preparing closers pre-call, or generating post-call coaching reports. Integrates with Closing Code AI backend for AI-powered sales intelligence."
version: 1.2.2
author: Closing Code AI
license: proprietary
copyright: "© 2026 The Closing Code AI. All rights reserved."
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

> ⚠️ **LEGAL WARNING:** This skill implements the proprietary Closing Cuántico™ QC_4.0 methodology.
> Commercial use without an active license is prohibited. © 2026 The Closing Code AI. All rights reserved.
> Terms: https://closingcodeai.com/terms

## Overview

Closing Code AI is the premium sales skill for Hermes Agent. Connects your Hermes agent with the Closing Code AI backend to analyze sales calls, generate pre-call briefs, and deliver post-call reports with a 0-70 score based on the proprietary Closing Cuántico™ QC_4.0 methodology.

**Stack:** Closing Code AI API (transcription + analysis) + Hermes Agent (delivery + coaching)

## When to Use (Triggers)

- "analyze this call" / "analiza esta llamada"
- "review my call" / "revisa mi llamada"
- "give me feedback on this recording" / "dame feedback de la call"
- "prepare the closer" / "prepara al closer"
- "generate pre-call brief" / "genera brief pre-llamada"
- "brief for the closer" / "brief para el closer"
- "generate post-call report" / "genera reporte post-llamada"
- "score this recording" / "califica esta grabación"
- "how did I close" / "qué tal cerré"
- "what archetype is this prospect" / "qué arquetipo es este prospecto"
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
Full post-call analysis against Closing Cuántico™ QC_4_0.
- Transcription with timestamps (Closing Code AI Whisper)
- Score 0-70 with 6 quantum dimensions (A-F) + Dimension G
- Three-dimensional profiling: Friction + Decision + Monetary
- The 12 Deadly Sins with exact timestamps
- Black Holes detected/confronted
- Recommended closing system (1 of 10)
- Suggested Reality Collapse for the profile
- Auto follow-up brief (email/WhatsApp ready)
- Comparison vs call history

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

1. Call ends → Closing Code AI ingests audio via `POST /v1/calls/ingest`
2. Closing Code AI transcribes (faster-whisper-server :8100)
3. Closing Code AI analyzes with CQ_3_3 methodology (analyzer :8002)
4. Webhook triggers → skill receives payload
5. Skill generates structured report with `reporte-post-llamada.md` template
6. Sends via Telegram/WhatsApp to closer + manager

### Manual Command

```bash
# Analyze call manually
hermes closing-code-ai analyze <audio_url_or_file>

# Generate pre-call brief
hermes closing-code-ai brief <prospect_name> <company>

# View history
hermes closing-code-ai history
```

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
│   └── reporte-post-llamada.md       → Post-call report template
└── scripts/
    └── webhook-handler.py            → Webhook handler + API client + Whop handler
```

> 🔒 **The Closing Cuántico™ QC_4.0 methodology is NOT in this repository.**
> The public skill is only the interface. The complete methodology (dimensions A-G,
> 12 Deadly Sins, 10 Closing Systems, 4 Archetypes, 5 Collapses) lives in the
> private Closing Code AI backend and is accessed via API with CLOSING_CODE_AI_API_KEY.
> Without a valid API key and active tier, the skill cannot generate analysis.

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
| `/v1/calls/{id}/analysis` | GET | Full QC_4_0 analysis with A-G scores | Closer+ |

### Authentication

The skill requires `CLOSING_CODE_AI_API_KEY` in the environment. The user gets their API key from the Closing Code AI portal (`https://app.closingcodeai.online/settings`).

### Webhook

Closing Code AI sends webhooks to the configured URL when an analysis finishes. The skill exposes a local webhook server at `http://localhost:9876/webhook/closing-code-ai` (configurable).

```bash
# Configure webhook in Closing Code AI
curl -X POST https://api.closingcodeai.online/v1/webhooks \
  -H "X-API-Key: $CLOSING_CODE_AI_API_KEY" \
  -d '{"url": "http://localhost:9876/webhook/closing-code-ai", "events": ["call.analysis.completed"]}'
```

---

## Skill Rules

1. **Direct and actionable** — no fluff. Use closer language.
2. **Honest but constructive** — if the call was bad, say it with a concrete solution.
3. **Confidential** — never share transcripts or prospect data outside the user.
4. **Fast** — pre-call brief <30s, post-call report <5 min after webhook receipt.
5. **English & Spanish** — responds in the user's language.

---

## Prompt Triggers (Auto-activation)

The skill activates automatically when the user says:

- "analyze this call", "review my call", "feedback on the call"
- "prepare the closer", "brief for", "pre-call brief"
- "generate report", "call score", "how did I close"
- "what's my quantum score", "what sins did I commit"
- "what archetype was this prospect", "how to handle objections"
- "call diagnosis", "QC_4_0 report"
- "how to improve my closing", "sales coaching"

---

## Common Pitfalls

1. **No CLOSING_CODE_AI_API_KEY**: The skill fails silently. Always verify the key is configured.
2. **Audio too long (>2h)**: Whisper may truncate. Recommend segmentation for calls >90 min.
3. **Webhook not configured**: Automatic post-call doesn't work. User must run manual analysis.
4. **Wrong tier**: If the user has free Signal Lite but asks for post-call analysis, suggest upgrade to Closer Engine.
5. **Prospect with no public data**: The pre-call brief will be generic. Use open questions as fallback.
6. **Exposing backend name in the skill**: NEVER use the real backend name (QuantumCore) in public files. Always use the visible brand (Closing Code AI). See `references/brand-abstraction-pattern.md`.

---

## Verification Checklist

- [ ] CLOSING_CODE_AI_API_KEY configured
- [ ] CLOSING_CODE_AI_BASE_URL points to correct backend
- [ ] Webhook configured in Closing Code AI portal
- [ ] Telegram/WhatsApp gateway of Hermes active
- [ ] User tier verified (Signal/Closer/Pro)
- [ ] Report generated with score 0-70 (dimensions A-G) + grade
- [ ] Follow-up brief includes concrete next step + suggested closing system
- [ ] Transcription not shared outside the user

---

## Installation

```bash
# Install via private tap (recommended method)
hermes skills tap add quantum-agent-MGM/closing-code-ai-skill

# Or install manually
git clone https://github.com/quantum-agent-MGM/closing-code-ai-skill.git \
  ~/.hermes/skills/devops/closing-code-ai
```

## Tier Activation

```bash
# Signal Lite (free) — pre-call brief
hermes closing-code-ai activate --tier signal-lite

# Closer Engine ($197/mo) — post-call analysis
hermes closing-code-ai activate --tier closer-engine --key $CLOSING_CODE_AI_API_KEY

# Closing Code Pro ($497/mo) — everything + multi-closer + ML
hermes closing-code-ai activate --tier closing-code-pro --key $CLOSING_CODE_AI_API_KEY
```

> ⚡ **Full analysis requires Closer Engine ($197/mo)**
> → Activate at: [whop.com/checkout/plan_rY3E9SKYb61XI](https://whop.com/checkout/plan_rY3E9SKYb61XI/)
> → You will receive your API key via Telegram in less than 2 minutes.

## Distribution and Monetization

### Distribution Channels

1. **Hermes Skills Hub** — `hermes skills tap add quantum-agent-MGM/closing-code-ai-skill`
2. **ClawHub** (`clawhub.ai`)
3. **aiskill.market**
4. **r/hermesagent** — early adopters
5. **High-ticket closer communities worldwide**

### Monetization Loop

```
Customer installs free tap → Uses Signal Lite for 2-3 weeks →
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

- v1.2.2 (2026-05-14): Global repositioning — English + Spanish, languages field in skill.yaml, bilingual triggers
- v1.2.1 (2026-05-14): telegram_id in customers table, notify_user_activation sends to client if telegram_id present
- v1.2.0 (2026-05-14): SQLite + HMAC + Whop handler + bug fixes (score-0-70, typo, Mustache comment)
- v1.1.0 (2026-05-14): Complete skill with tiers, scoring, webhook, distribution
- v1.0.0 (2026-05-13): Initial launch — analysis + report

---

*Closing Code AI — Sales Engine Skill v1.2.2*
*Powered by Closing Code AI backend + Hermes Agent*
*https://closingcodeai.online*
