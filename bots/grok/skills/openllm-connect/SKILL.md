---
name: openllm-connect
description: Step-by-step connection of OpenLLM MCP on Grok Bot. Use when adding custom MCP, installing the CLI, pairing keys, tools are missing, or troubleshooting binary/key/origin failures.
---

# Connect OpenLLM MCP (Grok Bot)

Wire the official unified MCP server (`openllm mcp`) so Grok Bot can see gateway, context, and memory tools.

Grok Bot **does not** pick up Cursor `mcp.json`. A shared bot **template cannot pack a custom MCP** for the next owner. Each owner adds OpenLLM themselves.

Grok Bot runs in the cloud: it **cannot** reach `localhost` on the user's laptop. A local daemon URL will not work.

Upstream: [OpenLLM CLI](https://github.com/openllmsh/cli/tree/prerelease). Shared write-up: [shared/openllm-connect.md](../../../../shared/openllm-connect.md). Copy-paste: [docs/setup.md](../../docs/setup.md). Config keys: `OPENLLM_API_KEY` and `OPENLLM_CLOUD_ORIGIN`.

Ask **one question at a time**. Never commit secrets.

## Add as custom MCP (AddMcpServer)

There is no separate settings form. In chat (paraphrase, then confirm with the user):

**Stdio (preferred when the cloud machine can run the CLI):**

> Add a custom MCP server named `openllm` that runs `openllm mcp`. Set env `OPENLLM_API_KEY` to the key I provide next and `OPENLLM_CLOUD_ORIGIN` to `https://openllm.sh` unless I specify another origin.

Install CLI on a machine you control (review, then):

```sh
curl -fsSL "https://openllm.sh/install" | bash
openllm version
```

**Dashboard one-click:** run `~/.openllm/bin/openllm setup` if PATH is missing.

If `openllm` is not installed on the cloud machine, use the npm launcher (still stdio):

> Add a custom MCP server named `openllm` that runs `npx -y @openllmsh/npm mcp` with the same env vars.

**Remote MCP / SSE (only if the OpenLLM dashboard shows one):**

Do **not** invent a URL. If the dashboard lists a remote MCP or SSE endpoint, add it as custom MCP with a bearer header — placeholders only:

```json
{
  "mcpServers": {
    "openllm": {
      "url": "<PASTE_URL_FROM_OPENLLM_DASHBOARD>",
      "headers": {
        "Authorization": "Bearer <PASTE_OPENLLM_API_KEY>"
      }
    }
  }
}
```

Chat form:

> Add a custom MCP server named `openllm` at `<PASTE_URL_FROM_OPENLLM_DASHBOARD>` with header `Authorization: Bearer <PASTE_OPENLLM_API_KEY>`.

Canonical stdio shape (same as [shared/mcp.stdio.example.json](../../../../shared/mcp.stdio.example.json)):

```json
{
  "mcpServers": {
    "openllm": {
      "command": "openllm",
      "args": ["mcp"],
      "env": {
        "OPENLLM_API_KEY": "${OPENLLM_API_KEY}",
        "OPENLLM_CLOUD_ORIGIN": "${OPENLLM_CLOUD_ORIGIN}"
      }
    }
  }
}
```

## Verify

You should see an `openllm` MCP server with tools. **Read the live tool list.** Typical groups (labels can shift; do not hard-code names in plans):

- Native gateway API — generated from the same schema as `https://openllm.sh/api/swagger`
- Code/docs search — `openllm-context` / `claude-context`
- Memory — `openllm-memory` / `supermemory`

Keep GitHub, Vercel, and other connectors attached — OpenLLM is not those products. Full playbook: **grok-orchestrator**.

## Pairing

If the user already runs the OpenLLM desktop/daemon flow, `~/.openllm/.env` may already hold origin + key **on their laptop**. That does **not** automatically authenticate Grok Bot. Collect the dashboard key into MCP env for this host unless tools already authenticate successfully.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Server fails to start / `command not found` | Cloud machine has no CLI. Use `npx -y @openllmsh/npm mcp`, or install the CLI on that host. |
| Tools empty / auth errors | Bad or missing `OPENLLM_API_KEY`. Typical prefix `sk-llm`. Do not log the key. |
| Wrong account or 404-style gateway errors | `OPENLLM_CLOUD_ORIGIN` (default `https://openllm.sh`). Origin is a **host origin**, not a `/v1` URL. |
| Cursor works, Grok Bot does not | Re-add as **custom MCP** here. Cursor `mcp.json` is not shared. No localhost URLs. |
| User wants a remote URL you do not see | Copy whatever MCP/SSE URL the OpenLLM dashboard **shows**. If none exists, stay on stdio. |

## After connect

Offer dashboard mode (**openllm-dashboard**) or a first dev task (**openllm-dev-task**).
