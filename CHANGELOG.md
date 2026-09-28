# Changelog

All notable changes to this monorepo are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- README: Harness survey section linking docs/harness-survey.md, now itemizing all 23 harnesses by verdict.
- Harness investigation program: audit of coding-agent CLIs for OpenLLM model-fabric attachment. Results land under `bots/` as each harness is verified.
- Six new ready bots, all verified live 2026-09-28 against a local OpenLLM gateway (macOS arm64):
  - **Claude Code** (`bots/claude`) — `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN` attach, claude 2.1.282.
  - **Codex CLI** (`bots/codex`) — `model_providers` block with Responses wire API, codex 0.157.0. Previous "BLOCKED" verdict superseded.
  - **OpenCode** (`bots/opencode`) — `@ai-sdk/openai-compatible` provider in `opencode.json`, opencode 1.15.7.
  - **Pi** (`bots/pi`) — custom provider in `~/.pi/agent/models.json`, pi 0.73.1.
  - **MiniMax Code** (`bots/mcode`) — `mcode provider add --api-format anthropic-messages`, mcode 0.4.12.
  - **ZCode** (`bots/zcode`) — `~/.zcode/v2/provider_config.json` provider rule + manual model rules + default selection, zcode-app-cli 3.14.3-28.
- Each bot folder ships `README.md`, `bot.manifest.json`, and `docs/setup.md` with copy-paste attach steps and a troubleshooting table.

### Changed

- Audit follow-ups (Opus 5.5 review): survey table now carries the three MCP bots (Hermes, Cursor plugin, Grok Bot) as numbered rows so README counts reconcile row-by-row (12 live · 2 gated · 9 pending = 23); mmx/CommandCode/Claude Squad moved to an "adjacent tools" section. Added "Gateway endpoints" section to shared/openllm-connect.md (local daemon vs hosted origin, /v1 vs root rule, loopback auth caveat); per-host table covers all ten bots. OpenCode key guidance switched to the documented `{env:OPENLLM_API_KEY}` options form. Codex setup now says where top-level keys go in config.toml (before any `[table]`). zcode README snippet includes the kimi manual rule. Pi docs aligned to grok-4.7 (re-verified live). Claude Code docs use a gateway-catalog model-id placeholder instead of an invented id, and recommend a wrapper script over `.env`. Architecture doc shows the base-URL attach path alongside MCP.
- All OpenLLM CLI links point at the prerelease branch: `https://github.com/openllmsh/cli/tree/prerelease` (8 files).
- Harness survey expanded from 18 to 23 harnesses; codex verdict updated BLOCKED → LIVE (Responses wire API + `web_search = "disabled"`), opencode pending → LIVE, zcode added as LIVE. [docs/harness-survey.md](./docs/harness-survey.md).
- README rebuilt: badge row, table of contents, 10-bot table with attach methods and verification dates, per-harness quick starts, "Which attach method?" matrix. [README.md](./README.md).
- CONTRIBUTING host enum extended: `claude-code | codex | opencode | pi | mcode | zcode` join the list.


### Fixed

- Devin follow-ups — Muse CLI auth/usage/latency/URL checks; fix OpenLLM install URL; Hermes CLI version check.

### Merged (from PR #3 and PR #2)

- **Hermes** (`bots/hermes`, status: ready) — Hermes Agent as orchestrator. `hermes mcp add` stdio setup docs (verified against openllm CLI 2.6.36 / 43 tools), plus five skills: `getting-started`, `hermes-orchestrator`, `openllm-connect`, `openllm-dashboard`, `openllm-dev-task`. Documents two `hermes mcp add` pitfalls: `--args` must come last (it swallows trailing flags into `args`), and the tool-enable prompt needs stdin when scripted.
- Port Muse×OpenLLM integration from Drive into [`bots/muse`](./bots/muse) (status: ready). Emulated workspace skill + Secure Vault against openllm.sh, with a path to the official Muse connector directory.

## [0.1.0] — 2026-09-19

(No git tag exists yet; link refs restored when the first tag is cut.)

### Added

- Monorepo layout: `shared/` plus one folder per orchestrator under `bots/`.
- Shared architecture, OpenLLM connect docs, stdio MCP example, and abstract mark.
- **Grok Bot** (`bots/grok`, status: ready) — Grok-oriented skills and AddMcpServer setup docs. Emphasizes that a template share cannot pack custom MCP.
- **Cursor** (`bots/cursor`, status: ready) — Cursor plugin `openllm-orchestrator-cursor` (stdio `openllm mcp`, skills, rule, commands). Ported from [grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator).
- Root `.cursor-plugin/marketplace.json` listing `bots/cursor` so this repo can be a multi-plugin marketplace source.
- **Muse** and **Hermes** stub folders (same OpenLLM fabric; no fake skills).
- MIT license, contributing guide, and [MIGRATION.md](./MIGRATION.md).
