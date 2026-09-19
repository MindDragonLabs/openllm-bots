---
name: openllm-connect
description: Step-by-step connection of OpenLLM MCP to Cursor and Grok Bot. Use when installing the CLI, pairing keys, MCP tools are missing, or troubleshooting binary/key/origin failures.
---

# Connect OpenLLM MCP

Wire the official unified MCP server (`openllm mcp`) so the orchestrator can see gateway, context, and memory tools.

Upstream: [OpenLLM CLI](https://github.com/openllmsh/cli). Shared write-up: [shared/openllm-connect.md](../../../../shared/openllm-connect.md). Cursor docs: [docs/setup.md](../../docs/setup.md). Config keys: `OPENLLM_API_KEY` and `OPENLLM_CLOUD_ORIGIN` (environment **or** `~/.openllm/.env` from daemon pairing).

Ask **one question at a time**. Never commit secrets.

## Cursor (this plugin)

### 1. Install the CLI

Canonical:

```sh
curl -fsSL "https://openllm.sh/api/setup/cli/install.sh" | bash
openllm version
openllm mcp
```

The last command is a **stdio MCP server** (it waits on stdin). Cursor should spawn it via `mcp.json`; the user should not need to leave it running in a terminal.

**Dashboard one-click:** the gateway dashboard can install OpenLLM's plugin/CLI for you. That install is sandboxed and skips PATH/completion — run:

```sh
~/.openllm/bin/openllm setup
```

Optional launcher if `openllm` is not on PATH yet (not this plugin's default `mcp.json`):

```sh
npx -y @openllmsh/npm mcp
```

### 2. Plugin variables

This plugin declares:

| Variable | Required | Default | Where the value comes from |
| --- | --- | --- | --- |
| `OPENLLM_API_KEY` | yes | — | openllm.sh dashboard (`sk-llm` / API key) |
| `OPENLLM_CLOUD_ORIGIN` | no | `https://openllm.sh` | Same origin the CLI/docs call the cloud gateway |

In Cursor: **Plugins → Configure** (or the install-time variable form). Values substitute into `${OPENLLM_API_KEY}` and `${OPENLLM_CLOUD_ORIGIN}` in `mcp.json`. Plugin-managed MCP config is read-only in the dashboard.

The CLI also reads `~/.openllm/.env` written by daemon pairing. One pairing can serve every OpenLLM tool on the machine. Prefer plugin variables for marketplace installs so Cloud Agents get the same substitution.

### 3. Confirm `mcp.json`

Shipped config (stdio only — no invented remote URL):

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

Reload the window or toggle the server in Customize → MCP.

### 4. Verify

You should see an `openllm` MCP server with tools. **Read the live tool list.** Typical groups (labels can shift; do not hard-code names in plans):

- Native gateway API — generated from the same schema as `https://openllm.sh/api/swagger` (one tool per OpenAPI operation). Printable locally with `openllm api --spec` if the CLI is installed.
- Code/docs search — `openllm-context` / `claude-context` (`openllm exec ctx …` is the hook-side equivalent).
- Memory — `openllm-memory` / `supermemory`.

`openllm mcp [--only]` can restrict groups; this plugin starts the default (all groups).

## Grok Bot (custom MCP)

Grok Bot **does not** pick up this plugin's `mcp.json`. A shared bot **template cannot pack a custom MCP** for the next owner. Each owner adds OpenLLM themselves.

Grok Bot runs in the cloud: it **cannot** reach `localhost` on the user's laptop. A local daemon URL will not work.

Full playbook: **grok-bot-orchestrator** and [bots/grok/docs/setup.md](../../../grok/docs/setup.md). Dedicated Grok skills live in [`bots/grok/skills`](../../../grok/skills).

### Add as custom MCP (AddMcpServer equivalent)

**Stdio (preferred when the cloud machine can run the CLI):**

> Add a custom MCP server named `openllm` that runs `openllm mcp`. Set env `OPENLLM_API_KEY` to the key I provide next and `OPENLLM_CLOUD_ORIGIN` to `https://openllm.sh` unless I specify another origin.

If `openllm` is not installed on that machine, use the npm launcher (still stdio):

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

## Pairing

If the user already runs the OpenLLM desktop/daemon flow, `~/.openllm/.env` may already hold origin + key. You may skip re-asking for a key **only** if MCP tools already authenticate successfully. Otherwise collect the dashboard key into plugin variables / MCP env.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Server fails to start / `command not found` | CLI not on PATH. Install script, or `~/.openllm/bin/openllm setup`, or point the command at `~/.openllm/bin/openllm`. Confirm with `openllm version`. |
| Tools empty / auth errors | Bad or missing `OPENLLM_API_KEY`. Create a key on the dashboard; typical prefix is `sk-llm`. Do not log the key. |
| Wrong account or 404-style gateway errors | `OPENLLM_CLOUD_ORIGIN` (default `https://openllm.sh`). Typos, `http` vs `https`, trailing paths. Origin is a **host origin**, not a `/v1` URL. |
| Cursor works, Grok Bot does not | Re-add as **custom MCP** on Grok Bot. Cursor `mcp.json` is not shared. No localhost URLs. |
| Dashboard plugin installed but Cursor cannot spawn `openllm` | Run `~/.openllm/bin/openllm setup`; restart Cursor. |
| User wants a remote URL you do not see | Open the OpenLLM dashboard **Integrations** (or equivalent) and copy whatever MCP/SSE URL **they** show. If none exists, stay on stdio `openllm mcp`. |

## After connect

Offer dashboard mode (**openllm-dashboard**) or a first dev task (**openllm-dev-task**).
