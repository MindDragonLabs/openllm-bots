# Cursor plugin setup

Cursor agent is the orchestrator; OpenLLM is the model fabric. Plugin id: `openllm-orchestrator-cursor`.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Grok Bot (custom MCP, not this `mcp.json`): [../../grok/docs/setup.md](../../grok/docs/setup.md)

## Prerequisites

1. An [OpenLLM](https://openllm.sh) account.
2. The OpenLLM CLI. Review, then:

   ```sh
   curl -fsSL "https://openllm.sh/api/setup/cli/install.sh" | bash
   openllm version
   ```

   Dashboard one-click installs are sandboxed — run `~/.openllm/bin/openllm setup` once. Upstream CLI: [github.com/openllmsh/cli](https://github.com/openllmsh/cli/tree/prerelease).

3. An API key from the OpenLLM dashboard (`sk-llm` / API key). Put it in plugin variables, not in git.

## Install the plugin

### Marketplace (when listed)

1. Open **Customize** → Plugins / Marketplace.
2. Install **OpenLLM Orchestrator (Cursor)** (`openllm-orchestrator-cursor`).
3. Set variables under **Plugins → Configure**.
4. Confirm the `openllm` MCP server is running.

Submit/update listing: [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish). This monorepo's marketplace manifest is [`.cursor-plugin/marketplace.json`](../../../.cursor-plugin/marketplace.json) with `source: bots/cursor`.

### Clone the monorepo

```sh
git clone https://github.com/MindDragonLabs/openllm-bots
```

Use it as a project, as a team marketplace source, or copy `bots/cursor`.

### Local plugin (development)

1. Copy **`bots/cursor`** (not the whole monorepo) to `~/.cursor/plugins/local/openllm-orchestrator-cursor`. The folder must live **inside** `~/.cursor/plugins/local`; Cursor skips symlinks that point elsewhere.
2. Restart Cursor or **Developer: Reload Window**.
3. Open Customize and confirm skills, the orchestrator rule, commands, and the `openllm` MCP server.

On Teams/Enterprise, local plugin imports may be admin-gated.

## Configure variables

Declared in [`.cursor-plugin/plugin.json`](../.cursor-plugin/plugin.json), substituted into [`mcp.json`](../mcp.json):

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENLLM_API_KEY` | yes | — | Dashboard API key |
| `OPENLLM_CLOUD_ORIGIN` | no | `https://openllm.sh` | Gateway origin (host origin, not a `/v1` path) |

The CLI also reads `~/.openllm/.env` from daemon pairing. Marketplace/Cloud Agent installs should still set plugin variables so `${OPENLLM_API_KEY}` resolves.

Shipped MCP server (stdio only — no invented remote URL):

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

Alternate paths (CLI, npm launcher, dashboard-only remote URL): [shared/openllm-connect.md](../../../shared/openllm-connect.md).

## Commands

- `/setup-openllm` — connect and verify
- `/openllm-dev-task` — development execution mode

## Verify

Reload MCP, then ask the agent to list live tools on the `openllm` server and list models. Do not print the API key.
