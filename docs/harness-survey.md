# Harness Survey — OpenLLM Model Fabric Attachment

Living document. Last full pass: **2026-09-28** (macOS 26, arm64). Repo: MindDragonLabs/openllm-bots.

Goal: identify the top coding-agent harnesses, test each for OpenLLM attachment, record verdicts.
**Live** = a real completion routed through the OpenLLM gateway (`http://127.0.0.1:8787`, OpenAI-compatible `/v1` + Anthropic-compat root).

Per-harness setup docs live in `bots/<name>/docs/setup.md` when a bot folder exists.

## Results

| # | Harness | Binary | Ver | OpenLLM attach | Verdict |
|---|---------|--------|-----|----------------|---------|
| 1 | Claude Code | `claude` | 2.1.282 | `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` | **LIVE** (re-verified 2026-09-28) — [bots/claude](../bots/claude) |
| 2 | Codex CLI | `codex` | 0.157.0 | `model_providers` block, Responses wire API | **LIVE** (2026-09-28, was BLOCKED) — [bots/codex](../bots/codex) |
| 3 | OpenCode | `opencode` | 1.15.7 | `opencode.json` `@ai-sdk/openai-compatible` | **LIVE** (2026-09-28, was pending) — [bots/opencode](../bots/opencode) |
| 4 | Pi | `pi` | 0.73.1 | `~/.pi/agent/models.json` custom provider | **LIVE** (re-verified 2026-09-28) — [bots/pi](../bots/pi) |
| 5 | MiniMax Code | `mcode` | 0.4.12 | `mcode provider add`, `anthropic-messages` | **LIVE** (2026-09-28) — [bots/mcode](../bots/mcode) |
| 6 | ZCode | `zcode` | 3.14.3-28 | `~/.zcode/v2/provider_config.json` | **LIVE** (2026-09-28, new) — [bots/zcode](../bots/zcode) |
| 7 | Goose | `goose` | 1.52.0 | `GOOSE_PROVIDER=openai` + `OPENAI_BASE_URL` | **LIVE** (2026-09-19) |
| 8 | Aider | `aider` | 0.86.2 | `--openai-api-base` (`openai/<model>` prefix + `/v1`) | **LIVE** (2026-09-19) |
| 9 | Crush | `crush` | 0.96.1 | `~/.config/crush/crush.json` provider (`openai-compat`) | **LIVE** (2026-09-19) |
| 10 | Gemini CLI | `gemini` | 0.60.0 | `GOOGLE_GEMINI_BASE_URL` | **GATED** — Google-protocol auth, not OpenAI-compat |
| 11 | Qwen Code | `qwen` | 0.24.1 | `OPENAI_BASE_URL` | **PARTIAL** — reaches gateway; tool schema (missing `parameters`) rejected with 422 |
| 12 | Cursor CLI | `cursor-agent` | 2026.09.18 | — | pending (own model backend; Cursor plugin uses `openllm mcp` — [bots/cursor](../bots/cursor)) |
| 13 | Devin CLI | `devin` | 3000.11.3 | — | pending (Devin Cloud session required) |
| 14 | Grok CLI | `grok` | 1.0.41 | — | pending (xAI first-party; Grok Bot path uses `openllm mcp` — [bots/grok](../bots/grok)) |
| 15 | Kimi CLI | `kimi` | 2.1.0 | — | pending (Moonshot first-party) |
| 16 | Amp | — | — | not installed | **UNRESOLVED** — Sourcegraph; install path unclear |
| 17 | Plandex | — | — | not installed | **UNTESTED** — BYO-key, OpenAI-compatible custom provider likely viable; releases stalled since 2025 |
| 18 | Warp | — | — | not installed | **UNTESTED** — cloud-agent model, terminal agent config surface not verified |
| 19 | Amazon Q Developer CLI | `q` | — | not installed | **UNTESTED** — Bedrock-first; custom provider surface not verified |
| 20 | GitHub Copilot CLI | `copilot` | — | not installed | **UNTESTED** — GitHub-account auth; BYO-endpoint path not verified |
| 21 | MiniMax mmx | `mmx` | 1.0.26 | platform API key | authenticated — multimodal toolkit, not a coding agent; superseded by mcode here |
| 22 | CommandCode | `cmd` | 1.64.1 | own gateway | works as its own 72-model gateway, not an OpenLLM client |
| 23 | Claude Squad | `claude-squad` | 1.0.20 | — | orchestrates other agents' CLIs; inherits whatever each inner CLI uses |

## Attach methods that WORK (per harness type)

1. **Anthropic-compatible root URL** — Claude Code (`ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`), mcode (`--api-format anthropic-messages`). Point at the gateway root, **no `/v1`**.
2. **OpenAI-compatible `/v1` base URL** — OpenCode, Pi, Aider, Crush, Goose, zcode. Point at `<gateway>/v1`.
3. **OpenAI Responses wire API** — Codex (`wire_api = "responses"` under `/v1`).
4. **MCP (stdio)** — Hermes ([bots/hermes](../bots/hermes)), Cursor ([bots/cursor](../bots/cursor)). `openllm mcp` exposes the gateway tool surface.
5. **Emulated skill + vault** — Muse ([bots/muse](../bots/muse)).

## Credentials state (survey host)

- OpenLLM key: `~/.openllm/.env` (`OPENLLM_API_KEY`) — never written into this repo.
- mcode home: `~/.minimax-code/` (v0.4.12); custom provider `openllm` registered.
- zcode provider file: `~/.zcode/v2/provider_config.json` (mode 600).
- mmx/mcode MiniMax platform key: seeded separately from `~/.hermes/.env`.

## Gotchas found

- **OpenLLM chain aliases route per-harness.** `lite` → claude_code (declined) + chatgpt (needs codex signed in). Direct model ids (`grok/grok-4.5+`, `kimi_code/*`) are the reliable path.
- **Codex was blocked, now works.** Requires `wire_api = "responses"` (chat removed in 0.153+), `env_key` (not hardcoded key), and `web_search = "disabled"` — the daemon rejects codex's cache-only web-search policy with `unsupported_web_search_policy`.
- **mcode needs Anthropic wire format.** `openai-completions` requests from mcode are rejected by the gateway with a 400 schema error; `anthropic-messages` against the root passes.
- **zcode needs three config parts.** Provider rule + manual model rule per catalog-unknown id + `defaultModelSelection`, or the first prompt fails with `Select a model before continuing`.
- **OpenCode needs `--model` on `run`.** Without it, the configured default (subscription agent) is used — error surfaces as `Insufficient account funds`.
- **Qwen tool schema** sends tools without `parameters`; gateway 422s. Fix on Qwen side or tolerate in gateway.
- **Gemini CLI** is Google-protocol only; OpenAI-compat base URL won't work.
- **Crush `providers.json`** is regenerated by `crush models` — use `~/.config/crush/crush.json` (survives).
- **Pi compat flags.** `supportsDeveloperRole: false` and `supportsReasoningEffort: false` prevent gateway-side rejects.
- **Claude Code auth precedence.** Unset `ANTHROPIC_API_KEY`; use `ANTHROPIC_AUTH_TOKEN` for gateway auth.
- **Reasoning models ignore `max_tokens`** (kimi); drop the cap for clean responses.
