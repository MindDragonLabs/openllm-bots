# ZCode

**Orchestrator:** ZCode (`zcode`, npm package `zcode-app-cli`)
**Model fabric:** [OpenLLM](https://openllm.sh) via a personal provider rule in `~/.zcode/v2/provider_config.json`
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json)) · verified live 2026-09-28 (loopback gateway; see caveat) against zcode-app-cli 3.14.3-28 / runtime 0.16.9

ZCode keeps planning, permission modes, skills, and plugins. OpenLLM becomes the model fabric through the shared v2 provider registry — the same file ZCode Desktop reads.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | ZCode | Plans, permission modes, skills, plugins, terminal/files/git |
| **Model fabric** | OpenLLM gateway | Models, completions, routing across your existing providers |

```text
zcode  →  provider_config.json (openllm rule)  →  OpenLLM gateway /v1  →  models
```

Shared docs: [architecture](../../shared/architecture.md) · [connect rules](../../shared/openllm-connect.md) · [harness survey](../../docs/harness-survey.md)

## Attach (summary)

Edit `~/.zcode/v2/provider_config.json` — provider rule + manual model rules + a default selection. All three parts are required:

```jsonc
{
  "schemaVersion": 1,
  "config": {
    "providerConfigRules": {
      "providerRules": [
        {
          "providerId": "openllm",
          "providerName": "OpenLLM",
          "enabled": true,
          "config": {
            "group": "standard-personal",
            "access": {
              "type": "api-key",
              "apiKey": "sk-llm-REPLACE_ME",            // your OpenLLM API key
              "apiKeyManagementUrl": "https://openllm.sh"
            },
            "api": {
              "type": "openai-chat-completions",
              "baseUrl": "http://127.0.0.1:8787/v1",
              "headers": {}
            },
            "personalModelIds": ["grok/grok-4.7", "kimi_code/k3"],
            "modelOrder": ["grok/grok-4.7", "kimi_code/k3"],
            "visibility": "visible"
          }
        }
      ]
    },
    "modelConfigRules": {
      "providerModelRules": [],
      "manualProviderModelRules": [
        {
          "providerId": "openllm",
          "modelId": "kimi_code/k3",
          "config": {
            "properties": {
              "contextWindow": 256000,
              "inputFormat": { "supportsImage": false, "supportsVideo": false, "supportsPdf": false },
              "supportsJsonSchemaOutput": false,
              "supportsNativeWebSearch": false,
              "supportsMidConversationSystem": false
            },
            "optionSpecs": {
              "maxOutputTokens": { "max": 32000 },
              "reasoningLevel": { "values": ["low", "medium", "high"], "map": "{}" }  // map is a mapping-expression STRING per zcode schema
            }
          }
        },
        {
          "providerId": "openllm",
          "modelId": "grok/grok-4.7",
          "config": {
            "properties": {
              "contextWindow": 200000,
              "inputFormat": { "supportsImage": false, "supportsVideo": false, "supportsPdf": false },
              "supportsJsonSchemaOutput": false,
              "supportsNativeWebSearch": false,
              "supportsMidConversationSystem": false
            },
            "optionSpecs": {
              "maxOutputTokens": { "max": 32000 },
              "reasoningLevel": { "values": ["low", "medium", "high"], "map": "{}" }  // map is a mapping-expression STRING per zcode schema
            }
          }
        }
      ]
    },
    "providerOrder": ["openllm"],
    "defaultModelSelection": { "providerId": "openllm", "modelId": "grok/grok-4.7" }
  }
}
```

Verify headless:

```sh
zcode --prompt "Reply with exactly: OPENLLM-OK"
```

A `ZCode Built-in missing` notice can appear for a personal-only provider setup; the completion still routes through the gateway.

Full steps and pitfalls: [docs/setup.md](./docs/setup.md).

## Loopback caveat

"Verified live" means a real completion routed through an OpenLLM gateway on the date shown. The survey gateway runs on loopback, where the daemon does not enforce request authentication — the runs prove routing and request shape, not key transport. See [the survey method note](../../docs/harness-survey.md).

## Gotchas

- **All three config parts are required.** Provider rule alone fails with `Model creation failed → Select a model before continuing`. You need (1) the provider rule, (2) a manual model rule per model id — smart rules inherit from the upstream catalog, which does not know gateway ids — and (3) `defaultModelSelection`.
- **API key must be in the file** (`access.apiKey`) — an environment-only key does not satisfy the runtime's login gate for a personal provider. Keep the file mode `600` and never commit it.
- **`/v1` root** for `openai-chat-completions`. This is the opposite of the Anthropic-format rule (gateway root, no `/v1`) used by claude/mcode attach.
- The provider file is shared with ZCode Desktop — changing it affects both clients.
- `ZCODE_PERSONAL_PROVIDER_CONFIG_FILE` can point at a separate file to isolate provider settings.
