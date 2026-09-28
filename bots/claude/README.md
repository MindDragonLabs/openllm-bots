# Claude Code

**Orchestrator:** Claude Code (`claude`)
**Model fabric:** [OpenLLM](https://openllm.sh) via Anthropic-compatible base URL
**Status:** ready ([`bot.manifest.json`](./bot.manifest.json)) · verified live 2026-09-28 (loopback gateway; see caveat) against Claude Code 2.1.282

Claude Code keeps planning, tools, approvals, and file/git access. OpenLLM becomes the model fabric: every completion is routed through the OpenLLM gateway instead of a first-party Anthropic endpoint.

| Role | Who | Does |
| --- | --- | --- |
| **Orchestrator** | Claude Code | Plans, tools, approvals, terminal/files/git, subagents, skills |
| **Model fabric** | OpenLLM gateway | Models, completions, routing across your existing providers |

```text
claude  →  ANTHROPIC_BASE_URL  →  OpenLLM gateway  →  models you already pay for
```

Shared docs: [architecture](../../shared/architecture.md) · [connect rules](../../shared/openllm-connect.md) · [harness survey](../../docs/harness-survey.md)

## Attach (summary)

Export two environment variables before launching `claude`:

```sh
export ANTHROPIC_BASE_URL="http://127.0.0.1:8787"      # OpenLLM gateway root — no /v1 suffix
export ANTHROPIC_AUTH_TOKEN="$OPENLLM_API_KEY"          # OpenLLM API key, not an Anthropic key
unset ANTHROPIC_API_KEY                                  # avoid conflicting auth sources
```

Verify headless:

```sh
claude -p --model <gateway-model-id> "Reply with exactly: OPENLLM-OK"
```

A warning about claude.ai connectors appears when `ANTHROPIC_API_KEY` is set — that is the signal it is overriding your gateway auth. Unset it (as above); `ANTHROPIC_AUTH_TOKEN` then carries the gateway key. Pick `<gateway-model-id>` from the gateway's `/v1/models` list, not from memory.

Copy-paste steps, model ids, and pitfalls: [docs/setup.md](./docs/setup.md).

## What changes

- Requests go to the OpenLLM gateway; OpenLLM routes to whichever provider/subscription it fronts.
- Model ids become **gateway catalog ids** (`grok/grok-4.7`, `kimi_code/k3`, chain aliases like `lite`/`plus`/`ultra`). Do not invent ids — list them from the gateway.
- Skills, hooks, subagents, MCP, and permission modes are unchanged; only the endpoint moves.

## Loopback caveat

"Verified live" means a real completion routed through an OpenLLM gateway on the date shown. The survey gateway runs on loopback, where the daemon does not enforce request authentication — the runs prove routing and request shape, not key transport. See [the survey method note](../../docs/harness-survey.md).

## Gotchas

- **No `/v1` suffix.** Claude Code appends the Anthropic path itself. Point at the gateway root.
- **`ANTHROPIC_AUTH_TOKEN`, not `ANTHROPIC_API_KEY`** — the token var is the supported gateway-auth path; a set `ANTHROPIC_API_KEY` can take precedence and break routing.
- **Model metadata warnings** for gateway ids (e.g. `grok/grok-4.7`) are cosmetic; the completion still routes.
- Claude Code expects Anthropic-protocol models on the far side of the base URL. Route to Anthropic-protocol-capable models or the gateway's Anthropic-compat surface when in doubt.
