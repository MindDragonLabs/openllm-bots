# Hermes (stub)

This folder is **reserved** for the **Hermes** orchestrator.

Hermes (when published) is the orchestrator. [OpenLLM](https://openllm.sh) is the **same model fabric** as every other bot in this monorepo: `openllm mcp`, variables `OPENLLM_API_KEY` and `OPENLLM_CLOUD_ORIGIN`.

There are **no skills or MCP configs here yet**. Do not treat this directory as an installable bot.

Status: `stub` — see [`bot.manifest.json`](./bot.manifest.json).

## Shared docs (use these now)

- [Architecture](../../shared/architecture.md) — orchestrator vs OpenLLM
- [OpenLLM connect](../../shared/openllm-connect.md) — CLI install, env vars, remote MCP rules
- [stdio MCP example](../../shared/mcp.stdio.example.json)

Ready bots today: [Grok](../grok), [Cursor](../cursor). How to fill this folder later: [CONTRIBUTING.md](../../CONTRIBUTING.md).
