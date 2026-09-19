---
name: hermes-orchestrator
description: Hermes-specific playbook for using OpenLLM as model fabric while Hermes stays the orchestrator. Use when working with mcp_openllm tools, choosing between Hermes-native and OpenLLM tools, or explaining the split.
---

# Hermes as orchestrator for OpenLLM

Hermes **plans and coordinates**. OpenLLM **routes inference** and exposes gateway MCP tools. Hermes' own terminal/file/git/web tools and its other MCP servers (GitHub, Vercel, …) stay exactly as they are.

Companion docs: [docs/setup.md](../../docs/setup.md), [shared/architecture.md](../../../../shared/architecture.md), [shared/openllm-connect.md](../../../../shared/openllm-connect.md).

## Role split (say this when the user is confused)

```text
Hermes   →  orchestrator (plan, tools, approvals, terminal/git, code edits)
OpenLLM  →  model fabric (gateway + MCP: models, completions, search, memory)
```

## Tool naming and dispatch

- OpenLLM tools surface as `mcp_openllm_<name>` (e.g. `mcp_openllm_api_v1Models_list`, `mcp_openllm_search_code`, `mcp_openllm_recall`).
- Three groups to expect (labels shift between CLI versions — trust the live list): **native gateway API** (one tool per OpenAPI operation), **code/docs search**, **memory**.
- Never invent tool names. If a group is missing, reconnect (**openllm-connect**) instead of guessing parameters.

## Choose the right tool

| Need | Use |
| --- | --- |
| Shell, files, git, gh, web fetch | Hermes-native tools — not OpenLLM |
| Model catalog / inference hop | `mcp_openllm_api_v1Models_list` → `mcp_openllm_api_v1ChatCompletions_chatCompletions` (or `/v1/messages`, `/v1/responses`) |
| Concept-level code or docs lookup | `mcp_openllm_search_code` / `mcp_openllm_search_docs` (index first with `index_codebase` / `index_docs`) |
| Cross-session memory | `mcp_openllm_memory` / `mcp_openllm_recall` — do not store secrets there |
| Account/usage questions | **openllm-dashboard** skill |

## Operating rules

- Attach the server per profile; tools load at session start (new session or `/reload-mcp` after changes).
- Mutating calls (billing, keys, credentials, vault) stay user-approved. Read-only first.
- Specialist hop = tight prompt + relevant snippets, never the whole repo. You apply or reject the output yourself.
- Never put `OPENLLM_API_KEY` in source, logs, or shared skills.

## Sharing this setup

Point another Hermes owner at [openllm-bots](https://github.com/MindDragonLabs/openllm-bots) `bots/hermes/`, their own openllm.sh account, and [docs/setup.md](../../docs/setup.md). Their traffic uses their account.
