# Grok Bot setup

Copy-pasteable path for **Grok Bot owners**. Grok Bot is the orchestrator; OpenLLM is the model fabric.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect rules: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Playbook skill: [grok-orchestrator](../skills/grok-orchestrator/SKILL.md)

A shared bot **template cannot pack custom MCP** for the next owner. Cursor `mcp.json` is not copied over. Each owner adds OpenLLM themselves. Do not put the API key in a skill file.

Optional later: a **public Grok Bot template that references this repository** for skills. It would not include API keys and would not skip the custom-MCP step below.

## Prerequisites

- Grok Bot / Cursor account and a bot
- OpenLLM account: [https://openllm.sh](https://openllm.sh)
- An API key from the OpenLLM dashboard (`sk-llm` / API key)
- CLI **or** dashboard one-click plugin **or** a remote MCP/SSE URL the dashboard actually shows

Install CLI (review the script, then):

```sh
curl -fsSL "https://openllm.sh/install" | bash
openllm version
```

If you installed from the OpenLLM dashboard, run `~/.openllm/bin/openllm setup` once so `openllm` is on PATH.

## 1. Keep your other connectors

Leave GitHub, Vercel, and anything else you already use. OpenLLM does not replace them.

## 2. Add OpenLLM as a custom MCP

Grok Bot adds connectors **in chat** (AddMcpServer equivalent). There may be no settings form.

Paste **one** of the following. Do not send the key in a skill file.

### A. Stdio (preferred)

```text
Add a custom MCP server named openllm that runs: openllm mcp
Set environment:
- OPENLLM_API_KEY = (I will paste the key in the next message)
- OPENLLM_CLOUD_ORIGIN = https://openllm.sh
```

If the cloud machine does not have the binary:

```text
Add a custom MCP server named openllm that runs: npx -y @openllmsh/npm mcp
Use the same OPENLLM_API_KEY and OPENLLM_CLOUD_ORIGIN environment variables.
```

### B. Remote URL from the dashboard only

If Integrations (or equivalent) on [openllm.sh](https://openllm.sh) shows an MCP or SSE URL, use **that** URL. Do not guess.

```text
Add a custom MCP server named openllm at <PASTE_URL_FROM_OPENLLM_DASHBOARD>
Header Authorization: Bearer <PASTE_OPENLLM_API_KEY>
```

Equivalent shape (placeholders only):

```json
{
  "name": "openllm",
  "url": "<PASTE_URL_FROM_OPENLLM_DASHBOARD>",
  "headers": {
    "Authorization": "Bearer <PASTE_OPENLLM_API_KEY>"
  }
}
```

Grok Bot cannot reach `localhost` or your laptop daemon. Subscription traffic that OpenLLM documents as local-daemon-only stays on a machine you control; do not point the cloud bot at `127.0.0.1`.

## 3. Import companion skills

From [`bots/grok/skills/`](../skills/) in [this monorepo](https://github.com/MindDragonLabs/openllm-bots):

| Skill directory | Purpose |
| --- | --- |
| `skills/getting-started` | First run |
| `skills/openllm-connect` | Pairing and troubleshooting |
| `skills/openllm-dashboard` | Account surfaces via MCP |
| `skills/openllm-dev-task` | Coding tasks |
| `skills/grok-orchestrator` | This playbook |

Copy each `SKILL.md` body into Grok Bot skills (or install the Cursor plugin under [`bots/cursor`](../../cursor) when you also use Cursor).

Discover live MCP tool names; never invent them.

## 4. Verify

Ask:

```text
List the tools on the openllm MCP server. Then list models I can call. Do not print my API key.
```

You want a non-zero tool list and a catalog from the gateway. Then:

```text
Use dashboard mode: summarize my recent usage if that tool exists.
```

```text
Use development execution mode: <describe a small, real repo task>.
You orchestrate; OpenLLM only supplies models and gateway tools.
```

## 5. Sharing the bot

Send new owners:

1. This monorepo: [https://github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots)
2. [openllm.sh](https://openllm.sh) so they create **their** key
3. Section 2 (custom MCP)

They must not reuse your key.

## Cursor vs Grok Bot

| | Cursor IDE | Grok Bot |
| --- | --- | --- |
| [`bots/cursor/mcp.json`](../../cursor/mcp.json) | Loaded after install + variables | Not automatic — add custom MCP |
| Stdio `openllm mcp` | Yes, local CLI | Yes, if the **cloud** machine can spawn `openllm` or `npx` |
| Localhost daemon URL | Possible on that same machine | No |
| Skills/rules/commands | From the Cursor plugin | Import or copy [`skills/`](../skills/) |
| GitHub / Vercel | Separate connectors | Separate connectors |

## Role line to pin on the bot

```text
You are the orchestrator. OpenLLM is model fabric (gateway + MCP).
Do not claim OpenLLM replaces GitHub or Vercel.
Prefer MCP over the OpenLLM website. Discover tool names from the live server.
Never write secrets into git or shared skills.
```
