"""Executable oracle tests for the bounded standard SHA-256 digest."""

import hashlib
import json
import os
import subprocess

import pytest

pytestmark = pytest.mark.toolchain


BACKENDS = (
    "mncs-research-bytecode",
    "mncs-portable-wasm-mvp",
    "mncs-c11",
    "mncs-llvm-ir",
    "mncs-cranelift",
)
LENGTHS = (0, 1, 55, 56, 63, 64, 65, 127, 128, 129, 1024)


def byte_sequence(data):
    return {
        "sequence": {
            "values": [{"byte": {"value": value}} for value in data]
        }
    }


def test_standard_digest_matches_independent_oracle_on_executable_backends(
    root, library_root, mncs_bin, tmp_path
):
    cases = []
    for length in LENGTHS:
        data = bytes((index * 37 + 11) % 256 for index in range(length))
        cases.append({
            "id": f"sha256-digest-{length}",
            "request": {
                "schema_version": "0.1",
                "target": {
                    "module": "mncs.std.sha256.v1",
                    "function": "digest_standard",
                },
                "arguments": [byte_sequence(data)],
                "step_budget": 8_000_000,
            },
            "expected": [byte_sequence(hashlib.sha256(data).digest())],
        })

    corpus = tmp_path / "sha256-digest-corpus.json"
    corpus.write_text(json.dumps({
        "schema_version": "0.1",
        "name": "stdlib-sha256-bounded-digest",
        "cases": cases,
    }))
    source = os.path.join(library_root, "std", "sha256.mncs")

    for backend in BACKENDS:
        output_dir = tmp_path / backend
        environment = dict(os.environ)
        environment["MNCS_LIBRARY_PATH"] = library_root
        environment.pop("MNCS_STDLIB_BUNDLE", None)
        result = subprocess.run(
            [
                mncs_bin,
                "experiment",
                "run",
                source,
                "--backend",
                backend,
                "--corpus",
                str(corpus),
                "--output-dir",
                str(output_dir),
            ],
            capture_output=True,
            text=True,
            env=environment,
        )
        assert result.returncode == 0, f"{backend}: {result.stderr}"
        report = json.loads((output_dir / "result.json").read_text())
        observations = report["cases"]
        assert len(observations) == len(LENGTHS), f"{backend}: corpus drift"
        assert all(
            item["status"] == "returned" and item["expectation_met"] is True
            for item in observations
        ), f"{backend}: {observations}"
        if backend == "mncs-research-bytecode":
            assert max(item["steps"] for item in observations) <= 500_000


def test_streaming_consumer_matches_independent_oracle_across_chunk_boundaries(
    root, library_root, mncs_bin, tmp_path
):
    lengths = (0, 55, 64, 1024, 1025, 2048, 3073, 4096)
    cases = []
    for length in lengths:
        data = bytes((index * 53 + 19) % 256 for index in range(length))
        chunk_sizes = (1024, 1024, 1024, 1024) if length > 3073 else (333, 1024, 1024, 1024)
        chunks = []
        offset = 0
        for chunk_size in chunk_sizes:
            chunks.append(data[offset:offset + chunk_size])
            offset += chunk_size
        assert offset >= length
        cases.append({
            "id": f"sha256-stream-{length}",
            "request": {
                "schema_version": "0.1",
                "target": {
                    "module": "examples.sha256.stream_consumer",
                    "function": "digest_four_chunks",
                },
                "arguments": [byte_sequence(chunk) for chunk in chunks],
                "step_budget": 4_000_000,
            },
            "expected": [byte_sequence(hashlib.sha256(data).digest())],
        })

    corpus = tmp_path / "sha256-stream-corpus.json"
    corpus.write_text(json.dumps({
        "schema_version": "0.1",
        "name": "stdlib-sha256-streaming-consumer",
        "cases": cases,
    }))
    source = os.path.join(root, "examples", "source", "sha256-stream-consumer.mncs")
    environment = dict(os.environ)
    environment["MNCS_LIBRARY_PATH"] = library_root
    environment.pop("MNCS_STDLIB_BUNDLE", None)
    result = subprocess.run(
        [
            mncs_bin,
            "experiment",
            "run",
            source,
            "--backend",
            "mncs-research-bytecode",
            "--corpus",
            str(corpus),
            "--output-dir",
            str(tmp_path / "stream"),
        ],
        capture_output=True,
        text=True,
        env=environment,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "stream" / "result.json").read_text())
    observations = report["cases"]
    assert len(observations) == len(lengths), "streaming corpus drift"
    assert all(
        item["status"] == "returned" and item["expectation_met"] is True
        for item in observations
    ), observations
    assert max(item["steps"] for item in observations) <= 2_000_000
