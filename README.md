# Fahu agent skills

A Codex skill pack with the pstack adaptation and pinned Cloudflare and Matt Pocock skills.

## Install skills

Run these commands from the destination project.

```sh
npm install -D skills@1.7.4 github:fahu/agent-skills --allow-git=root
npx skills experimental_sync --agent codex --yes
```

If you previously installed this library with `skills add`, remove that source before syncing. Use `npx skills remove fahu/skills --yes`, with the source name recorded in `skills-lock.json`.

Commit `package-lock.json` and `skills-lock.json` with `package.json`. For a fresh checkout, run `npm ci --allow-git=root` followed by the sync command. The `--allow-git=root` option permits direct Git dependencies in npm 12.

## Configure a project

For Matt Pocock workflows such as `to-spec` and `triage`, invoke this once in the destination project's Codex chat.

```text
$setup-matt-pocock-skills
```

Commit the generated `docs/agents/*.md` files and the updated `AGENTS.md` or `CLAUDE.md`. [Setup skill](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/setup-matt-pocock-skills/SKILL.md)

## Maintain the collection

Update the `skills` array in `package.json` to change the selection or upstream revisions. Use full commit SHAs. After editing the pstack adaptation, regenerate and verify the exports.

```sh
npm run skills:build
npm run check
```
