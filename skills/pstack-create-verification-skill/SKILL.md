---
name: pstack-create-verification-skill
description: "pstack: Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for $pstack-create-verification-skill, \"make a control skill for this repo\", or when a project has no scripted way to prove UI/CLI/service behavior."
license: MIT
---

# pstack · create-verification-skill

This is a Codex adaptation of Lauren Tan’s **pstack**, pinned in
[upstream.lock.json](../pstack/.bundle/upstream.lock.json).

This entrypoint requires the `pstack` skill alongside it. If
`../pstack/.bundle/codex.md` is missing, stop and ask to install `pstack`
from the same reviewed revision.
Do not fetch or install dependencies during a workflow.

1. Read [the Codex adapter](../pstack/.bundle/codex.md) before following upstream material.
   It replaces incompatible tool, model, autonomy, and path instructions.
   Applicable project instructions and the user’s request take precedence.
2. Read [the upstream workflow](../pstack/.bundle/upstream/skills/create-verification-skill/SKILL.md)
   and apply it through that adapter. Load supporting files only as needed.
3. Route cross-skill calls through the prefixed entrypoints in `../pstack/.bundle/skills/`.
   Resolve other relative references beside the original upstream file.
   Report missing required capabilities; do not claim skipped checks passed.
