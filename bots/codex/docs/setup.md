# Codex CLI setup

Copy-pasteable path for attaching Codex CLI to OpenLLM. Codex is the orchestrator; OpenLLM is the model fabric.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect rules: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Harness survey: [docs/harness-survey.md](../../../docs/harness-survey.md)

Verified: codex-cli **0.157.0**, macOS arm64, local OpenLLM gateway `http://127.0.0.1:8787/v1`, 2026-09-28.

## Prerequisites

- OpenLLM account + API key: [openllm.sh](https://openllm.sh)
- Codex CLI installed (`codex --version` works)
- Gateway reachable from this machine

## 1. Environment

```sh
export OPENLLM_API_KEY="sk-llm-..."
```

## 2. Add the provider block

Edit `~/.codex/config.toml` — put the four top-level keys **before any `[table]`** section (TOML assigns top-level keys to the last open table), replacing any existing `model`/`model_provider` lines:

```toml
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

Field notes:

| Field | Value | Why |
| --- | --- | --- |
| `wire_api` | `"responses"` | `"chat"` was removed in codex 0.153+; config fails to load with it |
| `web_search` | `"disabled"` | codex's default live-search sends a cache-only web-search policy the gateway daemon rejects |
| `env_key` | `"OPENLLM_API_KEY"` | Key read from env at run time; never hardcode `api_key` |
| `base_url` | gateway `/v1` | Responses endpoint lives under `/v1` |

## 3. Verify headless

```sh
codex exec --skip-git-repo-check "Reply with exactly: OPENLLM-OK"
```

Expected output includes `OPENLLM-OK`. A `Model metadata for grok/grok-4.7 not found` warning is cosmetic.

## 4. Isolated setup (optional, recommended for testing)

Keep your everyday ChatGPT-login config untouched by using a separate `CODEX_HOME`:

```sh
mkdir -p ~/.codex-openllm
cat > ~/.codex-openllm/config.toml <<'EOF'
model = "grok/grok-4.7"
model_provider = "openllm"
model_reasoning_effort = "low"
web_search = "disabled"

[model_providers.openllm]
name = "OpenLLM"
base_url = "http://127.0.0.1:8787/v1"
env_key = "OPENLLM_API_KEY"
wire_api = "responses"
EOF

CODEX_HOME=~/.codex-openllm codex exec --skip-git-repo-check "Reply with exactly: OPENLLM-OK"
```

## 5. Pick models from the catalog

```sh
curl -s http://127.0.0.1:8787/v1/models \
  -H "Authorization: Bearer $OPENLLM_API_KEY" | jq -r '.data[].id' | head -30
```

Update `model =` in the config to the id you want. Per-invocation override: `codex exec -m kimi_code/k3 ...` with `model_provider` already set to `openllm`.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `wire_api = "chat" is no longer supported` | pre-0.153 config | Set `wire_api = "responses"` |
| `unsupported_web_search_policy` error mid-run | web search enabled | Set `web_search = "disabled"` (values: `disabled`, `cached`, `indexed`, `live`) |
| 401 from gateway | key not in env | `export OPENLLM_API_KEY=...` in the launching shell |
| Requests still hit OpenAI | provider block not selected | `model_provider = "openllm"` must be set (top level, not inside the block) |
| `Model metadata ... not found` warning | gateway id not in codex's local metadata | Cosmetic; completion still routes |

## Loopback caveat

"Verified live" ran on a loopback gateway that does not enforce request authentication — it proves routing, not key transport. See the [survey method note](../../../docs/harness-survey.md).
