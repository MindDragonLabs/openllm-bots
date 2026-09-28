---
name: openllm-dev-task
description: Execute a coding or development task with Hermes as orchestrator and OpenLLM as model fabric (gateway models, completions hop, code/docs search, memory). Use when the user wants implementation work, not account inspection.
---

# Development execution mode (Hermes)

**You** (Hermes) own the plan, the repo, tests, git, and deploys. **OpenLLM** supplies the model fabric: catalog, optional specialist inference, code/docs context search, cross-session memory.

Do not send the project "into OpenLLM to implement." Implement with Hermes' own tools; use the gateway where it adds value.

Architecture: [shared/architecture.md](../../../../shared/architecture.md). If MCP is missing: **openllm-connect** / [docs/setup.md](../../docs/setup.md).

## Recipe

### 1. Clarify the goal
One sentence: outcome, repo/path, definition of done. One question max, then proceed.

### 2. Pick a model via the gateway
list models via the live MCP tool (e.g. `mcp_openllm_api_v1Models_list` on openllm CLI 2.6.36 — **discover the actual name first**, it may differ) → choose from **returned ids** (chain aliases included). Match the job: coding-capable entry for implementation; stronger reasoning entry for hard review; small/fast for classify-summarize. Say which id and why. If listing fails, continue with your default model and say the catalog was unavailable.

### 3. Gather context
- **Repo:** Hermes-native tools — `read_file`, `search_files`, terminal, tests.
- **OpenLLM code/docs search:** index once, then search (landmark names from 2.6.36: `index_codebase` / `index_docs`, then `search_code` / `search_docs` — discover live). Library docs, indexed code, public references.
- **Memory:** `memory` / `recall` for prior decisions. No secrets there.

Skip absent groups; never fake results.

### 4. Implement with Hermes tools
Edit (`patch`/`write_file`), lint, test, commit — Hermes' own toolset. PRs via `gh`; deploys via Vercel/whatever the project uses. OpenLLM replaces none of that.

### 5. Optional specialist hop
Second opinion or different model family: the live chat-completions tool (2.6.36 landmark: `mcp_openllm_api_v1ChatCompletions_chatCompletions`; also `/v1/messages`, `/v1/responses` variants — discover live) with a **tight prompt and relevant snippets** — never the whole repo. You apply or reject the output in the working tree.

### 6. Report
- What changed (files, behavior).
- Which OpenLLM models/tools used.
- Verification run (tests, commands, exit codes).
- What you did **not** do via OpenLLM (e.g. "opened the PR myself with gh").

## Anti-patterns

- Treating OpenLLM MCP as a shell that writes the repo
- Inventing model ids or tool names
- `OPENLLM_API_KEY` in source, CI logs, or shared skills
- Skipping tests because a gateway model "looked correct"
- Dashboard mutation tools mid-coding-task

## Loop-in dashboard
Blocked on quota, missing provider, unknown model id → **openllm-dashboard**, then resume.
