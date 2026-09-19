# 06 — Monitoring

An agent looping on fallback chains can burn real tokens. Set up a watchdog.

## Usage watchdog (scheduled)

Create a cron job (see `templates/cron/usage-watchdog.md`) that:

- Runs daily (or hourly during heavy-use periods).
- Calls `bin/openllm_cli.py usage` (GET of the gateway usage path; FILL
  `/usage` or `--usage-path` / `OPENLLM_USAGE_PATH`) for the scoped key
  (or the dashboard's reported spend, if no API exposes it).
- Compares against the key's spend cap.
- Stays silent when healthy; notifies the user at ~80% of cap; warns loudly
  at ~95%.

When creating it with `cron.add`, set `predicted_connector_permissions` to the
usage endpoint actually used, and give the job a clear title like
`OpenLLM spend watchdog`.

## Per-task discipline

- Before any batched or long-running job, state the estimated token cost and
  get the user's go-ahead when it is non-trivial.
- Prefer chains with cheaper fallbacks for bulk work; reserve frontier models
  for single high-value calls.
- If a scoped key supports cooldowns, respect them — back off instead of
  hammering.

## What to track

A lightweight line in the daily memory log is enough: date, total tokens,
spend vs. cap. Never log prompts or completions.
