# MNCS standard library — module catalog

This tree is the library itself: 61 MNCS modules, semantically
authoritative at the MNCS level. Consumers bind to these modules by
identity and bounded agreement, never by re-implementing the same
helpers ad hoc.

## Layout

```text
library/
  core/         foundational total operations (status lattice, boolean
                algebra, ordering/selection, bounded lineage, bounded
                sequences, byte/mask/vector/partition primitives,
                version envelopes, proof kernel vocabulary,
                image/vision observer pipeline)
  std/          portable abstractions over core: text/JSON, encoding,
                collections, algorithms, numerics, task/scope/channel,
                clock, hashing, terminal parsing, platform vocabulary,
                application/process effects
  family/       family-governance vocabulary, HOSTED TRANSIENTLY
                (see ARCHITECTURE.md; long-term owner undecided)
  jit/          JIT execution vocabulary per RFC 0048, HOSTED
                TRANSIENTLY (may migrate toward compiler/runtime)
  capability/   RESERVED, empty until its language features exist
```

Layering: `core` imports `core` only, acyclic; `std` imports `core`/`std`;
`family`/`jit` import `core` only (plus `jit` internal). Enforced by
`tests/test_modules.py`. One module per file.

## Modules

Profiles are the compatibility unit: each module declares the lowest
source profile it needs. Descriptions are the modules' own header
lines; the manifest (`stdlib-manifest.json`) is the machine-readable
form of this table.

