# Sample flows

Worked examples of the orchestrator pattern. Model ids and chains are
illustrative — run `models` against the real gateway.

## 1. Cheap summarization

**User:** "Summarize this thread with the cheapest option."

**Agent:**
1. (Knows from the usage index that the `cheap` chain routes to low-cost
   models.)
2. Runs: `openllm_cli.py chat --model cheap --message "<thread text>"`
3. Gateway serves via its second hop after the first fails.
4. Replies with the summary, plus: "Served by <hop model>, 1,204 tokens."

## 2. Model comparison

**User:** "Which writes a better haiku about debugging, model A or B?"

**Agent:**
1. Runs the same prompt against both model ids.
2. Presents both haikus side by side with token counts.
3. Asks which the user prefers — does not declare a winner unilaterally.

## 3. Multi-connector workflow

**User:** "Pull the Q3 notes from Drive and turn them into action items."

**Agent:**
1. Google Drive connector → fetches the doc text.
2. `openllm_cli.py chat --model <frontier-chain> --system "Extract action
   items as a checklist with owners." --message "<doc text>"`
3. Writes the checklist to the user's tracker.
4. Reports: items extracted, model served, tokens used.

## 4. Guarded batch job

**User:** "Score these 10 headlines with two models each."

**Agent:**
1. Checks spend state first: "This will be ~20 calls, roughly X tokens
   against your $Y cap. Go ahead?"
2. On approval, runs the calls sequentially (respecting cooldowns).
3. Returns a compact table: headline × model → score, with totals.
