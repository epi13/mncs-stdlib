"""Corpus regeneration determinism (no toolchain).

Every committed corpus produced by a generator must match the generator
output byte-for-byte. Generators run against a snapshot: on mismatch the
tree is restored and the test reports which files drifted.
"""

import hashlib
import os
import shutil
import subprocess
import tempfile

# Generators that write into examples/execution/ on their own.
OUT_GENERATORS = [
    "scripts/gen-library-core-corpora.py",
    "scripts/gen-family-coherence-corpora.py",
    "scripts/gen_collection_corpora.py",
    "scripts/gen_scope_channel_corpora.py",
    "scripts/gen_clock_corpus.py",
    "scripts/gen_json_emit_corpus.py",
    "scripts/gen_platform_capability_corpus.py",
    "scripts/gen_sha256_corpus.py",
    "scripts/gen_store_corpus.py",
    "scripts/gen_task_corpus.py",
    "scripts/gen_text_scan_corpus.py",
    "scripts/gen_subtype_windows_corpus.py",
]

# Generators that write to explicit argv paths: (script, outputs...).
ARGV_GENERATORS = [
    ("scripts/gen_rfc_status_corpus.py", ["examples/execution/rfc-status-corpus.json"]),
    ("scripts/gen_journal_corpus.py", ["examples/execution/journal-corpus.json"]),
    ("scripts/gen_proof_corpus.py", ["examples/execution/proof-kernel-corpus.json"]),
    (
        "scripts/gen_proof_dep_corpus.py",
        [
            "examples/execution/proof-dep-corpus.json",
            "examples/execution/proof-dep-admission-corpus.json",
        ],
    ),
    ("scripts/gen_proof_fuzz.py", ["examples/execution/proof-kernel-fuzz-corpus.json"]),
]


def snapshot(directory):
    hashes = {}
    for name in sorted(os.listdir(directory)):
        path = os.path.join(directory, name)
        if os.path.isfile(path):
            with open(path, "rb") as handle:
                hashes[name] = hashlib.sha256(handle.read()).hexdigest()
    return hashes


def test_all_generators_reproduce_committed_bytes(root):
    execution = os.path.join(root, "examples", "execution")
    before = snapshot(execution)
    # Protect the tree: run generators, then compare; restore on failure.
    with tempfile.TemporaryDirectory() as staging:
        backup = os.path.join(staging, "execution")
        shutil.copytree(execution, backup)
        try:
            for script in OUT_GENERATORS:
                result = subprocess.run(
                    ["python3", script],
                    cwd=root,
                    capture_output=True,
                    text=True,
                )
                assert result.returncode == 0, f"{script}: {result.stderr}"
            for script, outputs in ARGV_GENERATORS:
                result = subprocess.run(
                    ["python3", script, *[os.path.join(root, o) for o in outputs]],
                    cwd=root,
                    capture_output=True,
                    text=True,
                )
                assert result.returncode == 0, f"{script}: {result.stderr}"
            after = snapshot(execution)
        finally:
            # Always restore byte-identical committed state.
            for name in os.listdir(execution):
                os.remove(os.path.join(execution, name))
            for name in os.listdir(backup):
                shutil.copy2(os.path.join(backup, name), execution)
    drifted = sorted(
        name
        for name in set(before) | set(after)
        if before.get(name) != after.get(name)
    )
    assert not drifted, f"generators drift from committed corpora: {drifted}"