| File | Module | Profile | Contents |
| --- | --- | --- | --- |
| `core/bounds.mncs` | `mncs.core.bounds.v1` | 0.5 | mncs.core.bounds — a second scalar bounds vocabulary used to pressure the Profile 0.9 namespace rules. Its clamp has the same name as the ordering |
| `core/bytes.mncs` | `mncs.core.bytes.v1` | 0.7 | mncs.core.bytes — byte-oriented primitives for fingerprints and encodings. |
| `core/contracts.mncs` | `mncs.core.contracts.v1` | 0.13 | mncs.core.contracts — executable semantic-contract vocabulary. |
| `core/geometry.mncs` | `mncs.core.geometry.v1` | 0.13 | mncs.core.geometry — typed spatial primitives for machine-native layout. |
| `core/identity.mncs` | `mncs.core.identity.v1` | 0.13 | mncs.core.identity — bounded opaque digest values. |
| `core/image.mncs` | `mncs.core.image.v1` | 0.13 | mncs.core.image — bounded grayscale images and deterministic pixel ops. |
| `core/lineage.mncs` | `mncs.core.lineage.v1` | 0.10 | mncs.core.lineage — total parent/child relations for bounded identities. |
| `core/logic.mncs` | `mncs.core.logic.v1` | 0.13 | mncs.core.logic — total boolean algebra helpers. |
| `core/mask.mncs` | `mncs.core.mask.v1` | 0.8 | mncs.core.mask — logical predicate composition over four bounded lanes. |
| `core/numeric.mncs` | `mncs.core.numeric.v1` | 0.8 | mncs.core.numeric — small integer-vector numeric kernels. |
| `core/ordering.mncs` | `mncs.core.ordering.v1` | 0.5 | mncs.core.ordering — comparison-based selection over signed integers. |
| `core/partition.mncs` | `mncs.core.partition.v1` | 0.8 | mncs.core.partition.v1 — bounded weighted integer partitioning. |
| `core/proof_admit.mncs` | `mncs.core.proof_admit.v1` | 0.13 | mncs.core.proof_admit.v1 — authoritative tranche-0.2 proof admission and binding (RFC 0007 hardening pass). |
| `core/proof_check.mncs` | `mncs.core.proof_check.v1` | 0.10 | mncs.core.proof_check.v1 — the MNCS-native RFC 0007 proof kernel (tranche 0.1). |
| `core/proof_dep.mncs` | `mncs.core.proof_dep.v2` | 0.10 | mncs.core.proof_dep.v2 — the MNCS-native RFC 0007 proof kernel, tranche 0.2. |
| `core/proof_term.mncs` | `mncs.core.proof_term.v1` | 0.10 | mncs.core.proof_term.v1 — canonical flat vocabulary for the RFC 0007 proof core. |
| `core/random.mncs` | `mncs.core.random.v1` | 0.6 | mncs.core.random — deterministic byte/integer random streams. |
| `core/result.mncs` | `mncs.core.result.v1` | 0.6 | mncs.core.result — the standard Result shape with a real reason payload. |
| `core/sequences.mncs` | `mncs.core.sequences.v1` | 0.13 | mncs.core.sequences — reusable operations over bounded sequences. |
| `core/status.mncs` | `mncs.core.status.v1` | 0.13 | mncs.core.status — authoritative MNCS status/evidence-dominance lattice. |
| `core/vector.mncs` | `mncs.core.vector.v1` | 0.8 | mncs.core.vector — small, portable integer-vector building blocks. |
| `core/version.mncs` | `mncs.core.version.v1` | 0.6 | mncs.core.version — canonical version identities and compatibility envelopes. |
| `core/vision.mncs` | `mncs.core.vision.v1` | 0.13 | mncs.core.vision — MNCS-native visual observer: pixels to scene graphs. |
| `std/ansi.mncs` | `mncs.std.ansi.v1` | 0.8 | mncs.std.ansi.v1 — bounded ANSI/VT semantic parsing. |
| `std/application.mncs` | `mncs.std.application.v1` | 0.16 | mncs.std.application — the reusable typed application-entry contract. |
| `std/channel.mncs` | `mncs.std.channel.v1` | 0.13 | mncs.std.channel — deterministic bounded-channel contracts. |
| `std/chunk.mncs` | `mncs.std.chunk.v1` | 0.13 | mncs.std.chunk — bounded chunk cursors with cross-chunk span identities. |
| `std/clock.mncs` | `mncs.std.clock.v1` | 0.10 | mncs.std.clock — relational wall-clock comparisons over u64 epoch milliseconds (HARNESS-PRESSURE-005). |
| `std/encoding.mncs` | `mncs.std.encoding.v1` | 0.13 | mncs.std.encoding — canonical big-endian byte encodings for scalar values. |
| `std/fixed.mncs` | `mncs.std.fixed.v1` | 0.6 | mncs.std.fixed — blessed milli-scale decimal scores. |
| `std/fnv1a.mncs` | `mncs.std.fnv1a.v1` | 0.13 | mncs.std.fnv1a — bounded, generic FNV-1a byte folding. |
| `std/json.mncs` | `mncs.std.json.v1` | 0.13 | mncs.std.json — bounded JSON recognition. |
| `std/json_cursor.mncs` | `mncs.std.json_cursor.v1` | 0.10 | mncs.std.json_cursor — bounded JSON token-boundary cursor. |
| `std/json_emit.mncs` | `mncs.std.json_emit.v1` | 0.13 | mncs.std.json_emit — bounded canonical JSON emission. |
| `std/json_projection.mncs` | `mncs.std.json_projection.v1` | 0.13 | mncs.std.json.projection — bounded raw key/value projections. |
| `std/json_stream.mncs` | `mncs.std.json_stream.v1` | 0.13 | mncs.std.json_stream — scalar structural JSON stream state. |
| `std/platform.mncs` | `mncs.std.platform.v1` | 0.6 | mncs.std.platform — portable finite-domain platform vocabulary. |
| `std/process.mncs` | `mncs.std.process.v1` | 0.18 | mncs.std.process — the reusable typed explicit-argv process effect. |
| `std/relation.mncs` | `mncs.std.relation.v1` | 0.13 | mncs.std.relation — bounded deterministic edge sets with transitive closure. |
| `std/scope.mncs` | `mncs.std.scope.v1` | 0.13 | mncs.std.scope — deterministic structured task-scope contracts. |
| `std/sha256.mncs` | `mncs.std.sha256.v1` | 0.14 | mncs.std.sha256 — SHA-256 as pure bounded MNCS (index PRESS-006). |
| `std/simd.mncs` | `mncs.std.simd.v1` | 0.8 | mncs.std.simd — compositional numerical kernels over semantic vectors. |
| `std/sort.mncs` | `mncs.std.sort.v1` | 0.13 | mncs.std.sort — deterministic bounded sort and deduplication. |
| `std/store.mncs` | `mncs.std.store.v1` | 0.13 | mncs.std.store — durable-state transition contracts (index PRESS-013/ 016/017/018, RFC 0026 substrate). |
| `std/task.mncs` | `mncs.std.task.v1` | 0.8 | mncs.std.task — bounded task/cancellation lifecycle seed. |
| `std/text_map.mncs` | `mncs.std.text_map.v1` | 0.13 | mncs.std.text_map.v1 — bounded text-to-code tables. |
| `std/text_scan.mncs` | `mncs.std.text_scan.v1` | 0.13 | mncs.std.text_scan — bounded literal text scanning over byte views. |
| `std/text_utf8.mncs` | `mncs.std.text_utf8.v1` | 0.13 | mncs.std.text_utf8 — bounded UTF-8 validation, scalar stepping, and a deliberately small case fold over byte views. |
| `std/text_view.mncs` | `mncs.std.text_view.v1` | 0.10 | mncs.std.text_view — bounded, host-neutral text references. |
| `std/token_set.mncs` | `mncs.std.token_set.v1` | 0.13 | mncs.std.token_set — deterministic bounded token-set algebra. |
| `family/coherence.mncs` | `mncs.family.coherence.v01` | 0.13 | mncs.family.coherence — the MNCS-native decision core of the family coherence system. |
| `family/journal.mncs` | `mncs.family.journal.v1` | 0.10 | mncs.family.journal.v1 — the MNCS-native decision core for canonical Journal progress events. |
| `family/rfc_status.mncs` | `mncs.family.rfc_status.v1` | 0.10 | mncs.family.rfc_status.v1 — the MNCS-native decision core for RFC status claims. |
| `jit/binding.mncs` | `mncs.jit.binding.v1` | 0.13 | mncs.jit.binding — logical bindings and generational publication for the MNCS-native JIT orchestration layer. |
| `jit/depends.mncs` | `mncs.jit.depends.v1` | 0.13 | mncs.jit.depends — dependency edges and invalidation for the MNCS-native JIT orchestration layer. |
| `jit/lifecycle.mncs` | `mncs.jit.lifecycle.v1` | 0.13 | mncs.jit.lifecycle — provider-neutral executable-artifact lifecycle. |
| `jit/plan.mncs` | `mncs.jit.plan.v1` | 0.13 | mncs.jit.plan — provider-neutral execution planning for the MNCS-native JIT orchestration layer. |
| `jit/profile.mncs` | `mncs.jit.profile.v1` | 0.13 | mncs.jit.profile — execution observations and tiering hooks for the MNCS-native JIT orchestration layer. |
| `jit/proof.mncs` | `mncs.jit.proof.v1` | 0.13 | mncs.jit.proof — proof-aware execution metadata for the MNCS-native JIT orchestration layer. |
| `jit/session.mncs` | `mncs.jit.session.v1` | 0.13 | mncs.jit.session — persistent JIT session state for the MNCS-native JIT orchestration layer. |
| `jit/types.mncs` | `mncs.jit.types.v1` | 0.13 | mncs.jit.types — shared vocabulary for the MNCS-native JIT/execution orchestration layer. |

