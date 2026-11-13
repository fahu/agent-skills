#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True

from export import entrypoints, exported_files


def verify(root, require_all=False):
    lock = json.loads((root / "upstream.lock.json").read_text())
    errors = []
    snapshot = root / lock["snapshot"]
    expected_files = set(lock["files"])
    actual_files = {
        path.relative_to(snapshot).as_posix()
        for path in snapshot.rglob("*") if path.is_file()
    }
    package = root.parents[2]
    # npm omits the upstream Git ignore file from the installed package.
    if (
        ".gitignore" not in actual_files
        and package.name == "skills"
        and package.parent.name == "@fahu"
        and package.parent.parent.name == "node_modules"
    ):
        expected_files.discard(".gitignore")
    if actual_files != expected_files:
        errors.append(f"Snapshot file set changed: {actual_files ^ expected_files}")
    for name, recorded in lock["files"].items():
        path = snapshot / name
        if not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != recorded["sha256"]:
            errors.append(f"Snapshot content changed: {name}")
        if bool(path.stat().st_mode & 0o111) != recorded["executable"]:
            errors.append(f"Snapshot executable mode changed: {name}")
        if path.is_symlink():
            errors.append(f"Unexpected snapshot symlink: {name}")

    source_names = {path.parent.name for path in (snapshot / "skills").glob("*/SKILL.md")}
    if source_names != set(lock["commands"]):
        errors.append("Command map does not cover exactly the upstream public skills")
    entries = entrypoints(lock)
    if set(path.name for path in (root / "skills").iterdir()) != set(entries):
        errors.append("Local entrypoints differ from the command map")

    discovery = root.parent.parent
    installed_count = 0
    for name, entry in entries.items():
        folder = root / entry["path"]
        manifest = folder / "SKILL.md"
        if not manifest.is_file():
            errors.append(f"Missing entrypoint: {name}")
            continue
        content = manifest.read_text()
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"Invalid skill name: {name}")
        if f"\nname: {name}\n" not in content:
            errors.append(f"Entrypoint name does not match folder: {name}")
        if "../../codex.md" not in content:
            errors.append(f"Entrypoint does not load the adapter: {name}")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" not in target and not (folder / target.split("#")[0]).exists():
                errors.append(f"Broken entrypoint reference: {name}: {target}")
        metadata = folder / "agents" / "openai.yaml"
        if not metadata.is_file():
            errors.append(f"Missing Codex metadata: {name}")
        else:
            expected_policy = entry["allow_implicit_invocation"]
            match = re.search(r"allow_implicit_invocation: (true|false)", metadata.read_text())
            actual_policy = match is None or match[1] == "true"
            if actual_policy != expected_policy:
                errors.append(f"Invocation policy changed: {name}")
        exported = discovery / name
        if not exported.is_dir():
            if require_all or name == "pstack":
                errors.append(f"Missing exported entrypoint: {name}")
            continue
        installed_count += 1
        if not metadata.is_file():
            continue
        for relative, expected in exported_files(root, name, entry).items():
            installed = exported / relative
            if not installed.is_file() or installed.read_bytes() != expected:
                errors.append(f"Incorrect exported entrypoint: {name}/{relative}")
        installed_manifest = exported / "SKILL.md"
        if installed_manifest.is_file():
            for target in re.findall(r"\]\(([^)]+)\)", installed_manifest.read_text()):
                if "://" not in target and not (exported / target.split("#")[0]).exists():
                    errors.append(f"Broken exported reference: {name}: {target}")

    exposed = {path.name for path in discovery.glob("pstack*")}
    if exposed - set(entries) or (require_all and exposed != set(entries)):
        errors.append(f"Unexpected discovery set: {exposed ^ set(entries)}")

    repository_discovery = discovery.parent / ".agents" / "skills"
    if repository_discovery.is_dir():
        for name in entries:
            link = repository_discovery / name
            if not link.is_symlink() or link.resolve() != (discovery / name).resolve():
                errors.append(f"Incorrect repository discovery link: {name}")
    return errors, len(expected_files), len(entries), installed_count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check the pinned pstack bundle and installed exports.")
    parser.add_argument("--require-all", action="store_true", help="Require every exported pstack entrypoint.")
    args = parser.parse_args()
    errors, file_count, skill_count, installed_count = verify(
        Path(__file__).resolve().parents[1], args.require_all
    )
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    print(f"PASS: {file_count} unchanged upstream files; {skill_count} bundled entrypoints; "
          f"{installed_count} installed exports.")
