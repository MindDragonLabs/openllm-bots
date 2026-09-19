# 01 — Overview

## What we're building

An emulated OpenLLM connector: Muse gains the ability to send prompts to any
model behind the user's openllm.sh gateway and get results back, with Muse
acting as the orchestrator (choosing models/chains, chaining with other tools,
enforcing spend discipline).

## Architecture

```
User (chat)
  │  "summarize this with the cheapest chain"
  ▼
Muse (orchestrator)
  │  decides model/chain, checks spend, builds the request
  ▼
openllm skill → bin/openllm_cli.py
  │  HTTPS, Authorization: Bearer sk-llm…
  ▼
openllm.sh gateway
  │  fallback chains, scoped-key accounting
  ▼
Providers (Anthropic, OpenAI, xAI, custom endpoints…)
```

## Pieces

- **Secure Vault** holds the `sk-llm` key. It is collected with
  `credentials.request_api_access` and injected at call time by the auth helper
  the scaffold generates. It is never written to disk, chat, or memory.
- **Workspace skill** at `~/workspace/skills/openllm/` with a `SKILL.md`
  (Purpose / Tooling / Auth / Operating Rules) and a CLI in `bin/`.
- **Orchestrator logic** lives in the conversation: Muse reads the skill, picks
  the model or chain, calls the CLI, and post-processes results. See
  `05-orchestrator-patterns.md`.
- **Monitoring** is a scheduled job that checks spend against the cap. See
  `06-monitoring.md`.

## Key facts about openllm.sh (verified from openllm.sh)

- One OpenAI-compatible endpoint; "just the base URL and key" to switch code.
- Keys look like `sk-llm…`; scoped keys exist (one key per app/device, own
  spend, own cooldown, revoked alone).
- Fallback chains: "ask for a chain, not a model. Whatever fails, the next hop
  answers."
- Free tier: 50M tokens/month, no card. Flat plan pricing, no token markup.
- Zero-knowledge: keys are AES-256-GCM encrypted in the user's browser under a
  recovery phrase; the service stores ciphertext. Prompts are not stored —
  metadata only (model, tokens, latency, cost).
- Subscription traffic (Claude Pro/Max, ChatGPT Plus, etc.) is served by a
  local daemon on the user's hardware via official vendor CLIs. The cloud
  refuses subscription traffic.
