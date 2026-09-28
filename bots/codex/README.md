# Codex CLI

**Orchestrator:** Codex CLI (`codex`)
**Model fabric:** [OpenLLM](https://openllm.sh) via a `model_providers` block (Responses wire API)
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json)) · verified live 2026-09-28 against codex-cli 0.157.0

Codex keeps planning, sandboxing, approvals, and tools. OpenLLM becomes the model fabric through a custom `model_providers.openllm` block in `config.toml`. An earlier survey verdict ("ChatGPT-account auth overrides the base URL — BLOCKED") is **outdated**: with a dedicated provider block and the Responses wire API, codex routes through OpenLLM.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | Codex CLI | Plans, sandboxing, approvals, terminal/files/git |
| **Model fabric** | OpenLLM gateway | Models, completions, routing across your existing providers |

```text
codex  →  model_providers.openllm (responses)  →  OpenLLM gateway /v1  →  models
```

Shared docs: [architecture](../../shared/architecture.md) · [connect rules](../../shared/openllm-connect.md) · [harness survey](../../docs/harness-survey.md)

## Attach (summary)

Edit `~/.codex/config.toml` — put the four top-level keys **before any `[table]`** section (TOML assigns top-level keys to the last open table), replacing any existing `model`/`model_provider` lines:

```toml
model = "grok/grok-4.7"
model_provider = "openllm"
model_reasoning_effort = "low"
web_search = "disabled"          # gateway rejects codex's cache-only web-search policy

[model_providers.openllm]
name = "OpenLLM"
base_url = "http://127.0.0.1:8787/v1"
env_key = "OPENLLM_API_KEY"      # read from the environment, never hardcode
wire_api = "responses"           # "chat" was removed in codex 0.153+
```

Verify headless:

```sh
export OPENLLM_API_KEY=...
codex exec --skip-git-repo-check "Reply with exactly: OPENLLM-OK"
```

Full steps, per-project config, and pitfalls: [docs/setup.md](./docs/setup.md).

## Gotchas

- **`wire_api = "chat"` no longer loads** (codex 0.153+ removed it). Use `"responses"`.
- **Set `web_search = "disabled"`.** Codex's default `live` web search sends a cache-only web-search policy the OpenLLM daemon rejects (`unsupported_web_search_policy`). Disabling it removes the error; the model itself still works.
- **Fallback model metadata warning** for gateway catalog ids is cosmetic.
- **Signed-in ChatGPT sessions coexist.** With `model_provider = "openllm"` at the top level, OpenLLM becomes the **default for every invocation** from that config; your ChatGPT login is untouched but unused. For per-invocation control use `-c model_provider=...` overrides, or a separate `CODEX_HOME` (as in [docs/setup.md](./docs/setup.md)) for a fully isolated setup.
- `env_key` beats hardcoding `api_key` — the key stays out of the file.
