# Hermes Agent Skill Standard — Validation & Format

Source: `software-development/hermes-agent-skill-authoring` (in-repo skill) + `tools/skill_manager_tool.py::_validate_frontmatter`.

## Hard Requirements (Validator Enforced)

| Rule | Detail | Penalty if Broken |
|------|--------|-------------------|
| Byte 0 | Must be `---` exactly. No leading blank line, no BOM. | Validation fails |
| Frontmatter close | Must be `\n---\n` before body. | Validation fails |
| YAML parse | Frontmatter must parse as YAML mapping. | Validation fails |
| `name` | Required. Lowercase, hyphens, ≤64 chars (`MAX_NAME_LENGTH`). | Validation fails |
| `description` | Required. ≤1024 chars (`MAX_DESCRIPTION_LENGTH`). | Validation fails |
| Non-empty body | Content after closing `---` must be non-empty. | Validation fails |
| Total size | ≤100,000 chars (`MAX_SKILL_CONTENT_CHARS`, ~36k tokens). | Validation fails |

## Recommended Peer-Matched Shape

Every user-local skill should include:

```yaml
---
name: my-skill-name
description: "Use when <trigger>. <one-line behavior>."
version: 1.0.0
author: Your Name
license: MIT
metadata:
  hermes:
    tags: [short, descriptive, tags]
    related_skills: [other-skill]
---
```

`version` / `author` / `license` / `metadata` are NOT enforced but every peer has them.

## skill.yaml Manifest (For Sellable Skills)

Sellable skills on Skills Hub / ClawHub require a `skill.yaml` with:

```yaml
name: my-skill
display_name: "My Skill"
description: "One-line value prop"
version: 1.0.0
homepage: https://example.com
repository: https://github.com/user/repo

platforms: [linux, macos, windows]
requires:
  hermes: ">=0.13.0"
  python: ">=3.11"

environment:
  required: [API_KEY_1]
  optional: [API_KEY_2]

tiers:
  free-tier:
    name: "Free"
    price: 0
    billing: free
    features: [feature-a]
    limits:
      calls_per_month: 20

  premium:
    name: "Premium"
    price: 197
    price_currency: USD
    billing: monthly
    features: [feature-a, feature-b]
    requires_upgrade_from: free-tier

categories: [sales, productivity]
tags: [tag1, tag2]
related_skills: [other-skill]

entry_points:
  cli:
    - command: my-skill
      subcommands: [analyze, brief, history]
  webhook:
    - path: /webhook/source
      method: POST

dependencies:
  python_packages: [requests, pyyaml]
  external_services:
    - name: api-service
      required_for_tiers: [premium]

metadata:
  hermes:
    tags: [sales]
    min_hermes_version: "0.13.0"
```

## Validation Script (Python)

```python
import yaml, re, pathlib

content = pathlib.Path("SKILL.md").read_text()
assert content.startswith("---"), "Must start with ---"
m = re.search(r'\n---\s*\n', content[3:])
assert m, "Frontmatter must close with newline --- newline"
fm = yaml.safe_load(content[3:m.start()+3])
assert "name" in fm and "description" in fm
assert len(fm["description"]) <= 1024
assert len(content) <= 100_000
body = content[m.end():]
assert len(body.strip()) > 100
print("✅ All validations passed")
```

## Directory Layout

```
skills/<category>/<skill-name>/
├── SKILL.md              → Main instructions
├── skill.yaml            → Manifest (for marketplace)
├── references/           → Knowledge banks, API docs, domain notes
├── templates/            → Starter files, boilerplate configs
└── scripts/              → Re-runnable actions, probes
```

## Distribution

- **Private tap**: `hermes skills tap add user/repo`
- **Skills Hub**: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- **ClawHub**: https://clawhub.ai
- **aiskill.market**: https://aiskill.market/blog/hermes-skills-hub-publishing-community-skills

## Common Pitfalls

1. **In-repo vs user-local**: `skill_manage(action='create')` writes to `~/.hermes/skills/`. For in-repo skills use `write_file` + `git add`.
2. **Session caching**: New skills are NOT visible until a fresh session. Plan for this.
3. **Description too generic**: Must start with "Use when ..." and describe the trigger class, not one task.
4. **Total size >100k**: Split large content into `references/*.md`.
