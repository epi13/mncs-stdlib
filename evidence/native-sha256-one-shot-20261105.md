# Native SHA-256 one-shot and streaming contract

## Delivered capability

`mncs.std.sha256.v1` now exports `digest_standard` for one bounded input of up
to 1024 bytes and `update_blocks_standard` for carrying a `DigestState` across
successive inputs of up to 1024 bytes. The one-shot function uses that same
stream update path. The consumer retains byte acquisition and chunk boundaries;
MNCS owns the SHA-256 compression, padding, and state transition.

The reusable interface remains at profile 0.14. It adds no host implementation
and requires no capability or effect. Each update has a fixed sixteen-block
work bound.

## Independent verification

- `tests/test_sha256_digest.py`: 11 lengths from empty input through 1024 bytes
  matched Python `hashlib.sha256` on Research Bytecode, Portable WASM MVP, C11,
  LLVM IR, and Cranelift.
- `examples/source/sha256-stream-consumer.mncs`: a separate MNCS consumer passed
  eight lengths through four consecutive state updates, including an uneven
  333-byte first chunk and empty trailing chunks. Python `hashlib.sha256` was
  the independent expected value.
- The largest Research Bytecode stream case was 4096 bytes at 1,306,940 steps;
  the test contract caps it at 2,000,000 steps. Empty, short, block-boundary,
  1 KiB, and multi-chunk inputs were included.
- Focused command: `MNCS_BIN=/home/epi13/Documents/Projects/mncs-language/target/release/mncs python3 -m pytest tests/test_sha256_digest.py -q` — 2 passed.

The Rust/Python oracle is test-only. Production consumers can keep their I/O
adapter and pass bounded chunks into the native stream state instead of
maintaining another digest implementation.
