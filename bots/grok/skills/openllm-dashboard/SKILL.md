---
name: openllm-dashboard
description: Use OpenLLM MCP tools for dashboard-like account work (models, usage, keys/devices, providers, config). Use when the Grok Bot user asks to inspect or manage their OpenLLM account without relying on the web UI.
---

# OpenLLM dashboard mode

Manage OpenLLM **account surfaces through MCP**, not by clicking around [openllm.sh](https://openllm.sh) first.

You (Grok Bot) are still the orchestrator. OpenLLM exposes a native gateway API as MCP tools (one tool per OpenAPI operation from `/api/swagger`). **Use the live tool list.** The operation ids below are from the public CLI-embedded spec so you can *recognize* surfaces — they are not a promise of exact MCP function names.

If MCP is not connected, **openllm-connect** and [docs/setup.md](../../docs/setup.md). Shared architecture: [shared/architecture.md](../../../../shared/architecture.md).

## Before you start

1. Confirm the `openllm` MCP server is connected. If not, **openllm-connect**.
2. List tools. Group them mentally into: gateway/account API, code/docs search, memory.
3. Prefer read operations unless the user asked to change something (rename a key, update config, add a custom provider).

## Surfaces to look for

Map user language to API areas, then pick the matching **live** tool.

| User intent | Upstream area (OpenAPI) | Notes |
| --- | --- | --- |
| What models can I call? | `GET /v1/models` (`v1Models.list`) | Account-enabled catalog, including chain aliases. Do not invent model ids. |
| Usage, tokens, recent requests | `/stats`, `/stats/requests`, `/stats/requests/items`, `/stats/keys/{id}` | Dashboard “overview” analogue. Summarize; do not dump huge request logs unless asked. |
| API keys, devices | `/keys`, `/keys/{id}`, `/keys/{id}/device-access` | **Conceptual** keys/devices. Never display full secret material. Confirm before create/delete/reset. |
| Providers / credentials | `/credentials`, `/providers/custom` | Provider and fallback awareness. Treat credential blobs as secret. Prefer status/list over rewrite. |
| Config | `/config/user`, `/config/global` | Read first. Explain diffs before `updateUser`. |
| Billing plan | `/billing`, `/billing/history` | If MCP cannot complete checkout/portal, fall back to the website. |
| Account profile | `/user` | Identity only — no secrets. |
| Search the web/docs via gateway | `POST /v1/search` | Dev-adjacent; still a gateway op. |
| Context plugin / memory plugin health | `/plugins/claude-context/…`, `/plugins/supermemory/…` | Same family as MCP groups `openllm-context` / `openllm-memory` (also called claude-context / supermemory). |

Public marketing index (`/public/usage-index`) is **not** the user's private dashboard. Do not mix it up with `/stats`.

## How to work

1. Restate the dashboard question (“show 30-day usage”, “list models”, “which providers are configured”).
2. Call the smallest read tool that answers it.
3. Explain provider/fallback **awareness**: OpenLLM routes across subscriptions and keys the user already pays for; a model row may name a provider and a chain hop. If a call fails, look for fallback-chain aliases in the catalog rather than guessing new vendors.
4. For mutations: say what will change, get approval, then call the tool.
5. **Browser fallback:** open [openllm.sh](https://openllm.sh) only when the live MCP/API cannot expose that surface (vault recovery UX, hosted checkout, something 2FA-gated). Say so explicitly.

## Guardrails

- Never paste provider API keys, vault recovery phrases, or raw `sk-llm` secrets into the repo, a PR, or a shared skill.
- Do not run vault reset (`/vault/reset/…`) or account deletion unless the user is explicit and you have confirmed consequences.
- Do not claim you “configured GitHub/Vercel via OpenLLM.” Those stay on their own connectors.
- If a tool errors because the surface is UI-only, stop inventing parameters and use the website.

## Done criteria

The user has the facts they asked for (or the mutation confirmed), plus a one-line pointer to which MCP tool you used. Offer a follow-up: another dashboard query, or switch to **openllm-dev-task**.
