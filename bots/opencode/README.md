# OpenCode

**Orchestrator:** OpenCode (`opencode`)
**Model fabric:** [OpenLLM](https://openllm.sh) via an `@ai-sdk/openai-compatible` provider in `opencode.json`
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json)) · verified live 2026-09-28 against opencode 1.15.7

OpenCode keeps planning, its Build/Plan agents, permissions, LSP, and sessions. OpenLLM becomes the model fabric through a provider block using the OpenAI-compatible AI SDK package.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | OpenCode | Plans, Build/Plan agents, permissions, LSP, sessions |
| **Model fabric** | OpenLLM gateway | Models, completions, routing across your existing providers |

```text
opencode  →  opencode.json provider "openllm"  →  OpenLLM gateway /v1  →  models
```

Shared docs: [architecture](../../shared/architecture.md) · [connect rules](../../shared/openllm-connect.md) · [harness survey](../../docs/harness-survey.md)

## Attach (summary)

Add an `openllm` provider to `opencode.json` (project) or `~/.config/opencode/opencode.json` (global):

```jsonc
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

The key comes from the environment — **no `apiKey` in the file**:

```sh
export OPENCODE_API_KEY_openllm="$OPENLLM_API_KEY"
```

Verify headless:

```sh
opencode run --model 'openllm/grok/grok-4.7' "Reply with exactly: OPENLLM-OK"
```

Full steps and pitfalls: [docs/setup.md](./docs/setup.md).

## Gotchas

- **Pass `--model` explicitly on `run`.** Without it opencode uses its configured default (often a subscription agent), which can fail with `Insufficient account funds` instead of routing to OpenLLM. You can also set `"model": "openllm/<id>"` in the config to make it the default.
- **`OPENCODE_API_KEY_openllm`** (lowercase provider id appended) is the env-var pattern opencode resolves for a custom provider key. It keeps the secret out of `opencode.json`.
- **`/v1` root** in `baseURL`.
- **Slash-containing model ids are fine** as JSON keys — `grok/grok-4.7` works; reference it as `openllm/grok/grok-4.7` on the CLI.
- `/connect` stores auth for known providers; a config-defined provider with an env key needs no `/connect` step.
