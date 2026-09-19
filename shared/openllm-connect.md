# Connect OpenLLM (shared)

How every orchestrator bot in this monorepo talks to OpenLLM. Product: [openllm.sh](https://openllm.sh). CLI source: [github.com/openllmsh/cli](https://github.com/openllmsh/cli/tree/prerelease).

Architecture (orchestrator vs model fabric): [architecture.md](./architecture.md). Example stdio MCP config: [mcp.stdio.example.json](./mcp.stdio.example.json).

Do **not** commit API keys. Do **not** invent a remote MCP URL.

## Prerequisites

1. An [OpenLLM](https://openllm.sh) account.
2. The **OpenLLM CLI** (provides `openllm mcp`). Review the official install script, then:

   ```sh
   curl -fsSL "https://openllm.sh/api/setup/cli/install.sh" | bash
   openllm version
   ```

   **Dashboard one-click:** installing OpenLLM's plugin from the gateway dashboard also drops the CLI, but that path is sandboxed — run `~/.openllm/bin/openllm setup` once.

3. An API key from the OpenLLM dashboard (`sk-llm` / API key). Put it in plugin variables or MCP env, not in git.

## Environment variables

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENLLM_API_KEY` | yes | — | Dashboard API key |
| `OPENLLM_CLOUD_ORIGIN` | no | `https://openllm.sh` | Gateway origin (host origin, not a `/v1` path) |

The CLI also reads `~/.openllm/.env` from daemon pairing. Marketplace / Cloud Agent installs should still set plugin variables so `${OPENLLM_API_KEY}` resolves.

## Stdio MCP (preferred)

Shipped and example config (stdio only):

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

Cursor: this is [`bots/cursor/mcp.json`](../bots/cursor/mcp.json); values come from Plugins → Configure.

Grok Bot: paste the equivalent as a **custom MCP** (AddMcpServer). Template share does **not** include the next owner's connector. Copy-paste: [bots/grok/docs/setup.md](../bots/grok/docs/setup.md).

The last command `openllm mcp` is a **stdio MCP server** (it waits on stdin). The host should spawn it; the user should not leave it running in a terminal.

### Alternate launchers

- **npm** (not the default `mcp.json`): `npx -y @openllmsh/npm mcp` with the same env vars — useful when the cloud machine has no `openllm` binary.
- **Absolute binary**: `~/.openllm/bin/openllm mcp` if PATH is incomplete.

## Remote MCP / SSE (dashboard URL only)

Only if the OpenLLM dashboard **Integrations** (or equivalent) shows an MCP or SSE URL. Add as custom MCP with `Authorization: Bearer <OPENLLM_API_KEY>`.

This repo does **not** ship a guessed remote URL. Placeholders only:

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

Grok Bot and other cloud hosts **cannot** reach `localhost` on the user's laptop. Do not point them at `127.0.0.1`. Subscription traffic that OpenLLM documents as local-daemon-only stays on a machine you control.

## MCP groups you should expect

Names can shift; trust the live list:

- Native gateway API (one tool per `/api/swagger` operation)
- Code/docs search (`openllm-context` / `claude-context`)
- Memory (`openllm-memory` / `supermemory`)

`openllm mcp [--only]` can restrict groups; default configs start all groups.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Server fails to start / `command not found` | CLI not on PATH. Install script, or `~/.openllm/bin/openllm setup`, or point the command at `~/.openllm/bin/openllm`. Confirm with `openllm version`. |
| Tools empty / auth errors | Bad or missing `OPENLLM_API_KEY`. Create a key on the dashboard; typical prefix is `sk-llm`. Do not log the key. |
| Wrong account or 404-style gateway errors | `OPENLLM_CLOUD_ORIGIN` (default `https://openllm.sh`). Typos, `http` vs `https`, trailing paths. Origin is a **host origin**, not a `/v1` URL. |
| Cursor works, Grok Bot does not | Re-add as **custom MCP** on Grok Bot. Cursor `mcp.json` is not shared. No localhost URLs. |
| Dashboard plugin installed but Cursor cannot spawn `openllm` | Run `~/.openllm/bin/openllm setup`; restart Cursor. |
| User wants a remote URL you do not see | Open the OpenLLM dashboard and copy whatever MCP/SSE URL **they** show. If none exists, stay on stdio `openllm mcp`. |

## Per-host notes

| Host | How OpenLLM is attached |
| --- | --- |
| Cursor | Plugin `mcp.json` + Plugins → Configure. See [bots/cursor](../bots/cursor/README.md). |
| Grok Bot | Custom MCP in chat. Template share cannot pack it. See [bots/grok/docs/setup.md](../bots/grok/docs/setup.md). |
| Muse | Emulated `openllm` workspace skill + Secure Vault (not `openllm mcp`). See [bots/muse](../bots/muse/README.md). |
| Hermes | Same fabric when that folder leaves stub status. |
