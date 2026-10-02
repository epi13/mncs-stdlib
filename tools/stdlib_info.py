#!/usr/bin/env python3
"""Queryable stdlib index for agents, environment, and Doctor.

Pure stdlib, no toolchain: reads stdlib-manifest.json (+ module headers
on demand) and answers with bounded JSON or human-readable text.

    list                          compact module index (name, profile, digest)
    show <module>                 header contract + source path + imports
    lookup <term>                 case-insensitive substring search over
                                  module names and header summaries
    compatible --max-profile X    composition verdict against a toolchain
    manifest                      print the manifest path + bundle identity

All output is bounded (lookup caps at 25 hits) so this stays cheap in
projections and prompts. Nothing here prints the library into stdout.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.dirname(HERE)

LOOKUP_CAP = 25


def load_manifest(root):
    path = os.path.join(root, "stdlib-manifest.json")
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError) as error:
        raise SystemExit(f"error: cannot read stdlib manifest {path}: {error}")


def profile_key(profile):
    return tuple(int(part) for part in str(profile).split("."))


def header_summary(root, module):
    path = os.path.join(root, "library", module["path"])
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return ""
    parts = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("//") and not stripped.startswith("///"):
            text = stripped[2:].strip()
            if not text:
                if parts:
                    break
                continue
            parts.append(text)
            joined = " ".join(parts)
            if len(joined) > 200 or text.endswith("."):
                break
        elif parts:
            break
    return " ".join(parts)


def cmd_list(manifest, args):
    rows = [
        {
            "name": m["name"],
            "profile": m["profile"],
            "sha256": m["content_sha256"][:12],
        }
        for m in manifest["modules"]
    ]
    if args.json:
        print(json.dumps(rows))
    else:
        for row in rows:
            print(f"{row['name']}  profile={row['profile']}  sha={row['sha256']}")


def cmd_show(root, manifest, args):
    wanted = args.module
    matches = [m for m in manifest["modules"] if m["name"] == wanted]
    if not matches:
        # Unversioned fallback: unique prefix match on the name stem.
        stems = [m for m in manifest["modules"]
                 if m["name"] == wanted or m["name"].startswith(wanted + ".")]
        if len(stems) == 1:
            matches = stems
    if len(matches) != 1:
        raise SystemExit(f"error: no unique module {wanted!r}")
    module = matches[0]
    record = {
        "name": module["name"],
        "path": os.path.join("library", module["path"]),
        "profile": module["profile"],
        "sha256": module["content_sha256"],
        "imports": module.get("imports", []),
        "summary": header_summary(root, module),
    }
    if args.json:
        print(json.dumps(record))
    else:
        print(f"module:  {record['name']}")
        print(f"path:    {record['path']}")
        print(f"profile: {record['profile']}")
        print(f"sha256:  {record['sha256']}")
        print(f"imports: {', '.join(record['imports']) or '(none)'}")
        print(f"summary: {record['summary']}")


def cmd_lookup(root, manifest, args):
    term = args.term.lower()
    hits = []
    for module in manifest["modules"]:
        summary = header_summary(root, module)
        if term in module["name"].lower() or term in summary.lower():
            hits.append({"name": module["name"], "summary": summary})
            if len(hits) >= LOOKUP_CAP:
                break
    if args.json:
        print(json.dumps(hits))
    else:
        for hit in hits:
            print(f"{hit['name']}\n    {hit['summary']}")
        if not hits:
            print("(no matches)")


def cmd_compatible(manifest, args):
    required = manifest["requires_profile"]["max"]
    maximum = args.max_profile
    ok = profile_key(required) <= profile_key(maximum)
    record = {
        "compatible": ok,
        "requires_profile": manifest["requires_profile"],
        "toolchain_max_profile": maximum,
        "bundle_identity": manifest["bundle_identity"],
        "reason": (
            f"stdlib requires profiles ≤ {required}; "
            f"toolchain supports ≤ {maximum}"
        ),
    }
    if args.json:
        print(json.dumps(record))
    else:
        print(("compatible: yes" if ok else "compatible: NO")
              + f" ({record['reason']})")
    return 0 if ok else 3


def cmd_manifest(root, manifest, args):
    record = {
        "manifest": os.path.join(root, "stdlib-manifest.json"),
        "bundle": os.path.join(root, manifest["bundle_path"]),
        "library": os.path.join(root, manifest["library_path"]),
        "bundle_identity": manifest["bundle_identity"],
        "module_count": manifest["module_count"],
        "requires_profile": manifest["requires_profile"],
    }
    if args.json:
        print(json.dumps(record))
    else:
        for key, value in record.items():
            print(f"{key}: {value}")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=DEFAULT_ROOT)
    parser.add_argument("--json", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    show = sub.add_parser("show")
    show.add_argument("module")
    lookup = sub.add_parser("lookup")
    lookup.add_argument("term")
    compat = sub.add_parser("compatible")
    compat.add_argument("--max-profile", required=True)
    sub.add_parser("manifest")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    manifest = load_manifest(root)
    if args.command == "list":
        cmd_list(manifest, args)
    elif args.command == "show":
        cmd_show(root, manifest, args)
    elif args.command == "lookup":
        cmd_lookup(root, manifest, args)
    elif args.command == "compatible":
        return cmd_compatible(manifest, args)
    elif args.command == "manifest":
        cmd_manifest(root, manifest, args)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
