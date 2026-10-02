# mncs-stdlib

The canonical MNCS standard library: normal reusable MNCS facilities,
written in MNCS itself, distributed as content-addressed modules, and
consumed by ordinary MNCS programs through the toolchain's module
resolution — no vendoring, no host-language fallbacks, no repository
layout knowledge required.

```text
mncs-language          syntax, semantics, profiles, module/package rules,
                       reference compiler, bundle format
      ↓
mncs-compiler          MNCS-native successor compiler (experimental)
      ↓
mncs-stdlib (this repo)  reusable MNCS facilities: core types, collections,
                         text, JSON, algorithms, encoding, numerics,
                         time/task/channel abstractions, proof/family/JIT
                         vocabularies in their documented namespaces
      ↓
MNCS programs
```

## Layout

```text
library/            the library itself: core/, std/, family/, jit/,
                    capability/ (reserved; see library/capability/README.md)
dist/               generated distribution artifacts (checked in):
                    dist/stdlib-bundle.json — the content-addressed pin
stdlib-manifest.json  generated compatibility manifest: bundle identity,
                    required source profiles, per-module digests
examples/           stdlib-owned fixtures, consumer witnesses, and
                    execution corpora (library contracts in executable form)
scripts/            deterministic corpus generators (pure Python, no toolchain)
tools/              manifest/info tooling (stdlib_info.py, gen_manifest.py)
tests/              integrity, freshness, compatibility, and toolchain tests
docs/               architecture, compatibility, contributor, integration docs
rfcs/               design records (RFC 0001 records the extraction itself)
pressures/          language/compiler/tooling pressure found via stdlib work
.mncs/project.json  family repository manifest (provider contracts)
family-semantic-contracts-v1.json  callable provider declarations
mncs-forge.toml     Forge workspace binding (declared workflows)
```

## What this repository owns

- Every `mncs.*` library module under `library/` and its executable
  contracts (corpora + generators under `examples/` and `scripts/`).
- The stdlib bundle pin (`dist/stdlib-bundle.json`) and the compatibility
  manifest (`stdlib-manifest.json`): what the library is, what profile it
  needs, and how to verify it byte-for-byte.
- Library-owned documentation: module catalog, compatibility rules, how to
  add a module, pressure-recording procedure.
- Provider contracts exposing the library to the MNCS environment
  (discovery, index queries, compatibility verdicts).

## What this repository explicitly does not own

- Language syntax, semantics, type rules, profiles, or module/package
  semantics — `mncs-language` (see `spec/`, `docs/source-profile-*.md`).
- Compilation, backends, the bundle *format*, or compiler intrinsics —
  the reference compiler in `mncs-language/crates/` and, when it
  succeeds, `mncs-compiler`.
- Runtime/execution semantics — `mncs-vm` and the backend envelopes.
- Environment composition, sessions, persistence — `mncs-environment`.
- Editor/IDE protocol behavior — `mncs-language-service` (consumes this
  repo through resolution, never by copy).
- Family governance meaning — the `mncs.family.*` modules are *hosted*
  here transiently (see below); their long-term owner is undecided and
  tracked as pressure. Likewise `mncs.jit.*` execution vocabulary may
  migrate toward `mncs-compiler`/runtime ownership once that boundary
  earns it.

## Relation to mncs-language

`mncs-language` defines what MNCS means; this repo is written in that
meaning. The toolchain resolves `mncs.*` imports from this repo's
`library/` (development) or from the bundle pin (distribution). Language
conformance harnesses execute this repo's corpora across backends; the
corpora live here because they pin *library* behavior. Language-owned
direction history stays in
`mncs-language/docs/core-standard-library.md` (amended at Stage F);
library-owned direction lives here (`ARCHITECTURE.md`, `rfcs/`).

## Relation to mncs-compiler

None structurally: the successor compiler consumes the stdlib like any
other MNCS program. Compiler-origin pressure discovered through stdlib
use is recorded here under `pressures/` and routed to the owning layer.

## Relation to mncs-vm

None structurally: the VM executes frozen artifacts and resolves no
imports. Stdlib modules must be expressible within profiles the VM's
admitted SSA subset can realize when the VM is the selected backend;
backend-envelope facts stay explicit (see `docs/compatibility.md`).

## Discovery by mncs-environment

The environment selects this repo by name (`mncs-stdlib`) in the
workspace scope and discovers provider contracts from
`family-semantic-contracts-v1.json` and `.mncs/project.json`:

- `mncs.stdlib-manifest/1` — callable index/compatibility queries
  (`tools/stdlib_info.py`).
- `mncs.stdlib-tests/*` — manifest test bindings (integrity suite).
- `adapter_library_paths: ["library"]` — this repo contributes its
  library root to MNCS resolution wherever the session invokes through
  the binding.

No guessed paths: consumers ask the manifest where the library root and
bundle are. See `docs/environment.md`.

## Build / test / validate

Prerequisites: Python 3 (integrity suite) and, for toolchain tests, an
`mncs` binary from `mncs-language` (`MNCS_BIN`, else the sibling
`../mncs-language/target/{release,debug}/mncs`).

```bash
# Integrity: manifest/bundle/module/regen checks (no toolchain needed)
python3 -m pytest tests/ -k "not toolchain" -q

# Full suite including toolchain compilation of every module
python3 -m pytest tests/ -q

# Regenerate distribution artifacts after a library edit
./tools/regen.sh          # dist/stdlib-bundle.json + stdlib-manifest.json
python3 tools/gen_manifest.py --check   # verify manifest matches bundle
```

`MNCS_STDLIB_ROOT` may point at this checkout explicitly; tooling also
accepts the repo by direct path. The toolchain discovers the stdlib root
as `MNCS_STDLIB_ROOT`, else the `mncs-stdlib` sibling of the language
checkout backing the `mncs` binary, else nothing (explicit
`MNCS_LIBRARY_PATH` roots always apply).

## Compatibility

Profiles are the compatibility mechanism — not SemVer. Each module
declares the source profile it needs (`mncs 0.x;`); the manifest
aggregates `requires_profile: {min, max}`; tooling compares that against
the toolchain's supported profiles:

```text
language contract (profiles + capability index)
      ↓
compiler supports profiles ≤ max
      ↓
stdlib requires profiles ≤ requires_profile.max
```

`tools/stdlib_info.py compatible --max-profile 0.18` answers the
composition question machine-readably. See `docs/compatibility.md`.

## Adding a library facility

See `docs/adding-a-module.md`. In short: one module per file, total and
effect-free unless a capability design exists, executable contract
(corpus + generator) from day one, profile honestly declared, bundle +
manifest regenerated, pressures recorded rather than worked around.

## Implementation pressure

Stdlib work that MNCS cannot yet express cleanly is recorded under
`pressures/` (one file per finding, registry in `pressures/registry.json`)
and routed to the owning repository. Never hide a language/compiler gap
behind host code here: isolate it, document the missing capability, file
the pressure. See `docs/pressures.md`.

## Migration provenance

This repository was extracted from `mncs-language` at Stage F
(see `rfcs/0001-stdlib-extraction.md` and `docs/MIGRATION.md`):
61 library modules, 86 execution corpora, 17 generators, 28 fixtures,
plus the bundle pin — with generator/corpus drift repaired and
determinism enforced by test for the first time.
