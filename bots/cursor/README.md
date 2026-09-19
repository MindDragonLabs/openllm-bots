# Cursor agent

**Orchestrator:** Cursor agent  
**Model fabric:** [OpenLLM](https://openllm.sh) via `openllm mcp`  
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json))  
**Plugin id:** `openllm-orchestrator-cursor`

This folder is a Cursor plugin. The agent plans and coordinates. OpenLLM is the gateway + MCP. GitHub, Vercel, and other connectors stay yours.

Homepage / source: [github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots). The monorepo marketplace manifest at [`.cursor-plugin/marketplace.json`](../../.cursor-plugin/marketplace.json) lists this directory as `source: bots/cursor`.

## Shared docs

- [Architecture](../../shared/architecture.md)
- [OpenLLM connect](../../shared/openllm-connect.md)
- [stdio MCP example](../../shared/mcp.stdio.example.json)

## Install

1. OpenLLM account + CLI (review, then run):

   ```sh
   curl -fsSL "https://openllm.sh/install" | bash
   openllm version
   ```

2. Install this plugin:

   - **Marketplace** (when listed): Customize → Plugins / Marketplace → **OpenLLM Orchestrator (Cursor)** (`openllm-orchestrator-cursor`).
   - **This repo as a marketplace source:** team marketplace pointing at [MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots).
   - **Local (development):** copy **this folder** (`bots/cursor`) to `~/.cursor/plugins/local/openllm-orchestrator-cursor`. It must live **inside** `~/.cursor/plugins/local`; Cursor skips symlinks that point elsewhere. Restart Cursor or **Developer: Reload Window**.

   On Teams/Enterprise, local plugin imports may be admin-gated.

3. **Plugins → Configure:** `OPENLLM_API_KEY` (required), `OPENLLM_CLOUD_ORIGIN` (optional, default `https://openllm.sh`). Values substitute into [`mcp.json`](./mcp.json). Never commit them.

4. Confirm the `openllm` MCP server is running.

Step-by-step: [docs/setup.md](./docs/setup.md).

## Layout

```text
.cursor-plugin/plugin.json
mcp.json
skills/          getting-started, openllm-connect, openllm-dashboard,
                 openllm-dev-task, grok-bot-orchestrator
rules/           openllm-orchestrator.mdc
commands/        setup-openllm, openllm-dev-task
docs/            setup.md
assets/logo.svg
```

Commands: `/setup-openllm`, `/openllm-dev-task`.

## Grok Bot users

Cursor `mcp.json` is **not** copied onto Grok Bot. Add OpenLLM as a custom MCP and use [../grok/docs/setup.md](../grok/docs/setup.md). Skill in this plugin: `grok-bot-orchestrator`. Dedicated Grok folder: [../grok](../grok).

## Variables

Declared in `.cursor-plugin/plugin.json`, substituted into `mcp.json`:

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENLLM_API_KEY` | yes | — | Dashboard API key |
| `OPENLLM_CLOUD_ORIGIN` | no | `https://openllm.sh` | Gateway origin (host origin, not a `/v1` path) |
