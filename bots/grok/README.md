# Grok Bot

**Orchestrator:** Grok Bot  
**Model fabric:** [OpenLLM](https://openllm.sh) via `openllm mcp`  
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json))

Grok Bot plans and coordinates. OpenLLM routes inference and exposes gateway MCP tools. GitHub, Vercel, and other apps stay on their own connectors.

A **Grok Bot template share cannot pack custom MCP** for the next owner. Each owner adds OpenLLM themselves. This folder does not ship API keys or guessed remote MCP URLs.

## Shared docs

- [Architecture](../../shared/architecture.md) — role split + diagram
- [OpenLLM connect](../../shared/openllm-connect.md) — CLI, env vars, remote MCP rules
- [stdio MCP example](../../shared/mcp.stdio.example.json)

## This folder

| Path | Purpose |
| --- | --- |
| [docs/setup.md](./docs/setup.md) | Copy-paste AddMcpServer for Grok Bot |
| [skills/getting-started](./skills/getting-started/SKILL.md) | First run |
| [skills/openllm-connect](./skills/openllm-connect/SKILL.md) | Pairing and troubleshooting |
| [skills/openllm-dashboard](./skills/openllm-dashboard/SKILL.md) | Account surfaces via MCP |
| [skills/openllm-dev-task](./skills/openllm-dev-task/SKILL.md) | Coding tasks |
| [skills/grok-orchestrator](./skills/grok-orchestrator/SKILL.md) | Grok Bot playbook |

Import these `SKILL.md` files into Grok Bot skills (or install the Cursor plugin in [`../cursor`](../cursor) when you also use Cursor).

## Attach OpenLLM

Preferred stdio (cloud machine must be able to spawn `openllm` or `npx`):

```text
Add a custom MCP server named openllm that runs: openllm mcp
Set environment:
- OPENLLM_API_KEY = (I will paste the key in the next message)
- OPENLLM_CLOUD_ORIGIN = https://openllm.sh
```

Full copy-paste blocks, npm launcher, and dashboard-only remote URL: [docs/setup.md](./docs/setup.md).

## Sibling bots

Cursor plugin: [`../cursor`](../cursor). Muse: [`../muse`](../muse) (emulated skill + Secure Vault). Hermes: stub ([`../hermes`](../hermes)).
