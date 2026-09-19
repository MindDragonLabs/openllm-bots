# Hermes

**Hermes is the orchestrator. OpenLLM is the model fabric.**

[Hermes Agent](https://hermes-agent.nousresearch.com) (Nous Research) is a terminal, IDE, and messaging-platform agent with skills, memory, MCP, cron, and delegation. This folder attaches [OpenLLM](https://openllm.sh) to it as a stdio MCP server so Hermes can route inference, inspect its account, and use context/memory tools through one gateway.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | Hermes | Plans, tools, approvals, terminal/files/git, GitHub/Vercel/other connectors |
| **Model fabric** | OpenLLM gateway + `openllm mcp` | Models, completions, account API, code/docs search, memory |

```text
Hermes  →  mcp_servers.openllm (stdio)  →  openllm mcp  →  OpenLLM gateway
```

## Attach (summary)

One command, after the key is in Hermes' env file:

```sh
hermes mcp add openllm --command openllm --connect-timeout 30 \
  --env 'OPENLLM_API_KEY=${OPENLLM_API_KEY}' 'OPENLLM_CLOUD_ORIGIN=${OPENLLM_CLOUD_ORIGIN}' \
  --args mcp
hermes mcp test openllm
```

Copy-paste steps, profiles, npm launcher, troubleshooting: [docs/setup.md](./docs/setup.md). Connect concepts (CLI install, env vars, remote MCP rules): [shared/openllm-connect.md](../../shared/openllm-connect.md).

Verified against `openllm` CLI **2.6.36**: 43 tools (native gateway API, code/docs search, memory). Trust the live list, not this count.

## Skills

| Skill | Use when |
| --- | --- |
| [`getting-started`](./skills/getting-started/SKILL.md) | First run on a fresh Hermes; teach the split, attach, verify |
| [`hermes-orchestrator`](./skills/hermes-orchestrator/SKILL.md) | Hermes-side playbook: role split, tool prefix, approvals |
| [`openllm-connect`](./skills/openllm-connect/SKILL.md) | Adding, verifying, or repairing the MCP server on Hermes |
| [`openllm-dashboard`](./skills/openllm-dashboard/SKILL.md) | Account work (usage, keys, providers, config) via MCP |
| [`openllm-dev-task`](./skills/openllm-dev-task/SKILL.md) | Implementation tasks using gateway models + context/memory |

## Notes for this host

- The connector is **per profile** (`~/.hermes/profiles/<name>/config.yaml`); repeat for each Hermes profile that needs it.
- Tools load in a **new session** (`/reset`, new CLI run, or gateway restart) — MCP discovery happens at session start.
- In-session tool names are prefixed: `mcp_openllm_<tool>`.
- Hermes keeps its own connectors (terminal, file, git/`gh`, web, …). OpenLLM does not replace them.

Shared architecture: [shared/architecture.md](../../shared/architecture.md). Status: `ready` — see [`bot.manifest.json`](./bot.manifest.json).
