# 05 — Orchestrator patterns

You are the orchestrator. The skill is the connector. These are the recurring
flows — adapt the wording, keep the mechanics.

## Direct call

User: "Ask GPT-5 for three taglines for an ice cream shop."
You: `openllm_cli.py chat --model <gpt-id> --message "…"`. Return the text.
State which model served it.

## Cheap-chain routing

User: "Summarize this thread with the cheapest option."
You:
1. Consult the gateway's usage index / your memory of best-value models.
2. Call the cheap chain (or cheapest single model).
3. Return the summary + tokens used + which hop served it.

## Fallback-aware request

User: "Draft this with Claude, fall back to GPT if it's down."
You: target the user's chain that orders Claude first. The gateway handles
failover; your job is to report which hop actually answered. Your flow must
never assume the first choice served.

## Multi-connector workflow

User: "Pull the Q3 notes from Drive and turn them into action items."
You:
1. Google Drive connector → fetch the doc.
2. OpenLLM `chat` → extract action items.
3. Write the result to the user's tracker / file.
Each leg is one connector; you own the sequencing and the handoffs.

## Batched fan-out

User: "Score these ten headlines with two different models."
You:
1. Check spend state first — batched jobs burn tokens fast.
2. Run the calls (sequentially; note rate limits/cooldowns on the scoped key).
3. Present a compact comparison table, with per-call token counts.

## Rules for every pattern

- Never send a prompt you haven't read — no blind forwarding of user pastes
  into the gateway without understanding the task.
- Keep prompts and completions out of memory, logs, and files. Metadata only.
- If the user names a model you don't have, run `models` first and say what's
  actually available rather than guessing an id.