## Namespace pressure (by design)

`core/ordering.mncs` and `core/bounds.mncs` intentionally export
overlapping `clamp_i64` names. `examples/source/profile09-stdlib-namespace-consumer.mncs`
imports both with aliases, proving the consumer retains two
declaring-module identities without relying on import discovery order.

## Key substrates

- **Bounded data**: `core/sequences.v1` + `core/bytes.v1` are the
  standard vocabulary (folds, membership, counting, option-shaped
  access, byte primitives, folding fingerprint); `std/encoding.v1`
  adds canonical big-endian encodings with executable round-trip laws.
- **Text**: borrowed spans (`std/text_view.v1`), never hidden
  allocation; bounded scanning (`std/text_scan.v1`), UTF-8 validation
  (`std/text_utf8.v1`), tables (`std/text_map.v1`).
- **JSON**: bounded scanner (`std/json.v1`), structural stream
  (`std/json_stream.v1`), raw projections (`std/json_projection.v1`),
  typed cursor (`std/json_cursor.v1`), canonical emission
  (`std/json_emit.v1`). No DOM; unknown keys outside the fixed matcher
  window stay structurally valid.
- **Branchless vectors/masks**: `core/vector.v1` + `core/mask.v1`
  (no physical SIMD width named); `std/simd.v1` adds an
  affine/ReLU/reduction kernel with visible intent.
- **Concurrency vocabulary**: `std/task.v1` (lifecycle seed),
  `std/scope.v1` (accounting), `std/channel.v1` (protocol). No
  threads, no preemption — deterministic contracts only.
- **Proof**: `core/proof_term.v1` + `core/proof_check.v1` (tranche-0.1
  kernel) + `core/proof_admit.v1` + `core/proof_dep.v2` (tranche-0.2
  admission). Dependent application/motives and open terms stay
  `UNKNOWN`, never `PASS`.
- **Effects with explicit authority**: `std/clock.v1` (relational
  comparisons under `--grant-time`), `std/process.v1` (explicit-argv
  process effect), `std/application.v1` (typed entry context).
  Importing never grants authority.

## Contracts and honesty properties

- Every operation is total and effect-free unless a capability design
  exists and is declared.
- The status lattice only weakens claims: nothing maps `UNKNOWN` to
  `PASS` or deletes `FAIL`. The negative fixture
  `examples/source/library-core-status-wrong.mncs` proves the corpus
  discriminates an UNKNOWN-laundering mutant on exactly that cell.
- `ordering` deliberately avoids contract clauses: current profiles
  cannot discharge contract-evidence obligations from source.
  Preconditions are documented in comments instead.
- `partition.v1` owns weighted allocation arithmetic; consumers
  (e.g. `mncs-tui`) do not copy its quotient/remainder logic.
- `ansi.v1` owns terminal sequence meaning but not terminal I/O;
  applications map its generic events at their own boundary.

## Backend envelope

Backend agreement is observed per corpus execution, not promised per
module. Corpora under `examples/execution/` execute on reference,
research-bytecode, portable-WASM, C11, LLVM, and Cranelift paths via
the language conformance harnesses; envelope facts
(`SUPPORTED`/`UNSUPPORTED`/`UNKNOWN`) are recorded per execution, and
exact-cost obligations remain `UNKNOWN` where the profiles cannot
discharge them. See `docs/compatibility.md`.

## Consumer binding

Consumers bind through elaboration-time linking with a host resolver:
filesystem roots (`MNCS_LIBRARY_PATH`, `MNCS_STDLIB_ROOT`, or the
toolchain default) for development, the bundle pin
(`dist/stdlib-bundle.json`) for distribution. The minimal witness is
`examples/source/library-consumer.mncs`. See `docs/bundle.md`.
