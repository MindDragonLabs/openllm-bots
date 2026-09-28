# openllm-bots

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Bots](https://img.shields.io/badge/bots-10-green.svg)](#bots)
[![Harnesses surveyed](https://img.shields.io/badge/harnesses%20surveyed-23-blue.svg)](./docs/harness-survey.md)

**Standardized multi-bot repository: any coding-agent harness as orchestrator, [OpenLLM](https://openllm.sh) as the shared model fabric.**

Every orchestrator bot lives in its own folder under `bots/`. Each one keeps its own planning, tools, approvals, and file/git access. Base-URL bots route their inference through one OpenLLM gateway; MCP bots call it for catalog, completions hops, search, and memory — so your models, subscriptions, and accounting live in one place either way.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | The harness (Claude Code, Codex, OpenCode, Hermes, …) | Plans, tools, approvals, code, GitHub/Vercel/… |
| **Model fabric** | OpenLLM gateway (`openllm mcp` or OpenAI/Anthropic-compat endpoints) | Models, completions, account API, context, memory |

```text
Orchestrator  =  the bot (its own tools and judgment)
Model fabric  =  OpenLLM gateway + MCP (one endpoint for every model you use)
```

Details and diagram: [shared/architecture.md](./shared/architecture.md). Connect concepts (CLI, env, remote MCP rules): [shared/openllm-connect.md](./shared/openllm-connect.md).

This layout replaces the flat plugin at [MindDragonLabs/grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator). See [MIGRATION.md](./MIGRATION.md).

## Contents

- [Bots](#bots)
- [Quick start](#quick-start)
- [Which attach method?](#which-attach-method)
- [Harness survey](#harness-survey--all-23-harnesses)
- [Adding a bot](#adding-a-bot)
- [Scope](#in-scope--out-of-scope)
- [Links](#links)
- [License](#license)

## Bots

| id | host | status | attach | path |
| --- | --- | --- | --- | --- |
| `claude` | Claude Code | ready · verified 2026-09-28 | Anthropic-compat base URL | [`bots/claude`](./bots/claude) |
| `codex` | Codex CLI | ready · verified 2026-09-28 | Responses-API provider block | [`bots/codex`](./bots/codex) |
| `opencode` | OpenCode | ready · verified 2026-09-28 | `@ai-sdk/openai-compatible` | [`bots/opencode`](./bots/opencode) |
| `pi` | Pi | ready · verified 2026-09-28 | `models.json` custom provider | [`bots/pi`](./bots/pi) |
| `mcode` | MiniMax Code | ready · verified 2026-09-28 | `anthropic-messages` custom provider | [`bots/mcode`](./bots/mcode) |
| `zcode` | ZCode | ready · verified 2026-09-28 | `provider_config.json` rule | [`bots/zcode`](./bots/zcode) |
| `grok` | Grok Bot | ready | `openllm mcp` (custom MCP in chat) | [`bots/grok`](./bots/grok) |
| `cursor` | Cursor | ready | `openllm mcp` (plugin `mcp.json`) | [`bots/cursor`](./bots/cursor) |
| `hermes` | Hermes Agent | ready | `openllm mcp` (`hermes mcp add`) | [`bots/hermes`](./bots/hermes) |
| `muse` | Muse | ready | emulated skill + Secure Vault | [`bots/muse`](./bots/muse) |

`status` is `ready`, `stub`, or `experimental` (see each `bot.manifest.json`). "Verified" means a real completion was routed through an OpenLLM gateway on the date shown. Verification ran on a loopback gateway that does not enforce request auth — it proves routing, not key transport; see [docs/harness-survey.md](./docs/harness-survey.md) for the method note.

## Quick start

Pick your harness. Every path needs an [OpenLLM](https://openllm.sh) account, an API key, and a running gateway — see [Gateway endpoints](./shared/openllm-connect.md#gateway-endpoints) for the local daemon (`http://127.0.0.1:8787`) and the hosted origin.

### Claude Code

```sh
export ANTHROPIC_BASE_URL="http://127.0.0.1:8787"    # gateway root, no /v1
export ANTHROPIC_AUTH_TOKEN="$OPENLLM_API_KEY"
unset ANTHROPIC_API_KEY
claude -p --model <model-id-from-your-gateway> "Reply with exactly: OPENLLM-OK"
```

Full setup: [bots/claude/docs/setup.md](./bots/claude/docs/setup.md)

### Codex CLI

```toml
# ~/.codex/config.toml
model = "grok/grok-4.7"
model_provider = "openllm"
model_reasoning_effort = "low"
web_search = "disabled"

[model_providers.openllm]
name = "OpenLLM"
base_url = "http://127.0.0.1:8787/v1"
env_key = "OPENLLM_API_KEY"
wire_api = "responses"
```

Full setup: [bots/codex/docs/setup.md](./bots/codex/docs/setup.md)

### OpenCode

The project `opencode.json`:

```jsonc
{
  "provider": {
    "openllm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "OpenLLM",
      "options": { "baseURL": "http://127.0.0.1:8787/v1", "apiKey": "{env:OPENLLM_API_KEY}" },
      "models": { "grok/grok-4.7": { "name": "Grok 4.7 via OpenLLM" } }
    }
  }
}
```

Key: `options.apiKey` is `"{env:OPENLLM_API_KEY}"` — the reference resolves the exported variable at launch. Then: `opencode run --model 'openllm/grok/grok-4.7' "..."` (see bot docs for the full model list).

Full setup: [bots/opencode/docs/setup.md](./bots/opencode/docs/setup.md)

### Pi

Add an `openllm` provider to `~/.pi/agent/models.json` (`api: "openai-completions"`, `apiKey: "OPENLLM_API_KEY"` (bare variable name)), then `pi --model openllm/grok/grok-4.7 -p "..."` (verified live on 4.7; any id in your provider block works).

Full setup: [bots/pi/docs/setup.md](./bots/pi/docs/setup.md)

### MiniMax Code (mcode)

```sh
mcode provider add --name "OpenLLM" --base-url "http://127.0.0.1:8787" \
  --api-format anthropic-messages --model "grok/grok-4.7" --api-key-env OPENLLM_API_KEY
mcode exec --model "custom_provider:openllm/grok/grok-4.7" --permission off "..."  # more models: see bot docs
```

Full setup: [bots/mcode/docs/setup.md](./bots/mcode/docs/setup.md)

### ZCode

Edit `~/.zcode/v2/provider_config.json` — provider rule + manual model rules + `defaultModelSelection` (all three required). Full setup: [bots/zcode/docs/setup.md](./bots/zcode/docs/setup.md)

### Grok Bot

A template share cannot pack custom MCP — each owner adds OpenLLM in chat:

```text
Add a custom MCP server named openllm that runs: openllm mcp
Set environment:
- OPENLLM_API_KEY = (paste the key in the next message)
- OPENLLM_CLOUD_ORIGIN = https://openllm.sh
```

Full setup: [bots/grok/docs/setup.md](./bots/grok/docs/setup.md)

### Cursor

Plugin id `openllm-orchestrator-cursor` ([`.cursor-plugin/marketplace.json`](./.cursor-plugin/marketplace.json)). Install the plugin, set **Plugins → Configure**: `OPENLLM_API_KEY` (required), `OPENLLM_CLOUD_ORIGIN` (optional). Commands: `/setup-openllm`, `/openllm-dev-task`.

Full setup: [bots/cursor/README.md](./bots/cursor/README.md) · [bots/cursor/docs/setup.md](./bots/cursor/docs/setup.md)

### Hermes

```sh
hermes mcp add openllm --command openllm --connect-timeout 30 \
  --env 'OPENLLM_API_KEY=${OPENLLM_API_KEY}' 'OPENLLM_CLOUD_ORIGIN=${OPENLLM_CLOUD_ORIGIN}' \
  --args mcp
hermes mcp test openllm
```

Full setup: [bots/hermes/docs/setup.md](./bots/hermes/docs/setup.md)

### Muse

Muse attaches via an emulated workspace skill + Secure Vault key — not `openllm mcp`. Read [`bots/muse`](./bots/muse) in order (`docs/01-overview.md` … `docs/09-troubleshooting.md`).

## Which attach method?

| Your harness speaks… | Attach method | Endpoint shape | Used by |
| --- | --- | --- | --- |
| Anthropic Messages protocol | Anthropic-compat base URL / provider | gateway **root** (no `/v1`) | Claude Code, mcode |
| OpenAI chat completions | OpenAI-compat base URL / provider | gateway `/v1` | OpenCode, Pi, Aider, Crush, Goose, zcode |
| OpenAI Responses API | Responses provider block | gateway `/v1` | Codex |
| MCP (stdio) | `openllm mcp` | spawned by the host | Hermes, Cursor, Grok Bot |
| No native provider config | emulated skill + vault | CLI calls gateway | Muse |

Rules of thumb:

- **Never commit keys.** Env vars or the host's secret store, always.
- **Discover model ids live** (`curl <gateway>/v1/models`) — do not invent them.
- **Direct model ids beat chain aliases** for reliability (`grok/grok-4.7` over `ultra`).

## Harness survey — all 23 harnesses

[docs/harness-survey.md](./docs/harness-survey.md) tracks **all 23 harnesses** tested for OpenLLM attachment — verified live, blocked with reasons, or pending. The full table (versions, attach methods, verdicts) lives there; this is the summary.

**Live (12):**

| Harness | Attach | Bot folder |
| --- | --- | --- |
| Claude Code | Anthropic-compat base URL | [`bots/claude`](./bots/claude) |
| Codex CLI | Responses-API provider block | [`bots/codex`](./bots/codex) |
| OpenCode | `@ai-sdk/openai-compatible` | [`bots/opencode`](./bots/opencode) |
| Pi | `models.json` custom provider | [`bots/pi`](./bots/pi) |
| MiniMax Code | `anthropic-messages` custom provider | [`bots/mcode`](./bots/mcode) |
| ZCode | `provider_config.json` rule | [`bots/zcode`](./bots/zcode) |
| Goose | `GOOSE_PROVIDER=openai` + base URL | — |
| Aider | `--openai-api-base` | — |
| Crush | `crush.json` provider | — |
| Hermes | `openllm mcp` (stdio) | [`bots/hermes`](./bots/hermes) |
| Cursor | `openllm mcp` (plugin) | [`bots/cursor`](./bots/cursor) |
| Grok Bot | `openllm mcp` (custom MCP) | [`bots/grok`](./bots/grok) |

**Blocked / gated (2):** Gemini CLI (Google-protocol auth only), Qwen Code (reaches the gateway; tool schema rejected with 422).

**Pending / untested (9):** Cursor CLI, Devin CLI, Grok CLI, Kimi CLI, Amp, Plandex, Warp, Amazon Q Developer CLI, GitHub Copilot CLI.

The counts reconcile row-by-row against the survey table (12 + 2 + 9 = 23). Adjacent tools that are not OpenLLM client harnesses (mmx, CommandCode, Claude Squad) are tracked separately in the survey, alongside Muse ([`bots/muse`](./bots/muse)), which attaches via an emulated skill + Secure Vault rather than a gateway endpoint.

## Adding a bot

Create `bots/<name>/` with `README.md` + `bot.manifest.json`, link to `shared/`, and (for Cursor plugins) register in `.cursor-plugin/marketplace.json`. Step-by-step: [CONTRIBUTING.md](./CONTRIBUTING.md).

## In scope / out of scope

**In scope**

- Teaching the orchestrator vs model-fabric split
- Attaching harnesses to OpenLLM (MCP, base URLs, provider configs)
- Per-harness setup docs and pitfalls, verified against real gateways
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
- Harness survey: [docs/harness-survey.md](./docs/harness-survey.md)
- This monorepo: [https://github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots)
- Predecessor: [https://github.com/MindDragonLabs/grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator)
- Cursor plugins reference: [https://cursor.com/docs/reference/plugins](https://cursor.com/docs/reference/plugins)
- Publish: [https://cursor.com/marketplace/publish](https://cursor.com/marketplace/publish)

## License

[MIT](./LICENSE) © 2026 MindDragonLabs
