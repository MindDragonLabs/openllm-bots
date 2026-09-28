# ZCode setup

Copy-pasteable path for attaching ZCode (`zcode-app-cli`) to OpenLLM. ZCode is the orchestrator; OpenLLM is the model fabric.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect rules: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Harness survey: [docs/harness-survey.md](../../../docs/harness-survey.md)

Verified: zcode-app-cli **3.14.3-28** (runtime 0.16.9), macOS arm64, local OpenLLM gateway `http://127.0.0.1:8787/v1`, 2026-09-28.

## Prerequisites

- OpenLLM account + API key: [openllm.sh](https://openllm.sh)
- ZCode installed: `npm install -g zcode-app-cli@latest` (then `zcode --version`)
- Gateway reachable from this machine

## 1. Create the provider file

ZCode reads personal providers from `~/.zcode/v2/provider_config.json` (shared with ZCode Desktop). If it does not exist, create it. **All three parts are required** — provider rule, manual model rules, and a default selection:

```json
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
              "apiKey": "sk-llm-REPLACE_ME",
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
              "reasoningLevel": { "values": ["low", "medium", "high"], "map": "{}" }
            }
          }
        },
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
              "reasoningLevel": { "values": ["low", "medium", "high"], "map": "{}" }
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

Lock the file down **before** writing the key into it (or chmod immediately after — the window between write and chmod also exposes the key):

```sh
umask 077   # in the shell you edit from
# ... edit the file (key lands 600 from the start)
# already written? close the window now:
chmod 600 ~/.zcode/v2/provider_config.json
```

## 2. Verify headless

```sh
zcode --prompt "Reply with exactly: OPENLLM-OK"
```

Expected: `OPENLLM-OK` (a `ZCode Built-in missing` notice may precede it; it is cosmetic for a personal-only provider setup).

## 3. Add more models

1. List gateway ids: `curl -s http://127.0.0.1:8787/v1/models -H "Authorization: Bearer $OPENLLM_API_KEY" | jq -r '.data[].id'`
2. Append the id to `personalModelIds` and `modelOrder`.
3. Copy one `manualProviderModelRules` block, change `modelId`, and adjust `contextWindow` if known.
4. Re-run the verify command. `/model` in the TUI refreshes the live registry.

## Why each required part exists

| Part | Without it |
| --- | --- |
| Provider rule (`providerRules`) | No endpoint/key — nothing to route to |
| `manualProviderModelRules` per model | Gateway ids are unknown to the upstream catalog; smart rules inherit nothing and the model stays unusable |
| `defaultModelSelection` | First prompt fails: `Model creation failed → Select a model before continuing` |

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Model creation failed` + `Select a model before continuing` | no `defaultModelSelection`, or no manual rule for the id | Add both (see table above) |
| `ZCode Built-in missing` notice | personal-only provider setup, no Z.AI account | Cosmetic; completion still routes |
| 401 from gateway | wrong `access.apiKey` | Replace `sk-llm-REPLACE_ME` with the real key |
| 404 / not found | `baseUrl` missing `/v1` for the chat-completions type | Use `http://<host>:8787/v1` |
| Config ignored | Desktop overwrote the shared file | Set `ZCODE_PERSONAL_PROVIDER_CONFIG_FILE` to a separate file |
| setting.json locale warning (`ui.locale: Invalid option`) | older/other tool wrote an invalid locale | Cosmetic for this attach; fix separately in `~/.zcode/cli/setting.json` |

## Loopback caveat

"Verified live" ran on a loopback gateway that does not enforce request authentication — it proves routing, not key transport. See the [survey method note](../../../docs/harness-survey.md).
