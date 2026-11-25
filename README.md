# Fahu agent skills

A Codex skill pack with the pstack adaptation and pinned Cloudflare and Matt Pocock skills.

## Install skills

Run this command from the destination project.

```sh
npx --yes skills@1.9.0 add fahu/agent-skills --agent codex --skill '*' --yes
```

Projects using Skills CLI sync can also declare `fahu/agent-skills` as a single GitHub source in their `package.json` skills array. Pin a commit to reproduce the same pack across checkouts.

## Configure a project

For Matt Pocock workflows such as `to-spec` and `triage`, invoke this once in the destination project's Codex chat.

```text
$setup-matt-pocock-skills
```

Commit the generated `docs/agents/*.md` files and the updated `AGENTS.md` or `CLAUDE.md`. [Setup skill](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/setup-matt-pocock-skills/SKILL.md)

## Maintain the collection

The third-party skill folders in `skills/` contain complete snapshots from these revisions. Each folder includes its upstream license.

- Cloudflare `security-audit` comes from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit).
- The 27 Matt Pocock skills come from [mattpocock/skills](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills).

When updating a third-party skill, copy the complete folder and its license, update the source revision above, and keep its discovery link in `.agents/skills/`.

After editing the pstack adaptation, regenerate and verify the exports.

```sh
npm run skills:build
npm run check
```
