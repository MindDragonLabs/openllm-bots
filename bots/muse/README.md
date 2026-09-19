# Muse

This folder is `bots/muse` inside the [openllm-bots](https://github.com/MindDragonLabs/openllm-bots) monorepo.

**Role split:** **Muse = orchestrator**, **OpenLLM ([openllm.sh](https://openllm.sh)) = model fabric**.

Shared docs ([architecture](../../shared/architecture.md), [OpenLLM connect](../../shared/openllm-connect.md)) currently emphasize the openllm.sh / `openllm mcp` path used by Grok and Cursor. Muse’s native path is the emulated workspace skill + Secure Vault against **openllm.sh**, as documented in this folder.

---

# Muse × OpenLLM Integration

A setup and training repository that teaches any Muse instance how to integrate
with [openllm.sh](https://openllm.sh) — a unified LLM gateway (one
OpenAI-compatible endpoint, one `sk-llm` key, fallback chains across providers)
— using Muse itself as the orchestrator.

## Two ways to integrate

1. **Official connector (public).** Submit at `muse.ai/platform`: describe the
   product → pass Meta's functional / security / legal review + end-to-end
   testing → appear in the connector directory for all users.
2. **Emulated connector (private, this repo).** A workspace skill backed by a
   small CLI that calls the OpenLLM API. The `sk-llm` key lives in the Secure
   Vault. No review, works today, private to one user. This repo documents that
   path.

## How to use this repo

Read the docs in order. They are written for the agent doing the setup.

| File | What it covers |
|---|---|
| `docs/01-overview.md` | Architecture: who calls what |
| `docs/02-prerequisites.md` | Account, scoped key, base URL |
| `docs/03-credential-setup.md` | Storing the key in the Secure Vault |
| `docs/04-skill-spec.md` | Building the `openllm` workspace skill |
| `docs/05-orchestrator-patterns.md` | How Muse orchestrates calls |
| `docs/06-monitoring.md` | Spend watchdog via scheduled checks |
| `docs/07-official-path.md` | Graduating to the public directory |
| `docs/08-limitations.md` | What this setup cannot do |
| `docs/09-troubleshooting.md` | 401s, rotation, common failures |
| `templates/` | Fill-in `SKILL.md`, CLI, and cron templates |
| `examples/sample-flows.md` | Worked prompt → action transcripts |

## Ground truth

- The API base URL is **not** in this repo. Take it from the openllm.sh
  dashboard ("just the base URL and key", per their FAQ). It is OpenAI
  compatible: `{base_url}/chat/completions`, `{base_url}/models`.
- The key prefix is `sk-llm`. Auth is `Authorization: Bearer <key>`.
- Generate a **scoped** key for this integration (own spend cap, own cooldown,
  revocable alone) — never reuse a personal master key.
- Keys are collected with `credentials.request_api_access`, never in chat.
