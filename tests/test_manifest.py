"""Manifest, bundle, and tree consistency (no toolchain needed).

The manifest is the composition contract: it must match the bundle pin
and the working tree exactly. Every check here recomputes from source;
nothing trusts a stored digest without re-hashing.
"""

import hashlib
import json
import os
import re
import subprocess

MODULE_RE = re.compile(r"^module\s+([\w.]+);", re.M)
PROFILE_RE = re.compile(r"^mncs\s+([0-9.]+);", re.M)


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


def test_manifest_schema_and_counts(root, manifest):
    assert manifest["schema_version"] == "mncs.stdlib-manifest/1"
    assert manifest["repository"] == "mncs-stdlib"
    assert manifest["module_count"] == len(manifest["modules"])
    assert manifest["module_count"] >= 50
    assert manifest["bundle_path"] == "dist/stdlib-bundle.json"
    assert manifest["library_path"] == "library"


def test_bundle_pin_verifies(root, bundle):
    assert bundle["schema_version"] == "mncs.stdlib-bundle/1"
    names = [m["name"] for m in bundle["modules"]]
    assert len(set(names)) == len(names), "duplicate bundled modules"
    for module in bundle["modules"]:
        actual = hashlib.sha256(module["text"].encode("utf-8")).hexdigest()
        assert actual == module["content_sha256"], module["name"]
    assert bundle_identity_for(bundle["modules"]) == bundle["bundle_identity"]


def test_manifest_matches_bundle(manifest, bundle):
    assert manifest["bundle_identity"] == bundle["bundle_identity"]
    manifest_names = sorted(m["name"] for m in manifest["modules"])
    bundle_names = sorted(m["name"] for m in bundle["modules"])
    assert manifest_names == bundle_names
    bundle_digests = {m["name"]: m["content_sha256"] for m in bundle["modules"]}
    for module in manifest["modules"]:
        assert module["content_sha256"] == bundle_digests[module["name"]]


def test_manifest_matches_tree(root, manifest):
    for module in manifest["modules"]:
        path = os.path.join(root, "library", module["path"])
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        actual = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert actual == module["content_sha256"], module["name"]
        assert MODULE_RE.search(text).group(1) == module["name"]
        assert PROFILE_RE.search(text).group(1) == module["profile"]


def test_requires_profile_is_exact(root, manifest):
    profiles = sorted(
        {m["profile"] for m in manifest["modules"]}, key=profile_key
    )
    assert manifest["requires_profile"] == {
        "min": profiles[0],
        "max": profiles[-1],
    }


def test_module_imports_resolve_within_bundle(manifest):
    names = {m["name"] for m in manifest["modules"]}
    for module in manifest["modules"]:
        for imported in module.get("imports", []):
            assert imported in names, f"{module['name']} imports {imported}"


def test_gen_manifest_check_passes(root):
    result = subprocess.run(
        ["python3", "tools/gen_manifest.py", "--root", root, "--check"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
