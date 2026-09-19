# 08 — Limitations

Hard boundaries. Do not work around them; explain them.

1. **The daemon path doesn't travel.** Subscription traffic (Claude Pro/Max,
   ChatGPT Plus, etc.) is served by a local daemon on the user's hardware
   through official vendor CLIs, and the openllm.sh cloud refuses it. A Muse
   connector — emulated or official — only reaches the cloud gateway
   (BYO provider keys, custom endpoints). Never imply otherwise to the user.
2. **Per-user, not public.** The emulated skill runs on one Muse instance
   under one user's credential. It is not reviewed, not listed, and not
   transferable without repeating the setup.
3. **Zero-knowledge is a design constraint, not a slogan.** The service cannot
   decrypt the user's vault; the connector must uphold the same posture: key
   in memory per request, never persisted, never logged. Prompts and
   completions are never stored — metadata only.
4. **Spend is real money.** The gateway charges the user's own provider
   accounts (no markup, but real bills). The orchestrator must check caps
   before batch work and surface costs after it.
5. **No prompt inspection by the provider.** Because prompts stream through
   without storage, debugging a bad completion means re-running with
   variations — there is no server-side trace to pull.
