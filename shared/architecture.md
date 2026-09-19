# Architecture

Every folder under [`bots/`](../bots/) is an **orchestrator**. OpenLLM is the shared **model fabric** (hosted gateway + `openllm mcp`). Other connectors stay responsible for repos, deploys, and the rest of the product surface.

This split is the same whether the host is Grok Bot, a Cursor agent, Muse, Hermes, or a future bot.

## Roles

```text
Orchestrator  =  the bot (Grok Bot / Muse / Cursor agent / Hermes / …)
                 plans, tool choice, approvals, editor/shell, GitHub/Vercel/…

Model fabric  =  OpenLLM gateway + `openllm mcp`
                 routes inference across subscriptions/providers the user already pays for
                 MCP: native API + code/docs search + memory
```

OpenLLM does **not** replace GitHub, Vercel, or the orchestrator's coding tools. It supplies models and gateway MCP tools.

Connect instructions (CLI, env vars, remote MCP rules): [openllm-connect.md](./openllm-connect.md). Example stdio config: [mcp.stdio.example.json](./mcp.stdio.example.json).

## Diagram

```mermaid
flowchart TB
  user[User]

  subgraph orch["Orchestrator — one bot folder"]
    agent["Grok Bot / Muse / Cursor agent / Hermes / …"]
  end

  subgraph fabric["Model fabric — OpenLLM (shared)"]
    mcp["openllm mcp stdio"]
    gw["Gateway origin<br/>OPENLLM_CLOUD_ORIGIN"]
    groups["MCP groups<br/>native API · context/search · memory"]
  end

  subgraph others["Other connectors — unchanged"]
    gh[GitHub]
    vercel[Vercel]
    more[Slack, browsers, …]
  end

  user --> agent
  agent --> mcp
  mcp --> groups
  mcp --> gw
  gw -->|"OpenAI-compatible /v1<br/>models, chat/completions, search"| providers["User's paid providers / subscriptions"]
  agent --> gh
  agent --> vercel
  agent --> more
```

Cursor loads [`bots/cursor/mcp.json`](../bots/cursor/mcp.json) and substitutes `${OPENLLM_API_KEY}` / `${OPENLLM_CLOUD_ORIGIN}` from Plugins → Configure.

Grok Bot needs the same server added as a **custom MCP** (a template share does not carry another owner's connector). See [bots/grok/docs/setup.md](../bots/grok/docs/setup.md).

## Two operating modes

| Mode | Orchestrator does | OpenLLM does |
| --- | --- | --- |
| **Dashboard** | Chooses read/mutate tools, explains results, asks approval for writes | Account API via MCP (usage, models, keys/devices, providers, config) |
| **Development execution** | Clarifies goal, edits code, tests, git, PRs, deploys | Catalog + optional completions hop + context/memory tools |

Browser on [openllm.sh](https://openllm.sh) is a **fallback** when MCP/API lacks a surface.

## MCP groups (discover live names)

The CLI's unified server (`openllm mcp`) exposes groups. Upstream currently documents native API plus code/docs search and memory; labels have appeared as `openllm-context` / `claude-context` and `openllm-memory` / `supermemory`. Skills talk about **jobs**, not frozen function names.

Native tools are generated from the same OpenAPI document the gateway serves at `/api/swagger` (also `openllm api --spec`). Useful landmarks:

- Inference: `/v1/models`, `/v1/chat/completions`, `/v1/messages`, `/v1/responses`, `/v1/search`
- Account: `/stats`, `/keys`, `/credentials`, `/providers/custom`, `/config/user`, `/billing`, `/user`

## Trust boundaries

- API keys stay in plugin variables, MCP env, or `~/.openllm/.env` — never in git.
- Provider credentials live in OpenLLM's vault model (see OpenLLM's own security docs). These bots do not proxy them.
- Repo secrets and deploy tokens stay on GitHub/Vercel (or whatever the project already uses).
- This repo does **not** ship API keys or guessed remote MCP URLs.

## References

- OpenLLM: [https://openllm.sh](https://openllm.sh)
- CLI / MCP: [https://github.com/openllmsh/cli/tree/prerelease](https://github.com/openllmsh/cli/tree/prerelease)
- This monorepo: [https://github.com/MindDragonLabs/openllm-bots](https://github.com/MindDragonLabs/openllm-bots)
- Predecessor (flat plugin): [https://github.com/MindDragonLabs/grok-openllm-orchestrator](https://github.com/MindDragonLabs/grok-openllm-orchestrator)
- Cursor plugins: [https://cursor.com/docs/reference/plugins](https://cursor.com/docs/reference/plugins)
