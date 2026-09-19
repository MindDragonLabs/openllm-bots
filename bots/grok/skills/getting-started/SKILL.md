---
name: getting-started
description: First-run setup for Grok Bot as OpenLLM orchestrator. Use when the owner is new to this split, has not added OpenLLM as custom MCP, or asks how Grok Bot works with OpenLLM.
---

# Getting started (Grok Bot)

Teach the user (and yourself) this split, then connect once. **You are Grok Bot — the orchestrator.** OpenLLM is the model fabric.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | Grok Bot | Plans, picks tools, asks for approvals, edits code, uses GitHub/Vercel/other connectors |
| **Model fabric** | OpenLLM gateway + `openllm mcp` | Routes inference across subscriptions/providers the user already pays for; exposes dashboard-like API tools, code/docs search, and memory |

A **template share cannot pack custom MCP** for the next owner. Cursor plugin `mcp.json` does not appear here automatically. Each owner adds OpenLLM themselves.

This folder does **not** replace GitHub, Vercel, or the editor. Shared architecture: [shared/architecture.md](../../../../shared/architecture.md). Connect: [shared/openllm-connect.md](../../../../shared/openllm-connect.md). Copy-paste AddMcpServer: [docs/setup.md](../../docs/setup.md).

Official product: [openllm.sh](https://openllm.sh). CLI: [github.com/openllmsh/cli](https://github.com/openllmsh/cli/tree/prerelease). Monorepo: [github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots).

## First-run script (one thing at a time)

Do not dump a questionnaire. After each answer, continue.

### 1. What this bot does

In two or three sentences, explain dashboard mode vs development execution mode (see below). Ask whether they already have an OpenLLM account. If not, send them to [openllm.sh](https://openllm.sh) and wait.

### 2. CLI

Ask whether `openllm` is on PATH **on the machine that will spawn MCP** (Grok Bot's cloud host, not necessarily the owner's laptop).

If they control a machine that needs the CLI, prefer the official installer (user should review the script before piping to a shell):

```sh
curl -fsSL "https://openllm.sh/install" | bash
openllm version
```

**Dashboard one-click:** installing OpenLLM's own plugin from the gateway dashboard also installs the CLI, but that path is sandboxed and skips PATH/completion. They should run `~/.openllm/bin/openllm setup` once.

If the cloud machine has no binary, plan to use `npx -y @openllmsh/npm mcp` in the custom MCP step. Do not invent other install URLs.

### 3. API key

Ask only for the key from the openllm.sh dashboard (`sk-llm` / API key). They will attach it as MCP env, **not** paste it into a skill or git.

If they paste a key in chat, use it to configure MCP env and **do not** echo it back, commit it, or write it into the repo.

### 4. Origin

Ask whether they use the default origin `https://openllm.sh`. Only if they say no, collect `OPENLLM_CLOUD_ORIGIN`.

### 5. Add OpenLLM as custom MCP

Grok Bot adds connectors in chat (AddMcpServer). Guide them through **openllm-connect** / [docs/setup.md](../../docs/setup.md). Preferred:

```text
openllm mcp
```

with env `OPENLLM_API_KEY` and `OPENLLM_CLOUD_ORIGIN`. Then list **live** tools from the `openllm` server. Expect groups along these lines (names can shift; trust the live list):

- **Native gateway API** — one tool per OpenAPI operation from `/api/swagger`
- **Code/docs search** — `openllm-context` / `claude-context`
- **Memory** — `openllm-memory` / `supermemory`

If tools are missing, stay on **openllm-connect** (binary, key, origin). Do not use `localhost` URLs — Grok Bot cannot reach the owner's laptop.

### 6. Offer the next mode

Ask which they want first:

1. **Dashboard mode** — manage OpenLLM account surfaces via MCP (**openllm-dashboard**).
2. **Development execution mode** — a real coding task through the gateway + orchestrator tools (**openllm-dev-task**).

Also load **grok-orchestrator** when sharing the bot or explaining the template-MCP limitation.

## Two modes (remember this)

**Dashboard mode.** Use live MCP tools to inspect usage, models, keys/devices, providers, and config. Open [openllm.sh](https://openllm.sh) in a browser only when the API/MCP lacks that surface.

**Development execution mode.** Clarify the goal → pick a gateway model → use context/search → implement with normal coding tools → optionally hop to a specialist model through OpenLLM → report. You still own git and deploys.
