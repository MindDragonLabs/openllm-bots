# Claude Code setup

Copy-pasteable path for attaching Claude Code to OpenLLM. Claude Code is the orchestrator; OpenLLM is the model fabric.

- Architecture: [shared/architecture.md](../../../shared/architecture.md)
- Connect rules: [shared/openllm-connect.md](../../../shared/openllm-connect.md)
- Harness survey: [docs/harness-survey.md](../../../docs/harness-survey.md)

Verified: Claude Code **2.1.282**, macOS arm64, local OpenLLM gateway `http://127.0.0.1:8787`, 2026-09-28.

## Prerequisites

- OpenLLM account + API key (`sk-llm`): [openllm.sh](https://openllm.sh)
- Claude Code installed: `npm install -g @anthropic-ai/claude-code` (or your existing install)
- The OpenLLM gateway reachable from this machine (local daemon or a gateway host you control)

## 1. Put the key in your shell env

Add to your shell profile (or a session export):

```sh
export OPENLLM_API_KEY="sk-llm-..."
```

Never hardcode the key into CLAUDE.md, skills, or any committed file.

## 2. Point Claude Code at the gateway

```sh
export ANTHROPIC_BASE_URL="http://127.0.0.1:8787"   # gateway root, NO /v1
export ANTHROPIC_AUTH_TOKEN="$OPENLLM_API_KEY"
unset ANTHROPIC_API_KEY
```

`ANTHROPIC_API_KEY` unset matters: when it is set, Claude Code warns that it takes precedence over claude.ai auth and connectors; the gateway token must be the only auth source.

## 3. Verify headless

```sh
claude -p --model <gateway-model-id> "Reply with exactly: OPENLLM-OK"
```

Replace `<gateway-model-id>` with an id your gateway actually lists (step 4) — do not invent one. Expected: `OPENLLM-OK`. On success every subsequent `claude` session in this shell routes through OpenLLM.

## 4. Model ids

Claude Code sends Anthropic-protocol requests. Use the gateway's Anthropic-compat surface and ids — list what your gateway exposes before choosing:

```sh
curl -s http://127.0.0.1:8787/v1/models \
  -H "Authorization: Bearer $OPENLLM_API_KEY" | jq -r '.data[].id' | head -30
```

Gateway catalog ids look like `grok/grok-4.7`, `kimi_code/k3`, plus chain aliases (`lite`, `plus`, `ultra`). Unknown-model warnings are cosmetic; a hard 4xx means the id is not in the catalog.

## 5. Persist per-project (optional)

For a repo-scoped setup, use a wrapper script (not a `.env` file — Claude Code does not source one, `unset` cannot be expressed there, and `.env` files are often committed):

```sh
#!/bin/sh
export ANTHROPIC_BASE_URL="http://127.0.0.1:8787"
export ANTHROPIC_AUTH_TOKEN="$OPENLLM_API_KEY"
unset ANTHROPIC_API_KEY
exec claude "$@"
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `claude.ai connectors are disabled...` warning | `ANTHROPIC_API_KEY` still set | `unset ANTHROPIC_API_KEY`; rely on `ANTHROPIC_AUTH_TOKEN` |
| 401 / 403 from gateway | wrong or missing token | Re-export `ANTHROPIC_AUTH_TOKEN="$OPENLLM_API_KEY"` |
| 404 on requests | base URL has `/v1` (or another path) appended | Use the bare gateway root |
| `unknown model` hard error | id not in gateway catalog | Pick an id from `/v1/models` |
| Slow first response | gateway cold-start / provider routing | Retry; check gateway logs |
