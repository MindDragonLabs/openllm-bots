# OpenCode setup

Copy-pasteable path for attaching OpenCode to OpenLLM. OpenCode is the orchestrator; OpenLLM is the model fabric.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect rules: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Harness survey: [docs/harness-survey.md](../../../docs/harness-survey.md)

Verified: opencode **1.15.7**, macOS arm64, local OpenLLM gateway `http://127.0.0.1:8787/v1`, 2026-09-28.

## Prerequisites

- OpenLLM account + API key: [openllm.sh](https://openllm.sh)
- OpenCode installed (`opencode --version` works)
- Gateway reachable from this machine

## 1. Environment

```sh
export OPENCODE_API_KEY_openllm="$OPENLLM_API_KEY"
```

`OPENCODE_API_KEY_<provider-id-lowercase>` is the env pattern opencode resolves for a custom provider's key. This keeps the secret out of `opencode.json`.

## 2. Register the provider

Create or edit `opencode.json` in the project root (or `~/.config/opencode/opencode.json` globally):

```json
{
  "provider": {
    "openllm": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "OpenLLM",
      "options": {
        "baseURL": "http://127.0.0.1:8787/v1"
      },
      "models": {
        "grok/grok-4.7": { "name": "Grok 4.7 via OpenLLM" },
        "kimi_code/k3": { "name": "Kimi K3 via OpenLLM" }
      }
    }
  }
}
```

Field notes:

| Field | Value | Why |
| --- | --- | --- |
| `npm` | `@ai-sdk/openai-compatible` | The AI SDK package for any OpenAI-compatible endpoint |
| `options.baseURL` | gateway `/v1` | Chat-completions endpoint root |
| `models` keys | gateway catalog ids | Slash ids are valid JSON keys; reference as `openllm/<id>` |
| no `apiKey` in options | — | Key comes from `OPENCODE_API_KEY_openllm` |

## 3. Verify headless

```sh
opencode run --model 'openllm/grok/grok-4.7' "Reply with exactly: OPENLLM-OK"
```

Expected: `OPENLLM-OK`. **Pass `--model` explicitly** — without it opencode uses its configured default agent/model (often a subscription login), which fails with `Insufficient account funds` instead of routing to OpenLLM.

## 4. Make OpenLLM the default (optional)

Add the model to the config so the TUI and `run` use it without `--model`:

```json
{
  "model": "openllm/grok/grok-4.7",
  "provider": { "openllm": { "...": "as above" } }
}
```

## 5. Pick models from the catalog

```sh
curl -s http://127.0.0.1:8787/v1/models \
  -H "Authorization: Bearer $OPENLLM_API_KEY" | jq -r '.data[].id' | head -30
```

Mirror the ids you want into the provider's `models` object.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Insufficient account funds` | default model used, not the OpenLLM provider | Pass `--model openllm/<id>` or set `"model"` in config |
| 401 from gateway | env var not set/misspelled | `export OPENCODE_API_KEY_openllm="$OPENLLM_API_KEY"` (lowercase provider id) |
| Provider not listed in TUI | config file location/syntax | Validate JSON; project `opencode.json` overrides global |
| 404 on requests | `baseURL` missing `/v1` | Use `http://<host>:8787/v1` |
| Model listed but calls fail | id not in gateway catalog | Verify with `/v1/models`; remove dead entries |
