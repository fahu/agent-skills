# Codex skills

Install all 62 skills from this repository with the standard [skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills@1.7.4 add fahu/skills --skill '*' --agent codex
```

| Skill group | Included skills |
| --- | --- |
| `coding-conventions` | Multiline `if` statements with explicit block bodies |
| `commits` | Atomic commits and conventional commit messages |
| `github-pr-management` | Review feedback, fixes, and reviewer replies |
| `pstack` | 59 prefixed entrypoints, including `$pstack` and `$pstack-how`, with the complete pinned upstream bundle |

## Select skills

Install a standalone skill by name:

```sh
npx skills@1.7.4 add fahu/skills --skill coding-conventions --agent codex
npx skills@1.7.4 add fahu/skills --skill commits --agent codex
npx skills@1.7.4 add fahu/skills --skill github-pr-management --agent codex
```

The `pstack` skill contains the shared adapter, supporting files, and internal workflow entrypoints. Include it whenever you select a `pstack-*` entrypoint:

```sh
npx skills@1.7.4 add fahu/skills --skill pstack pstack-how --agent codex
```

The CLI does not install skill dependencies automatically. Selecting `pstack` alone installs its help router and all supporting workflows; selecting additional entrypoints makes their individual `$pstack-*` names discoverable. The shared snapshot is stored once, inside the `pstack` skill.

Run the command from the destination project. The CLI installs project-local skills unless you select its global option. Installation does not activate pstack workflows or grant permission for external actions. Most pstack entrypoints preserve upstream's explicit-only invocation policy.

## Declare and restore skills

A consumer can declare this repository alongside the Vercel sources in `package.json`:

```json
{
  "skills": [
    { "source": "fahu/skills" }
  ]
}
```

Use `skills add` to record your selection in `skills-lock.json`. To select a reviewed revision, use a GitHub tree URL with the full commit SHA in place of `main`. Commit the lock file, then restore its pinned revisions in a fresh checkout:

```sh
npx skills@1.7.4 experimental_install
```

The declaration identifies the source; the lock file records the selected skills and revisions. In a project that already depends on `skills`, its npm installation task can run `skills experimental_install` directly. No `fahu-skills install` step is required.

## Installed layout

A complete Codex installation has this structure:

```text
.agents/skills/
  coding-conventions/
  commits/
  github-pr-management/
  pstack/
    SKILL.md
    .bundle/               Hidden supporting files
      codex.md
      upstream/            Complete pinned snapshot
      upstream.lock.json
      skills/              Internal workflow entrypoints
      scripts/
  pstack-how/
  pstack-.../               Other discoverable entrypoints
```

Every public pstack entrypoint refers to the shared `pstack` skill. Cross-workflow calls use its internal entrypoints, including when only a subset of public names is installed. The hidden `.bundle/` directory keeps the preserved upstream `SKILL.md` files and internal entrypoints outside Codex discovery. The standard CLI copies the committed files without rewriting their paths. Installed skills work independently of npm's cache and `node_modules`.

## Maintain and verify the repository

The canonical pstack entrypoints remain inside `skills/pstack/.bundle/skills/`. After editing them, regenerate the committed public exports and check their references, invocation policies, and snapshot integrity:

```sh
npm run skills:build
npm run check
```

The checkout's `.agents/skills/` links point to the public skill folders. The export generator is a repository maintenance command; consumers never run it.

To verify a complete installed bundle, run:

```sh
python3 .agents/skills/pstack/.bundle/scripts/verify.py --require-all
```

Omit `--require-all` when you intentionally installed a subset of public pstack entrypoints. The verifier still checks the complete upstream snapshot and every internal workflow. For legacy npm distribution, verify the packed tarball too: npm omits upstream `.gitignore`, which the legacy installer restores from its hash-checked fallback.

See [pstack's source pin and tool mapping](skills/pstack/.bundle/README.md), [unsupported features](skills/pstack/.bundle/codex.md), and [installation checks](skills/pstack/.bundle/SMOKE-TEST.md). The CLI integration is tested with `skills@1.7.4`; the restore command remains experimental.

## Licenses

pstack's [MIT license](skills/pstack/.bundle/upstream/LICENSE) and the commits skill's [Apache-2.0 license](skills/commits/LICENSE) are preserved with their files. Importing a skill does not change its license or project instructions.
