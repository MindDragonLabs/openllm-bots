# Changelog

All notable changes to this monorepo are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Harness investigation program: audit of 20 coding-agent CLIs (Claude Code, Codex CLI, Devin CLI, CommandCode, MiniMax CLI, OpenCode, Cursor CLI, Grok CLI, Pi CLI, and more) for OpenLLM model-fabric attachment. Results land under `bots/` as each harness is verified.

### Changed

- All OpenLLM CLI links now point at the prerelease branch: `https://github.com/openllmsh/cli/tree/prerelease` (8 files).

### Merged (from PR #3 and PR #2)

- **Hermes** (`bots/hermes`, status: ready) — Hermes Agent as orchestrator. `hermes mcp add` stdio setup docs (verified against openllm CLI 2.6.36 / 43 tools), plus five skills: `getting-started`, `hermes-orchestrator`, `openllm-connect`, `openllm-dashboard`, `openllm-dev-task`. Documents two `hermes mcp add` pitfalls: `--args` must come last (it swallows trailing flags into `args`), and the tool-enable prompt needs stdin when scripted.
- Port Muse×OpenLLM integration from Drive into [`bots/muse`](./bots/muse) (status: ready). Emulated workspace skill + Secure Vault against openllm.sh, with a path to the official Muse connector directory.

## [0.1.0] — 2026-09-19

### Added

- Monorepo layout: `shared/` plus one folder per orchestrator under `bots/`.
- Shared architecture, OpenLLM connect docs, stdio MCP example, and abstract mark.
- **Grok Bot** (`bots/grok`, status: ready) — Grok-oriented skills and AddMcpServer setup docs. Emphasizes that a template share cannot pack custom MCP.
- **Cursor** (`bots/cursor`, status: ready) — Cursor plugin `openllm-orchestrator-cursor` (stdio `openllm mcp`, skills, rule, commands). Ported from [grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator).
- Root `.cursor-plugin/marketplace.json` listing `bots/cursor` so this repo can be a multi-plugin marketplace source.
- **Muse** and **Hermes** stub folders (same OpenLLM fabric; no fake skills).
- MIT license, contributing guide, and [MIGRATION.md](./MIGRATION.md).

[Unreleased]: https://github.com/MindDragonLabs/openllm-bots/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MindDragonLabs/openllm-bots/releases/tag/v0.1.0
