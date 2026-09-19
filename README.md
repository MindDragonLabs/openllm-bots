# openllm-bots

**Standardized multi-bot repository** for orchestrators that share one model fabric.

Each orchestrator bot (Grok, Muse, Cursor, Hermes, …) lives in its own folder. They all use [OpenLLM](https://openllm.sh) as the model fabric. Grok and Cursor attach via `openllm mcp`; Muse uses an emulated workspace skill + Secure Vault (see [`bots/muse`](./bots/muse)).

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | The bot (Grok Bot / Muse / Cursor agent / Hermes / …) | Plans, tools, approvals, code, GitHub/Vercel/… |
| **Model fabric** | OpenLLM via `openllm mcp` | Models, completions, account API, context, memory |

```text
Orchestrator  =  the bot
Model fabric  =  OpenLLM gateway + MCP
```

Details and diagram: [shared/architecture.md](./shared/architecture.md). Connect (CLI, env, remote MCP rules): [shared/openllm-connect.md](./shared/openllm-connect.md).

This layout replaces the flat plugin at [MindDragonLabs/grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator). See [MIGRATION.md](./MIGRATION.md).

## Bots

| id | host | status | path | description |
| --- | --- | --- | --- | --- |
| `grok` | grok-bot | ready | [`bots/grok`](./bots/grok) | Grok Bot orchestrates; OpenLLM via `openllm mcp` |
| `cursor` | cursor | ready | [`bots/cursor`](./bots/cursor) | Cursor plugin; OpenLLM via `openllm mcp` |
| `muse` | muse | ready | [`bots/muse`](./bots/muse) | Muse orchestrates OpenLLM via emulated skill + Secure Vault |
| `hermes` | hermes | ready | [`bots/hermes`](./bots/hermes) | Hermes Agent orchestrates; OpenLLM via `hermes mcp add` (stdio `openllm mcp`) |

`status` is `ready`, `stub`, or `experimental` (see each `bot.manifest.json`).

## Quick start — Grok Bot

Grok Bot is the orchestrator. A **template share cannot pack custom MCP** — each owner adds OpenLLM themselves.

1. Review, then install the CLI:

   ```sh
   curl -fsSL "https://openllm.sh/api/setup/cli/install.sh" | bash
   openllm version
   ```

2. In Grok Bot chat, add a custom MCP (do not paste the key into a skill file):

   ```text
   Add a custom MCP server named openllm that runs: openllm mcp
   Set environment:
   - OPENLLM_API_KEY = (I will paste the key in the next message)
   - OPENLLM_CLOUD_ORIGIN = https://openllm.sh
   ```

3. Import skills from [`bots/grok/skills/`](./bots/grok/skills/).

Copy-paste and verification: [bots/grok/docs/setup.md](./bots/grok/docs/setup.md). Skill: [`grok-orchestrator`](./bots/grok/skills/grok-orchestrator/SKILL.md).

## Quick start — Cursor

Plugin id: `openllm-orchestrator-cursor` (listed in [`.cursor-plugin/marketplace.json`](./.cursor-plugin/marketplace.json)).

1. Install the CLI (same command as above).
2. Install the plugin from Customize → Plugins / Marketplace when listed, **or** copy [`bots/cursor`](./bots/cursor) to `~/.cursor/plugins/local/openllm-orchestrator-cursor` (folder must live inside `~/.cursor/plugins/local`; Cursor skips symlinks that point elsewhere), **or** add this repository as a team marketplace source.
3. Set **Plugins → Configure**: `OPENLLM_API_KEY` (required), `OPENLLM_CLOUD_ORIGIN` (optional, default `https://openllm.sh`).
4. Confirm the `openllm` MCP server is running.

Full Cursor setup: [bots/cursor/README.md](./bots/cursor/README.md) and [bots/cursor/docs/setup.md](./bots/cursor/docs/setup.md). Commands: `/setup-openllm`, `/openllm-dev-task`.

Submit/update a marketplace listing: [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish).

## Quick start — Hermes

Hermes is the orchestrator. Attach OpenLLM as a stdio MCP server on the Hermes host (per profile; the key goes in the profile `.env`, not git):

```sh
hermes mcp add openllm --command openllm --connect-timeout 30 \
  --env 'OPENLLM_API_KEY=${OPENLLM_API_KEY}' 'OPENLLM_CLOUD_ORIGIN=${OPENLLM_CLOUD_ORIGIN}' \
  --args mcp
hermes mcp test openllm
```

Then import skills from [`bots/hermes/skills/`](./bots/hermes/skills/).

Full setup with pitfalls: [bots/hermes/docs/setup.md](./bots/hermes/docs/setup.md).

## Quick start — Muse

Muse is the orchestrator. OpenLLM ([openllm.sh](https://openllm.sh)) is the model fabric, attached via an **emulated workspace skill** and a Secure Vault key — not `openllm mcp`.

Read [`bots/muse`](./bots/muse) in order (`docs/01-overview.md` … `docs/09-troubleshooting.md`). Templates: [`bots/muse/templates`](./bots/muse/templates). Sample flows: [`bots/muse/examples/sample-flows.md`](./bots/muse/examples/sample-flows.md).

## Adding a bot

Create `bots/<name>/` with `README.md` + `bot.manifest.json`, link to `shared/`, and (if it is a Cursor plugin) register it in `.cursor-plugin/marketplace.json`. Step-by-step: [CONTRIBUTING.md](./CONTRIBUTING.md).

## In scope / out of scope

**In scope**

- Teaching the orchestrator vs model-fabric split
- Connecting official `openllm mcp` (Grok, Cursor)
- Muse emulated workspace skill + Secure Vault against openllm.sh
- Per-host skills and setup docs
- Dashboard-like account work and development tasks through the gateway

**Out of scope**

- Replacing GitHub, Vercel, or other product MCP servers
- Shipping API keys, remote MCP URLs we do not control, or a second application
- Inventing OpenLLM tool names (always discover from the connected server)
- Claiming OpenLLM stores or deploys your git repo
- Fake skills in stub bot folders

## Links

- OpenLLM: [https://openllm.sh](https://openllm.sh)
- OpenLLM CLI: [https://github.com/openllmsh/cli/tree/prerelease](https://github.com/openllmsh/cli/tree/prerelease)
- This monorepo: [https://github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots)
- Predecessor: [https://github.com/MindDragonLabs/grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator)
- Cursor plugins reference: [https://cursor.com/docs/reference/plugins](https://cursor.com/docs/reference/plugins)
- Publish: [https://cursor.com/marketplace/publish](https://cursor.com/marketplace/publish)

## License

[MIT](./LICENSE) © 2026 MindDragonLabs
