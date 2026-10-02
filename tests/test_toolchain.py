"""Toolchain slice: compile every module, resolve real consumers.

Needs an mncs binary (MNCS_BIN or a sibling mncs-language checkout).
Skipped with a clear message when no toolchain is present.
"""

import json
import os
import subprocess

import pytest

pytestmark = pytest.mark.toolchain


def run_mncs(mncs_bin, args, library_root, extra_env=None):
    env = dict(os.environ)
    env["MNCS_LIBRARY_PATH"] = library_root
    env.pop("MNCS_STDLIB_BUNDLE", None)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [mncs_bin, *args],
        capture_output=True,
        text=True,
        env=env,
    )


def test_every_module_validates(root, library_root, mncs_bin, manifest):
    failures = []
    for module in manifest["modules"]:
        path = os.path.join(library_root, module["path"])
        result = run_mncs(mncs_bin, ["validate", path], library_root)
        if result.returncode != 0:
            failures.append(f"{module['name']}: {result.stdout[:300]}")
            continue
        try:
            report = json.loads(result.stdout)
        except ValueError:
            failures.append(f"{module['name']}: non-JSON validate output")
            continue
        if not report.get("valid"):
            failures.append(f"{module['name']}: {report.get('errors')}")
    assert not failures, "\n".join(failures)


def test_canonical_consumer_validates(root, library_root, mncs_bin):
    consumer = os.path.join(root, "examples", "source", "library-consumer.mncs")
    result = run_mncs(mncs_bin, ["validate", consumer], library_root)
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["valid"]


def test_namespace_consumer_validates(root, library_root, mncs_bin):
    consumer = os.path.join(
        root, "examples", "source", "profile09-stdlib-namespace-consumer.mncs"
    )
    result = run_mncs(mncs_bin, ["validate", consumer], library_root)
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["valid"]


def test_generic_consumer_validates(root, library_root, mncs_bin):
    consumer = os.path.join(root, "examples", "source", "status-generic-consumer.mncs")
    result = run_mncs(mncs_bin, ["validate", consumer], library_root)
    assert result.returncode == 0, result.stdout
    assert json.loads(result.stdout)["valid"]


def test_missing_library_fails_closed(root, mncs_bin):
    consumer = os.path.join(root, "examples", "source", "library-consumer.mncs")
    env = dict(os.environ)
    env.pop("MNCS_LIBRARY_PATH", None)
    env.pop("MNCS_STDLIB_BUNDLE", None)
    env["MNCS_STDLIB_ROOT"] = ""
    result = subprocess.run(
        [mncs_bin, "validate", consumer],
        capture_output=True,
        text=True,
        env=env,
    )
    combined = result.stdout + result.stderr
    assert result.returncode != 0, "import must fail without any library root"
    assert "MNE173" in combined, combined[:500]


def test_bundle_verify_roundtrip(root, mncs_bin):
    bundle = os.path.join(root, "dist", "stdlib-bundle.json")
    result = subprocess.run(
        [mncs_bin, "bundle", "verify", bundle],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_bundle_only_resolution(root, mncs_bin):
    # No filesystem root at all: the pin alone must satisfy the import.
    consumer = os.path.join(root, "examples", "source", "library-consumer.mncs")
    env = dict(os.environ)
    env.pop("MNCS_LIBRARY_PATH", None)
    env["MNCS_STDLIB_ROOT"] = ""
    env["MNCS_STDLIB_BUNDLE"] = os.path.join(root, "dist", "stdlib-bundle.json")
    result = subprocess.run(
        [mncs_bin, "validate", consumer],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["valid"]
