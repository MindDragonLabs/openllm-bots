# Changelog

All notable changes to this monorepo are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
