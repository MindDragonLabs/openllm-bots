# MiniMax Code (mcode) setup

Copy-pasteable path for attaching MiniMax Code to OpenLLM. mcode is the orchestrator; OpenLLM is the model fabric.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect rules: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Harness survey: [docs/harness-survey.md](../../../docs/harness-survey.md)

Verified: mcode **0.4.12**, macOS arm64, local OpenLLM gateway `http://127.0.0.1:8787`, 2026-09-28.

## Prerequisites

- OpenLLM account + API key: [openllm.sh](https://openllm.sh)
- MiniMax Code installed (`mcode --version` works; binary commonly at `~/.minimax-code/bin/mcode`)
- Gateway reachable from this machine

## 1. Environment

```sh
export OPENLLM_API_KEY="sk-llm-..."
export PATH="$HOME/.minimax-code/bin:$PATH"
```

## 2. Register the provider

```sh
mcode provider add \
  --name "OpenLLM" \
  --base-url "http://127.0.0.1:8787" \
  --api-format anthropic-messages \
  --model "grok/grok-4.7" \
  --model "kimi_code/k3" \
  --api-key-env OPENLLM_API_KEY
```

Key flags:

| Flag | Value | Why |
| --- | --- | --- |
| `--api-format` | `anthropic-messages` | The OpenAI-completions request shape mcode sends is rejected by the gateway (400 schema error); the Anthropic wire format passes |
| `--base-url` | gateway root, **no `/v1`** | Anthropic-format attach point is the root |
| `--api-key-env` | `OPENLLM_API_KEY` | Key read from env at run time |
| `--model` | repeatable | Gateway catalog ids; each becomes selectable |

Provider id is derived from `--name` (here: `openllm`). Check state:

```sh
mcode provider list
# custom_provider:openllm   enabled   sk-l****...
```

## 3. Verify headless

```sh
mcode exec \
  --model "custom_provider:openllm/grok/grok-4.7" \
  --permission off \
  --timeout 90s \
  "Reply with exactly: OPENLLM-OK"
```

Expected: `OPENLLM-OK`. The model reference is `custom_provider:<provider-id>/<model-id>`.

## 4. Use it day to day

- Interactive TUI: launch `mcode`, pick the OpenLLM model from the model selector.
- Headless: `mcode exec --model custom_provider:openllm/<id> ...`
- Health check: `mcode provider test custom_provider:openllm`
- MiniMax-credential work (OAuth or MiniMax API key) is untouched — `mcode provider use` switches sources; OpenLLM is just another source.

## 5. Pick models from the catalog

```sh
curl -s http://127.0.0.1:8787/v1/models \
  -H "Authorization: Bearer $OPENLLM_API_KEY" | jq -r '.data[].id' | head -30
```

Add more with a second `mcode provider add ... --model <id>` run, or re-register the provider with the full model list.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `BYOK provider ... upstream error: 400` with a long schema dump | provider registered as `openai-completions` | Re-add with `--api-format anthropic-messages` (remove the old one: `mcode provider remove custom_provider:openllm`) |
| 401 from gateway | key not in env | `export OPENLLM_API_KEY=...` in the launching shell |
| Model not found | id not in gateway catalog | Pick an id from `/v1/models` |
| Still routing to MiniMax | provider source still `minimax_api` | Select the model with the `custom_provider:openllm/` prefix, or `mcode provider use` |

## Loopback caveat

"Verified live" ran on a loopback gateway that does not enforce request authentication — it proves routing, not key transport. See the [survey method note](../../../docs/harness-survey.md).
