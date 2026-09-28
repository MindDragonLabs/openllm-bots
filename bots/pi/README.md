# Pi

**Orchestrator:** Pi (`pi`)
**Model fabric:** [OpenLLM](https://openllm.sh) via a custom provider in `~/.pi/agent/models.json`
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json)) · verified live 2026-09-28 (loopback gateway; see caveat) against pi 0.73.1

Pi keeps its minimal loop — read/write/edit/bash tools, extensions, TUI. OpenLLM becomes the model fabric through a custom provider entry in the agent models file.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | Pi | Plans, tools, extensions, TUI/RPC/SDK surfaces |
| **Model fabric** | OpenLLM gateway | Models, completions, routing across your existing providers |

```text
pi  →  models.json provider "openllm"  →  OpenLLM gateway /v1  →  models
```

Shared docs: [architecture](../../shared/architecture.md) · [connect rules](../../shared/openllm-connect.md) · [harness survey](../../docs/harness-survey.md)

## Attach (summary)

Add an `openllm` provider to `~/.pi/agent/models.json`:

```jsonc
{
  "providers": {
    "openllm": {
      "baseUrl": "http://127.0.0.1:8787/v1",
      "api": "openai-completions",
      "apiKey": "OPENLLM_API_KEY",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        { "id": "grok/grok-4.7", "name": "Grok 4.7 via OpenLLM", "contextWindow": 200000 },
        { "id": "grok/grok-4.5", "name": "Grok 4.5 via OpenLLM", "contextWindow": 200000 },
        { "id": "kimi_code/k3", "name": "Kimi K3 via OpenLLM", "contextWindow": 256000 }
      ]
    }
  }
}
```

Verify headless:

```sh
export OPENLLM_API_KEY=...
pi --model openllm/grok/grok-4.7 -p "Reply with exactly: OPENLLM-OK"
```

Full steps and pitfalls: [docs/setup.md](./docs/setup.md).

## Loopback caveat

"Verified live" means a real completion routed through an OpenLLM gateway on the date shown. The survey gateway runs on loopback, where the daemon does not enforce request authentication — the runs prove routing and request shape, not key transport. See [the survey method note](../../docs/harness-survey.md).

## Gotchas

- **`apiKey: "OPENLLM_API_KEY"`** keeps the secret out of the file; the variable must be set in the shell that launches pi.
- **Compat flags matter.** `supportsDeveloperRole: false` and `supportsReasoningEffort: false` stop pi from sending fields the gateway rejects. Set both unless your gateway build accepts them.
- **Model ids come from the gateway catalog.** List them first (`curl .../v1/models`); do not guess.
- **`--model openllm/<id>` needs the provider prefix.** A bare model id resolves against pi's default provider, not OpenLLM.
- Context values in `models.json` are hints pi uses for its context meter — set them to the real gateway model context sizes.
