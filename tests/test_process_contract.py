"""Process launch-vector capacity agreement (no toolchain).

The 256-entry bound is declared in two modules and enforced by the
language runtime and CLI. This test keeps the source declarations in
agreement; behavioral boundary proof lives in mncs-language's
process-lifecycle suites.
"""

import re

LAUNCH_VECTOR_CAPACITY = 256
STDIN_CAPACITY = 4096
STDIN_CHUNK_CAPACITY = 256

RECORDS = {
    "std/process.mncs": ("ProcessRequest", ("argv", "environment")),
    "std/application.mncs": ("ApplicationContext", ("argv", "environment")),
}


def _record_body(text, name):
    match = re.search(r"record\s+" + name + r"\s*\{(.*?)\n\}", text, re.S)
    assert match, f"record {name} not found"
    return match.group(1)


def test_launch_vector_capacities_agree(library_root):
    seen = {}
    for relpath, (record, fields) in RECORDS.items():
        with open(f"{library_root}/{relpath}", encoding="utf-8") as handle:
            body = _record_body(handle.read(), record)
        for field in fields:
            match = re.search(
                r"^\s*" + field + r":.*up_to\s+(\d+)\s*\]\s*,?\s*$", body, re.M
            )
            assert match, f"{relpath}: {record}.{field} has no bounded capacity"
            seen[f"{relpath}:{field}"] = int(match.group(1))
    assert set(seen.values()) == {LAUNCH_VECTOR_CAPACITY}, seen


def test_process_stdin_uses_the_profile_019_sequence_ceiling(library_root):
    with open(f"{library_root}/std/process.mncs", encoding="utf-8") as handle:
        source = handle.read()
    body = _record_body(source, "ProcessRequest")
    match = re.search(
        r"^\s*stdin:\s*\[byte;\s*up_to\s+(\d+)\]\s*,?\s*$",
        body,
        re.M,
    )
    assert match, "std/process.mncs: ProcessRequest.stdin has no bounded capacity"
    assert int(match.group(1)) == STDIN_CAPACITY
    assert source.startswith("mncs 0.19;"), "4096-byte views require Profile 0.19"


def test_process_stdin_chunks_cover_declared_forge_request_limit(library_root):
    with open(f"{library_root}/std/process.mncs", encoding="utf-8") as handle:
        source = handle.read()
    body = _record_body(source, "ProcessRequest")
    match = re.search(
        r"^\s*stdin_chunks:\s*\[\[byte;\s*up_to\s+(\d+)\s*\];"
        r"\s*up_to\s+(\d+)\s*\]\s*,?\s*$",
        body,
        re.M,
    )
    assert match, "std/process.mncs: ProcessRequest.stdin_chunks is not bounded"
    chunk_bytes, chunk_count = map(int, match.groups())
    assert chunk_bytes == STDIN_CAPACITY
    assert chunk_count == STDIN_CHUNK_CAPACITY
    assert re.search(r"^\s*stdin_chunk_count:\s*u64\s*,?\s*$", body, re.M)
    declared_capacity = STDIN_CAPACITY + chunk_bytes * chunk_count
    assert declared_capacity == 1_052_672
    assert declared_capacity >= 1_048_576, "typed stdin must admit Forge's 1 MiB request limit"
