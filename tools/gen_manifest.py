#!/usr/bin/env python3
"""Generate (or verify) the stdlib compatibility manifest.

The manifest (schema mncs.stdlib-manifest/1) is the machine-readable
composition contract: bundle identity, required source-profile range,
and the per-module table with digests. Generated from the bundle pin,
which is generated from library/:

    library/ --(mncs bundle generate)--> dist/stdlib-bundle.json
             --(gen_manifest.py)--> stdlib-manifest.json

Usage:
    python3 tools/gen_manifest.py [--check] [--root DIR]

--check verifies the committed manifest matches a fresh generation
and fails closed on any drift (module set, digests, profiles, bundle
identity). Pure stdlib; no toolchain needed.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

SCHEMA = "mncs.stdlib-manifest/1"

MODULE_RE = re.compile(r"^module\s+([\w.]+);", re.M)
PROFILE_RE = re.compile(r"^mncs\s+([0-9.]+);", re.M)
USE_RE = re.compile(r"^use\s+([\w.]+?)(?:\s+as\s+\w+)?;", re.M)


def profile_key(profile):
    return tuple(int(part) for part in str(profile).split("."))


def bundle_identity_for(modules):
    ordered = sorted((m["name"], m["content_sha256"]) for m in modules)
    digest = hashlib.sha256()
    for name, content in ordered:
        digest.update(name.encode("utf-8"))
        digest.update(b"\x00")
        digest.update(content.encode("utf-8"))
        digest.update(b"\n")
    return "mncs:stdlib-bundle:" + digest.hexdigest()


def collect_modules(library_root):
    modules = []
    for namespace in sorted(os.listdir(library_root)):
        ns_dir = os.path.join(library_root, namespace)
        if not os.path.isdir(ns_dir):
            continue
        for filename in sorted(os.listdir(ns_dir)):
            if not filename.endswith(".mncs"):
                continue
            path = os.path.join(ns_dir, filename)
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            module = MODULE_RE.search(text)
            profile = PROFILE_RE.search(text)
            if not module or not profile:
                raise SystemExit(f"error: {path} declares no module or profile")
            name = module.group(1)
            if not name.startswith("mncs."):
                continue
            uses = sorted(set(USE_RE.findall(text)))
            modules.append(
                {
                    "name": name,
                    "path": f"{namespace}/{filename}",
                    "profile": profile.group(1),
                    "content_sha256": hashlib.sha256(
                        text.encode("utf-8")
                    ).hexdigest(),
                    "imports": [u for u in uses if u.startswith("mncs.")],
                }
            )
    return modules


def source_commit(root):
    try:
        return (
            subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            )
            .stdout.strip()
        )
    except Exception:
        return "unknown"


def build_manifest(root):
    library_root = os.path.join(root, "library")
    modules = collect_modules(library_root)
    names = [m["name"] for m in modules]
    if len(set(names)) != len(names):
        dupes = sorted(n for n in set(names) if names.count(n) > 1)
        raise SystemExit(f"error: duplicate module names: {dupes}")
    profiles = sorted({m["profile"] for m in modules}, key=profile_key)
    bundle_path = os.path.join(root, "dist", "stdlib-bundle.json")
    try:
        with open(bundle_path, encoding="utf-8") as handle:
            bundle = json.load(handle)
    except (OSError, ValueError) as error:
        raise SystemExit(f"error: cannot read bundle pin {bundle_path}: {error}")
    if bundle.get("schema_version") != "mncs.stdlib-bundle/1":
        raise SystemExit("error: bundle pin has an unexpected schema")
    # The manifest re-derives the identity from tree content; the bundle
    # must agree exactly, otherwise pin and tree have diverged.
    derived = bundle_identity_for(modules)
    if derived != bundle.get("bundle_identity"):
        raise SystemExit(
            "error: bundle pin diverges from library/ "
            f"(pin {bundle.get('bundle_identity')}, tree {derived}); "
            "run ./tools/regen.sh"
        )
    return {
        "schema_version": SCHEMA,
        "repository": "mncs-stdlib",
        "source_commit": source_commit(root),
        "bundle_identity": derived,
        "bundle_path": "dist/stdlib-bundle.json",
        "library_path": "library",
        "requires_profile": {"min": profiles[0], "max": profiles[-1]},
        "module_count": len(modules),
        "modules": modules,
    }


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", default=DEFAULT_ROOT)
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    manifest = build_manifest(root)
    text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    manifest_path = os.path.join(root, "stdlib-manifest.json")
    if args.check:
        try:
            with open(manifest_path, encoding="utf-8") as handle:
                committed = handle.read()
        except OSError as error:
            raise SystemExit(f"error: cannot read {manifest_path}: {error}")
        if committed != text:
            raise SystemExit(
                f"error: {manifest_path} drifts from library/+dist; "
                "run ./tools/regen.sh"
            )
        print(f"manifest current: {manifest['module_count']} modules, "
              f"profiles {manifest['requires_profile']['min']}.."
              f"{manifest['requires_profile']['max']}, "
              f"{manifest['bundle_identity'][:32]}...")
        return 0
    with open(manifest_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(f"wrote {manifest_path}: {manifest['module_count']} modules")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
