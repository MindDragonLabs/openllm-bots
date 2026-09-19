---
name: openllm-dashboard
description: Use OpenLLM MCP tools for dashboard-like account work (usage, tokens, keys, providers, config, billing). Use when the Hermes user asks about their OpenLLM account instead of the web UI.
---

# OpenLLM dashboard mode (Hermes)

Manage the OpenLLM **account through MCP**, not by clicking [openllm.sh](https://openllm.sh) first. You (Hermes) stay the orchestrator; OpenLLM exposes the native gateway API as MCP tools.

If the server is not attached: **openllm-connect** / [docs/setup.md](../../docs/setup.md).

## Before you start

1. Confirm `mcp_openllm_*` tools are live. If not, **openllm-connect**.
2. Group them mentally: gateway/account API, code/docs search, memory.
3. Read operations first; mutations only on explicit request.

## Surfaces to look for

Map user language to API areas, then pick the matching **live** tool. Operation ids below are landmarks from the CLI-embedded OpenAPI spec (2.6.36: `api_stats_user`, `api_keys_list`, `api_v1Models_list`, …) — not a promise of exact names forever.

| User intent | Upstream area | Notes |
| --- | --- | --- |
| What models can I call? | `GET /v1/models` | Account-enabled catalog incl. chain aliases. Never invent model ids. |
| Usage, tokens, requests | `/stats`, `/stats/requests`(+`/items`, `/errors`), `/stats/keys/{id}` | Summarize; don't dump huge logs unasked. |
| Keys / devices | `/keys` | Never display secret material. Confirm before create/delete/reset. |
| Providers / credentials | `/credentials`, `/providers/custom` | Blobs are secret. Prefer status/list over rewrite. |
| Config | `/config/user`, `/config/global` | Read first; explain diffs before update. |
| Billing | `/billing`, `/billing/history` | Checkout/portal → website fallback. |
| Identity | `/user` | `whoAmI` on the MCP side is the quick account check. |
| Web/docs search via gateway | `POST /v1/search` | Gateway op, dev-adjacent. |

`/public/usage-index` is marketing data, not the user's dashboard.

## How to work

1. Restate the question ("30-day usage", "which providers are configured").
2. Call the smallest read tool that answers it.
3. Explain routing awareness: OpenLLM routes across subscriptions/keys the user already pays for; a model row may name a provider and a chain hop. On failure, look for fallback-chain aliases rather than guessing vendors.
4. Mutations: state what changes, get approval, then call.
5. Browser fallback only when MCP/API genuinely lacks the surface (vault recovery, hosted checkout, 2FA-gated). Say so.

## Guardrails

- No secrets in repo, PR, logs, or shared skills.
- No vault reset or account deletion without explicit, consequence-confirmed instruction.
- Don't claim OpenLLM configured GitHub/Vercel — those are separate connectors.

## Done criteria

User has the facts (or the confirmed mutation) plus one line naming the MCP tool used. Offer: another dashboard query, or **openllm-dev-task**.
