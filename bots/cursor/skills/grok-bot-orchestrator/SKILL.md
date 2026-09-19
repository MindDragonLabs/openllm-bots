---
name: grok-bot-orchestrator
description: Grok Bot–specific playbook for using OpenLLM as model fabric while Grok Bot remains the orchestrator. Use when the user is on Grok Bot, sharing a bot, or adding OpenLLM as a custom connector.
---

# Grok Bot as orchestrator for OpenLLM

Grok Bot (or any Cursor agent) **plans and coordinates**. OpenLLM **routes inference** and exposes gateway MCP tools. GitHub, Vercel, and other apps stay on their own connectors.

Companion docs: [bots/grok/docs/setup.md](../../../grok/docs/setup.md), [shared/architecture.md](../../../../shared/architecture.md). Dedicated Grok skills: [`bots/grok/skills`](../../../grok/skills) (including `grok-orchestrator`).

## What Grok Bot cannot pack for you

- A **bot template share does not include another owner's custom MCP servers.** New owners must add OpenLLM themselves.
- This Cursor plugin's `mcp.json` / stdio server **does not automatically appear** on Grok Bot. Re-add the connector there.
- Grok Bot **cannot call localhost** on the user's laptop. Do not use `http://127.0.0.1:…` as the MCP URL.

Marketplace install of **this** plugin (once listed) can still give Grok Bot the skills, rules, and — if the client can spawn stdio — `openllm mcp`. Treat custom-connector setup as required until tools actually list.

## New owner checklist

Do these in order. One question at a time if a secret or URL is missing.

1. **Keep product connectors.** GitHub, Vercel, Slack, etc. stay connected. Do not remove them “because OpenLLM is the gateway.”
2. **Add OpenLLM as a custom MCP** (chat-driven AddMcpServer — there is often no settings form). Confirm name `openllm`.
   - Stdio: `openllm mcp` with env `OPENLLM_API_KEY` and optional `OPENLLM_CLOUD_ORIGIN=https://openllm.sh`.
   - If the binary is missing on the cloud machine: `npx -y @openllmsh/npm mcp` with the same env.
   - If the OpenLLM dashboard shows a **remote MCP/SSE URL**, add that URL with `Authorization: Bearer <OPENLLM_API_KEY>`. Never invent the URL.
3. **Import skills** from [this monorepo](https://github.com/MindDragonLabs/openllm-bots) — prefer [`bots/grok/skills`](../../../grok/skills) — or paste the prose into Grok Bot skills. Minimum set: `getting-started`, `openllm-connect`, `openllm-dashboard`, `openllm-dev-task`, plus `grok-orchestrator` (Grok folder) or this skill.
4. **Verify** a non-zero tool count on `openllm`, then run a read-only models or usage call.
5. **Optional future:** a public Grok Bot template that *references this repo* for skills. It still will not ship the owner's API key or skip step 2.

## Role split (say this when the user is confused)

```text
Grok Bot  →  orchestrator (plan, tools, approvals, GitHub/Vercel, code edits)
OpenLLM   →  model fabric (gateway + MCP: models, completions, search, memory)
```

When a specialist model hop helps, Grok Bot calls OpenLLM chat/completions (live tool), then applies the result with its own editor/shell.

## Copy-paste chat lines

Stdio:

```text
Add a custom MCP server named openllm that runs: openllm mcp
Use environment OPENLLM_API_KEY=<the user will paste next> and OPENLLM_CLOUD_ORIGIN=https://openllm.sh
Do not store the key in a skill file or git.
```

npm launcher:

```text
Add a custom MCP server named openllm that runs: npx -y @openllmsh/npm mcp
Same environment variables as above.
```

Remote (placeholders only):

```text
Add a custom MCP server named openllm at <PASTE_URL_FROM_OPENLLM_DASHBOARD>
Header: Authorization: Bearer <PASTE_OPENLLM_API_KEY>
```

## Operating rules on Grok Bot

- Attach `@openllm` (or the server's attach control) when the task needs gateway tools.
- Dashboard questions → **openllm-dashboard**. Implementation → **openllm-dev-task**.
- Approvals: mutating keys, providers, billing, or vault stays user-confirmed.
- Never put secrets in a skill you might later share with the template.

## Sharing a bot

When someone clones or copies the bot, send them:

1. This monorepo: [https://github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots)
2. [openllm.sh](https://openllm.sh) for their own account and key
3. The custom-MCP paragraph above

Their traffic uses **their** OpenLLM account. Yours is not included.
