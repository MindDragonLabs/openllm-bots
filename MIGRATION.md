# Migration from grok-openllm-orchestrator

This monorepo **replaces** the flat plugin layout in [MindDragonLabs/grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator).

Readers and clones of that repository should come **here**: [https://github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots).

The predecessor should redirect (README banner, GitHub archive notice, or HTTP redirect) so new work lands in per-bot folders instead of a single plugin at the repo root.

## Why

One repo per orchestrator does not scale. Grok Bot, Cursor, Muse, Hermes, and future hosts all need the same OpenLLM fabric (`openllm mcp`) but different attach stories, skills, and manifests. This tree is:

```text
shared/     architecture + connect (every bot links here)
bots/<id>/  one orchestrator each
```

## Path map

| Old (grok-openllm-orchestrator) | New (openllm-bots) |
| --- | --- |
| `.cursor-plugin/plugin.json` | [`bots/cursor/.cursor-plugin/plugin.json`](./bots/cursor/.cursor-plugin/plugin.json) (id `openllm-orchestrator-cursor`) |
| `mcp.json` | [`bots/cursor/mcp.json`](./bots/cursor/mcp.json) and [`shared/mcp.stdio.example.json`](./shared/mcp.stdio.example.json) |
| `skills/` | [`bots/cursor/skills/`](./bots/cursor/skills/) (Cursor plugin) and Grok-oriented copies in [`bots/grok/skills/`](./bots/grok/skills/) |
| `skills/grok-bot-orchestrator/` | [`bots/grok/skills/grok-orchestrator/`](./bots/grok/skills/grok-orchestrator/) (also kept under Cursor as `grok-bot-orchestrator`) |
| `rules/` | [`bots/cursor/rules/`](./bots/cursor/rules/) |
| `commands/` | [`bots/cursor/commands/`](./bots/cursor/commands/) |
| `docs/architecture.md` | [`shared/architecture.md`](./shared/architecture.md) |
| `docs/grok-bot.md` | [`bots/grok/docs/setup.md`](./bots/grok/docs/setup.md) |
| `assets/logo.svg` | [`shared/logo.svg`](./shared/logo.svg) (plugin copy: [`bots/cursor/assets/logo.svg`](./bots/cursor/assets/logo.svg)) |
| Root README / plugin id `openllm-orchestrator` | [README.md](./README.md) plus marketplace entry in [`.cursor-plugin/marketplace.json`](./.cursor-plugin/marketplace.json) |

Variables are unchanged: `OPENLLM_API_KEY` and `OPENLLM_CLOUD_ORIGIN` (default `https://openllm.sh`). Stdio remains `openllm mcp`. No new secrets and no invented remote MCP URLs.

## What to do if you cloned the old repo

1. Clone or switch to this repository.
2. **Cursor:** install from `bots/cursor` (or add this repo as a marketplace source). Local copy goes to `~/.cursor/plugins/local/openllm-orchestrator-cursor`.
3. **Grok Bot:** follow [bots/grok/docs/setup.md](./bots/grok/docs/setup.md). You still add OpenLLM yourself; a template share cannot pack custom MCP.
4. Update any bookmarks that pointed at grok-openllm-orchestrator skills paths.
