---
name: openllm-dev-task
description: Run a structured development task with the Cursor/Grok Bot orchestrator plus OpenLLM models and gateway MCP.
---

# /openllm-dev-task

Follow the **openllm-dev-task** skill.

You (Cursor agent / Grok Bot) own the plan, repo edits, tests, git, and any GitHub/Vercel (or other) connectors.

OpenLLM supplies:

- model listing and routing through the gateway
- optional specialist hops via chat/completions (or equivalent live MCP ops)
- code/docs context search and cross-session memory when those MCP groups are connected

## Kickoff (one question at a time if anything is missing)

1. Restate the user goal in one sentence and confirm.
2. Confirm OpenLLM MCP tools are live; if not, run `/setup-openllm` first.
3. Pick a model from the gateway catalog (do not invent IDs).
4. Execute: context → implement with normal coding tools → optional OpenLLM model hop → report.

Do not treat OpenLLM as a replacement for GitHub, Vercel, or the editor.
