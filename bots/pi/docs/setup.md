# Pi setup

Copy-pasteable path for attaching Pi to OpenLLM. Pi is the orchestrator; OpenLLM is the model fabric.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect rules: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Harness survey: [docs/harness-survey.md](../../../docs/harness-survey.md)

Verified: pi **0.73.1**, macOS arm64, local OpenLLM gateway `http://127.0.0.1:8787/v1`, 2026-09-28.

## Prerequisites

- OpenLLM account + API key: [openllm.sh](https://openllm.sh)
- Pi installed (`pi --version` works)
- Gateway reachable from this machine

## 1. Environment

```sh
export OPENLLM_API_KEY="sk-llm-..."
```

## 2. Register the provider

Edit `~/.pi/agent/models.json`. If it exists, merge the `openllm` block into `providers`; do not delete other providers.

```json
{
  "providers": {
    "openllm": {
      "baseUrl": "http://127.0.0.1:8787/v1",
      "api": "openai-completions",
      "apiKey": "env:OPENLLM_API_KEY",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        { "id": "grok/grok-4.5", "name": "Grok 4.5 via OpenLLM", "context": 200000 },
        { "id": "grok/grok-4.6", "name": "Grok 4.6 via OpenLLM", "context": 200000 },
        { "id": "kimi_code/kimi-for-coding-highspeed", "name": "Kimi K3 highspeed via OpenLLM", "context": 256000 },
        { "id": "kimi_code/k3", "name": "Kimi K3 via OpenLLM", "context": 256000 }
      ]
    }
  }
}
```

Field notes:

| Field | Value | Why |
| --- | --- | --- |
| `apiKey` | `"env:OPENLLM_API_KEY"` | Key read from env at launch; nothing secret in the file |
| `api` | `"openai-completions"` | OpenAI chat-completions wire format against `/v1` |
| `compat.supportsDeveloperRole` | `false` | Stops pi sending a `developer` role message the gateway rejects |
| `compat.supportsReasoningEffort` | `false` | Stops pi sending `reasoning_effort` fields the gateway may reject |
| `context` | real model context | Pi's context meter uses it; wrong values skew the display |

## 3. Verify headless

```sh
pi --model openllm/grok/grok-4.5 -p "Reply with exactly: OPENLLM-OK"
```

Expected: `OPENLLM-OK`. The `--model` value is `<provider>/<model-id>`.

## 4. Use it day to day

- Interactive: launch `pi`, then `/model openllm/grok/grok-4.5` (or pick from the model list).
- Headless/scripted: `pi --model openllm/<id> -p "<task>"`.
- Extensions (including MCP) keep working; the provider change only moves the endpoint.

## 5. Pick models from the catalog

```sh
curl -s http://127.0.0.1:8787/v1/models \
  -H "Authorization: Bearer $OPENLLM_API_KEY" | jq -r '.data[].id' | head -30
```

Mirror the ids you want into the provider's `models` array. Do not guess ids.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| 400 mentioning `developer` role or `reasoning_effort` | compat flags missing | Set both compat flags to `false` |
| 401 from gateway | `OPENLLM_API_KEY` not exported | Export it in the shell that launches pi |
| `unknown provider` on `--model` | provider name typo | `--model openllm/<id>` — the key in `providers` is the prefix |
| Model listed but calls fail | id not actually in gateway catalog | Verify with `/v1/models`; remove dead entries |
| Context meter wildly wrong | wrong `context` value | Set the real gateway context size per model |
