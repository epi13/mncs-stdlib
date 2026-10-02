"""Compatibility composition checks.

Pure-manifest checks always run. The toolchain-floor comparison needs
the sibling language checkout's capability index and skips clearly
when it is absent.
"""

import json
import os
import subprocess

import pytest


def test_requires_profile_within_toolchain_floor_via_info_tool(root, manifest):
    # The info tool is the machine-readable composition oracle.
    info = os.path.join(root, "tools", "stdlib_info.py")
    result = subprocess.run(
        ["python3", info, "--root", root, "compatible", "--max-profile", "0.18"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout
    result = subprocess.run(
        ["python3", info, "--root", root, "compatible", "--max-profile", "0.5"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 3, "profile 0.5 toolchain must not satisfy 0.18 stdlib"


def test_requires_profile_within_language_capabilities(root, manifest):
    capabilities_path = os.path.join(
        root, "..", "mncs-language", "docs", "language-capabilities.json"
    )
    if not os.path.isfile(capabilities_path):
        pytest.skip("sibling mncs-language checkout absent; floor check deferred")
    with open(capabilities_path, encoding="utf-8") as handle:
        capabilities = json.load(handle)
    current = capabilities.get("current_profile")
    profiles = [
        entry.get("version")
        for entry in capabilities.get("profiles", [])
        if isinstance(entry, dict) and entry.get("version")
    ]
    if current:
        profiles.append(current)
    assert profiles, "language capability index names no profiles"

    def key(profile):
        return tuple(int(part) for part in str(profile).split("."))

    floor = sorted((str(p) for p in profiles), key=key)[-1]
    required = manifest["requires_profile"]["max"]
    assert key(required) <= key(floor), f"stdlib needs {required}, language offers {floor}"
