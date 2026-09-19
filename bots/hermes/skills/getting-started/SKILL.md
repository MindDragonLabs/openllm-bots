---
name: getting-started
description: First-run setup for Hermes as OpenLLM orchestrator. Use when OpenLLM is not yet attached to this Hermes profile, or the user asks how Hermes and OpenLLM relate.
---

# Getting started (Hermes)

Teach the split, then attach once. **You (Hermes) are the orchestrator. OpenLLM is the model fabric.**

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | Hermes | Plans, picks tools, approvals, terminal/files/git, GitHub/Vercel connectors |
| **Model fabric** | OpenLLM gateway + `openllm mcp` | Routes inference across subscriptions/providers; account API, code/docs search, memory |

Hermes does **not** get OpenLLM by default. Attach it per profile: [docs/setup.md](../../docs/setup.md), concepts in [shared/openllm-connect.md](../../../../shared/openllm-connect.md).

## First-run script (one thing at a time)

1. **Explain the split** (table above) in two sentences. Ask whether they already have an OpenLLM account; if not, send them to [openllm.sh](https://openllm.sh) and wait.
2. **CLI on the Hermes host.** `command -v openllm || openllm version`. If missing, official installer (review first): `curl -fsSL "https://openllm.sh/api/setup/cli/install.sh" | bash`.
3. **API key.** From the openllm.sh dashboard (`sk-llm` prefix). Goes into the profile `.env` (`hermes config env-path`) — never into a skill, git, or chat. If pasted in chat: move it to `.env`, do not echo it.
4. **Origin.** Default `https://openllm.sh`. Only collect `OPENLLM_CLOUD_ORIGIN` if they say otherwise.
5. **Register + verify** — the two commands from [docs/setup.md](../../docs/setup.md): `hermes mcp add openllm …` then `hermes mcp test openllm`. Mind the flag-order and stdin pitfalls documented there.
6. **New session, then confirm** the live tool list (`mcp_openllm_*`). Expect three groups: native gateway API, code/docs search, memory. Trust the live list.
7. **Offer a mode:** dashboard query (**openllm-dashboard**) or a dev task (**openllm-dev-task**).

## Two modes (remember this)

**Dashboard mode** — inspect/manage the OpenLLM account through MCP tools (usage, models, keys, providers, config). Browser on openllm.sh is fallback only.

**Development execution mode** — clarify goal → pick a gateway model → gather context (code/docs search, memory) → implement with Hermes' own tools → optional specialist hop through gateway completions → report.

Long-form playbook: **hermes-orchestrator**.
