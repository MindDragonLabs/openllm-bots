---
name: openllm-dev-task
description: Execute a real coding or development task with the Cursor/Grok Bot orchestrator using OpenLLM for models, gateway chat/completions, search, and optional context/memory MCP. Use when the user wants implementation work, not only account inspection.
---

# Development execution mode

**You** (Cursor agent / Grok Bot) own the plan, the repo, tests, git, and deploy connectors.

**OpenLLM** supplies the model fabric: list/route models, optional specialist inference via the gateway, code/docs context search, and cross-session memory.

Do not send the whole software project “into OpenLLM to implement.” Implement with the orchestrator's normal coding tools.

Shared architecture: [shared/architecture.md](../../../../shared/architecture.md). If MCP is missing: **openllm-connect** / `/setup-openllm`.

## Recipe

### 1. Clarify the goal

One sentence: outcome, repo/path, and definition of done. If ambiguous, ask **one** question, then proceed.

If MCP is not connected, run **openllm-connect** / `/setup-openllm` first.

### 2. Pick a model via the gateway

Use the live models tool (OpenAPI: `GET /v1/models`). Choose from **returned ids** (including chain aliases if present). Match the job:

- implementation / refactor → a coding-capable catalog entry
- deep review or hard reasoning → a stronger reasoning entry if listed
- quick classify/summarize → a smaller/faster entry if listed

Tell the user which id you selected and why. If listing fails, continue with the orchestrator's default model and say OpenLLM catalog was unavailable.

### 3. Gather context (OpenLLM + repo)

- **Repo:** read files, search the tree, run tests — orchestrator tools.
- **OpenLLM code/docs search** (group `openllm-context` / `claude-context`, or `openllm exec ctx search` if you are in a shell with the CLI): library docs, indexed code, public references.
- **Memory** (`openllm-memory` / `supermemory`): prior decisions from other sessions. Do not store secrets there.

If those groups are absent, skip them; do not fake results.

### 4. Implement with orchestrator tools

Edit, lint, test, and commit using Cursor/Grok Bot coding tools (editor, shell, git).

Use **GitHub** for PRs/issues when that connector is available. Use **Vercel** (or the project's real host) for deploys. OpenLLM does not replace those.

### 5. Optional specialist hop through OpenLLM

When a second opinion or a different model family would help (tricky algorithm, alternative API shape, “what would this model name this function”), call the gateway chat/completions (or `/v1/messages` / `/v1/responses` if those tools exist) **with a tight prompt and relevant snippets** — not the entire repo.

OpenAPI landmarks (live MCP names may differ):

- `POST /v1/chat/completions`
- `POST /v1/messages`
- `POST /v1/search` for grounded lookup

You remain responsible for applying or rejecting that output in the working tree.

### 6. Report

- What changed (files, behavior)
- Which OpenLLM model / tools you used
- Tests or verification you ran
- What you did **not** do via OpenLLM (e.g. opened the GitHub PR yourself)

## Anti-patterns

- Treating OpenLLM MCP as a shell that writes the repo for you
- Inventing model ids or MCP tool names
- Putting `OPENLLM_API_KEY` in source, CI logs, or README samples
- Skipping tests because a gateway model “looked correct”
- Using dashboard mutation tools during a coding task unless the task is account-related

## Loop-in dashboard

If the task is blocked on quota, missing provider, or unknown model id, switch briefly to **openllm-dashboard**, then resume implementation.
