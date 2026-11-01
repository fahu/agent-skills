---
name: pstack-statechart
description: "pstack: Check a TLA+ model of a system that moves between states, such as a product flow, a protocol, or a service, and draw it as a Mermaid statechart. The report gives the shortest path to each state that breaks a rule. Use for $pstack-statechart, or to show a bug as a path through states."
license: MIT
---

# pstack · statechart

This is a Codex adaptation of Lauren Tan’s **pstack**, pinned in
[upstream.lock.json](../pstack/.bundle/upstream.lock.json).

This entrypoint requires the `pstack` skill alongside it. If
`../pstack/.bundle/codex.md` is missing, stop and ask to install `pstack`
from the same reviewed revision.
Do not fetch or install dependencies during a workflow.

1. Read [the Codex adapter](../pstack/.bundle/codex.md) before following upstream material.
   It replaces incompatible tool, model, autonomy, and path instructions.
   Applicable project instructions and the user’s request take precedence.
2. Read [the upstream workflow](../pstack/.bundle/upstream/skills/statechart/SKILL.md)
   and apply it through that adapter. Load supporting files only as needed.
3. Route cross-skill calls through the prefixed entrypoints in `../pstack/.bundle/skills/`.
   Resolve other relative references beside the original upstream file.
   Report missing required capabilities; do not claim skipped checks passed.
