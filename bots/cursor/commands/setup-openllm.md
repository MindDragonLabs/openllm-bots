---
name: setup-openllm
description: Connect OpenLLM MCP to Cursor or Grok Bot — CLI install, plugin variables, pairing, and verify tools.
---

# /setup-openllm

Run the **openllm-connect** skill (and **getting-started** if this is a first run).

Ask **one question at a time**. Do not request the API key and a custom origin in the same turn.

## Goal

1. Confirm an [OpenLLM](https://openllm.sh) account exists.
2. Confirm the CLI is installed (`openllm version`) **or** the dashboard one-click plugin path was used, then `~/.openllm/bin/openllm setup` if PATH is missing.
3. Collect `OPENLLM_API_KEY` (required) then `OPENLLM_CLOUD_ORIGIN` (optional, default `https://openllm.sh`).
4. Point the user at Plugins → Configure for this plugin's variables (Cursor) **or** a custom MCP connector (Grok Bot). Never write secrets into the repo.
5. Reload MCP and verify tools appear. Then offer **dashboard mode** or a **first development task**.

Canonical stdio config is this plugin's `mcp.json`: command `openllm`, args `["mcp"]`. Grok Bot owners: [bots/grok/docs/setup.md](../../grok/docs/setup.md) — template share cannot pack custom MCP.
