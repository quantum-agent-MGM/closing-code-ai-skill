# Closing Code AI — Sales Engine Skill for Hermes Agent

```bash
hermes skills tap add quantum-agent-MGM/closing-code-ai-skill
```

**AI-powered sales call analysis for high-ticket closers.**

Powered by Closing Cuántico™ QC_4.0 — a proprietary methodology for
analyzing and improving closing performance.
🌐 Full English & Spanish support

---

## What it does

Analyzes your sales calls automatically and tells you **exactly** what you did wrong, what you did right, and how to close next time.

- 📊 **Score 0-70** with 6 quantum dimensions
- 👤 **Prospect profiling**: Shark? Pufferfish? Dolphin? Oyster?
- ⚠️ **12 Closing Deadly Sins** with timestamps
- 💰 **Prediction**: "This prospect will do X in 48h if you don't close today"
- 📝 **Auto follow-up brief**
- 🚀 **Recommended closing system** for each profile

## 3 Tiers

| Tier | Price | What it includes | Checkout |
|------|-------|------------------|----------|
| **Signal Lite** | **Free** | Pre-call brief with buyer profiling | [whop.com/checkout/plan_tKa03eOMu8tno](https://whop.com/checkout/plan_tKa03eOMu8tno/) |
| **Closer Engine** | **$197/mo** | Full post-call analysis + score + follow-up | [whop.com/checkout/plan_rY3E9SKYb61XI](https://whop.com/checkout/plan_rY3E9SKYb61XI/) |
| **Closing Code Pro** | **$497/mo** | Multi-closer + ML + CRM sync + weekly reports | [whop.com/checkout/plan_I8OXKp52wzdpV](https://whop.com/checkout/plan_I8OXKp52wzdpV/) |

## Installation

```bash
# 1. Add the tap
hermes skills tap add quantum-agent-MGM/closing-code-ai-skill

# 2. Activate free tier
hermes closing-code-ai activate --tier signal-lite

# 3. (Optional) Activate paid tier with API key
export CLOSING_CODE_AI_API_KEY="your-api-key"
hermes closing-code-ai activate --tier closer-engine
```

## Usage

```bash
# Analyze a call manually
hermes closing-code-ai analyze recording.mp3

# Generate pre-call brief
hermes closing-code-ai brief "John Smith" "Acme Corp"

# View history
hermes closing-code-ai history
```

## Stack

- **Backend**: Closing Code AI API (transcription + analysis)
- **Agent**: Hermes Agent (delivery + coaching)
- **Methodology**: Closing Cuántico™ QC_4.0 (proprietary)

## Requirements

- Hermes Agent ≥0.13.0
- Python ≥3.11
- `CLOSING_CODE_AI_API_KEY` (for Closer Engine and Pro tiers)

## License

Proprietary © 2026 The Closing Code AI. All rights reserved.
Commercial use without active license prohibited.

---

**Built for high-ticket closers worldwide · English & Spanish supported**
