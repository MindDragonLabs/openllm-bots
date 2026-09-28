# MiniMax Code (mcode)

**Orchestrator:** MiniMax Code (`mcode`)
**Model fabric:** [OpenLLM](https://openllm.sh) via custom provider (Anthropic-messages format)
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json)) · verified live 2026-09-28 against mcode 0.4.12

MiniMax Code keeps planning, permissions, sessions, and plugins. OpenLLM becomes the model fabric through `mcode provider add` with the `anthropic-messages` API format.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | MiniMax Code | Plans, permissions, sessions, plugins, terminal/files/git |
| **Model fabric** | OpenLLM gateway | Models, completions, routing across your existing providers |

```text
mcode  →  custom provider (anthropic-messages)  →  OpenLLM gateway  →  models
```

Shared docs: [architecture](../../shared/architecture.md) · [connect rules](../../shared/openllm-connect.md) · [harness survey](../../docs/harness-survey.md)

## Attach (summary)

One command (gateway root, **no `/v1`**, Anthropic wire format):

```sh
export OPENLLM_API_KEY=...
mcode provider add \
  --name "OpenLLM" \
  --base-url "http://127.0.0.1:8787" \
  --api-format anthropic-messages \
  --model "grok/grok-4.7" \
  --model "kimi_code/k3" \
  --api-key-env OPENLLM_API_KEY
```

Verify headless:

```sh
mcode exec \
  --model "custom_provider:openllm/grok/grok-4.7" \
  --permission off --timeout 90s \
  "Reply with exactly: OPENLLM-OK"
```

Full steps and pitfalls: [docs/setup.md](./docs/setup.md).

## Gotchas

- **`anthropic-messages` works; `openai-completions` does not.** mcode's `openai-completions` request shape is rejected by the OpenLLM gateway with a 400 schema error. Register the provider against the gateway root with `--api-format anthropic-messages`.
- **Gateway root, no `/v1`**, for the Anthropic wire format. (OpenAI-format attach points that do work elsewhere use `/v1` — the two are not interchangeable.)
- **Model reference is `custom_provider:openllm/<model-id>`** — the `custom_provider:` prefix and the provider id you chose, then the gateway model id.
- **`--api-key-env`, not `--api-key`.** The key is read from the environment at run time.
- `mcode provider list` shows the provider state; `mcode provider test <provider-id>` checks a configured model.
