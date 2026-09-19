# 07 — Official path (graduating to the directory)

The emulated skill is private to one user. To ship to everyone, submit at
`muse.ai/platform`:

1. **Describe your product** — what the connector does and how users will use
   it. (The Purpose section of your SKILL.md is a good first draft.)
2. **Submit for review** — Meta checks functional, security, and legal
   requirements, plus end-to-end testing. Expect scrutiny on: key handling
   (zero-knowledge story helps here), prompt/completion retention (keep the
   metadata-only posture), and spend guardrails (caps, per-task estimates).
3. **Appear in the directory** — users find it in Muse; editors review for
   featured placement.

Notes for the submission:

- Be explicit that the connector covers the **cloud gateway only** — the local
  daemon subscription path cannot travel through a cloud connector.
- Meta has partnered with Stripe (Link) so connectors can accept payments.
  OpenLLM charges a flat plan with no token markup, so billing likely stays on
  their dashboard — say so rather than wiring payments that don't fit.
- The custom-connector flow (API key pasted through Muse's secure flow, no
  directory listing) already exists for private use; the directory is the
  public tier above it.
