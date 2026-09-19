# 02 — Prerequisites

Before touching any tooling, confirm these with the user.

1. **An openllm.sh account.** The user signs up at openllm.sh themselves.
2. **The API base URL.** From their dashboard. Do not guess it (common shape is
   an OpenAI-compatible `…/v1`, but the dashboard is the source of truth). You
   need the exact **bare hostname** (e.g. `api.openllm.sh`) for the credential
   setup — egress is locked to declared hosts.
3. **A scoped `sk-llm` key.** Ask the user to generate one on the openllm.sh
   dashboard scoped to this integration:
   - Name it something like `muse-connector`.
   - Set a spend cap / cooldown if the dashboard offers it.
   - It must be revocable independently of their other keys.
   - Never ask for the key in chat. It is collected via the secure card in
     `03-credential-setup.md`.
4. **(Optional) A named fallback chain.** If the user has configured chains on
   the dashboard (e.g. `cheap`, `frontier`), get the chain names — the
   orchestrator can target chains instead of single models.
