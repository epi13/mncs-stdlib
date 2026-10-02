# mncs-stdlib architecture

Status: **canonical** (Stage F executed 2026-10; see
`rfcs/0001-stdlib-extraction.md`).

This repo is the independently owned, machine-native standard library
for MNCS. It is a *workload*, not an authority: it exercises the
language, pressures the compiler, and serves programs — it defines
neither meaning nor execution.

## 1. Namespaces

```text
mncs.core.*        smallest portable deterministic foundation.
                  Total, effect-free, no ambient authority. Every other
                  namespace may depend on core; core depends only on
                  core, acyclic (e.g. vision builds on image/geometry).
mncs.std.*        richer portable facilities written in MNCS over core.
                  No host I/O, no ambient authority; may depend on core
                  and on other std modules (acyclic).
mncs.family.*     family-governance vocabulary (RFC gates, journal
                  admission, coherence verdicts). HOSTED TRANSIENTLY:
                  shares the module/test machinery but is not portable
                  library surface; long-term owner undecided (pressure
                  STDLIB-P-001). Imports core only.
mncs.jit.*        JIT execution vocabulary per mncs-language RFC 0048.
                  HOSTED TRANSIENTLY: may migrate toward
                  mncs-compiler/runtime ownership (pressure STDLIB-P-002).
                  Imports core and jit-internal only.
(capability/)     RESERVED for capability/effect-shape declarations.
                  Empty until the language features exist; no placeholder
                  syntax is invented to fill it.
```

Layering rule (enforced by `tests/test_modules.py`): `core` imports
nothing; `std` imports `core`/`std`; `family`/`jit` import `core`
(+ `jit` internal). No cycles. One module per file; the declared
module name determines the bundle identity, never the path.

## 2. Module contract shape

Every module is a triple, all three checked in:

1. **Source** (`library/<ns>/<name>.mncs`): declares `mncs <profile>;`
   and `module <name>;`. Total and effect-free unless a capability
   design exists and is declared.
2. **Executable contract** (`examples/execution/<subject>-corpus.json`):
   bounded input/output cases pinning behavior, executed across
   backends by conformance harnesses.
3. **Generator** (`scripts/gen-*.py`): pure-Python, deterministic,
   self-contained (no toolchain, no sibling-repo reads). Committed
   outputs must match generator output byte-for-byte; enforced by
   `tests/test_regen.py` (this guarantee did not exist pre-extraction).

Consumer witnesses (`examples/source/*.mncs`) show real imports; the
three canonical witnesses are `library-consumer.mncs`,
`profile09-stdlib-namespace-consumer.mncs`, and
`status-generic-consumer.mncs`.

## 3. Distribution: the bundle pin

`dist/stdlib-bundle.json` (schema `mncs.stdlib-bundle/1`, format owned
by the reference compiler) is the content-addressed pin: per-module
`sha256` plus a `bundle_identity` over sorted `(name, digest)` pairs.
Regenerate with `./tools/regen.sh` (uses the `mncs` binary):

- development resolution: `library/` working tree via
  `MNCS_LIBRARY_PATH` / `MNCS_STDLIB_ROOT`;
- distribution resolution: the pin via `MNCS_STDLIB_BUNDLE` or the
  in-process `pinned_bundle()` — no path at all;
- divergence between pin and tree fails closed (`MNE234`); the pin
  never silently shadows a tree.

## 4. Compatibility: profiles + manifest

`stdlib-manifest.json` (schema `mncs.stdlib-manifest/1`, owned here)
is the machine-readable composition contract: bundle identity,
`requires_profile: {min, max}` aggregated over modules, and the full
module table with digests. Tooling answers *"can these components
compose?"* by comparing `requires_profile.max` against the toolchain's
supported profiles (see `docs/compatibility.md`). No SemVer: profiles
are the capability mechanism, content identities the versioning.

## 5. Authority boundaries (what lives where)

| Concern | Owner | This repo's relation |
|---|---|---|
| syntax, semantics, profiles, module rules | mncs-language | consumer; pressure source |
| reference compiler, backends, intrinsics, bundle format | mncs-language/crates | consumer; workload |
| successor compiler | mncs-compiler | fellow consumer |
| execution, VM artifact, admission | mncs-vm | backend envelope facts only |
| sessions, discovery, composition, persistence | mncs-environment | provider of contracts |
| diagnostics/repair policy | mncs-doctor | subject of checks |
| editor protocol, indexes | mncs-language-service | resolved, never copied |
| durable objects | mncs-store | future index substrate (schema reserved) |
| orchestration | mncs-forge | declared workflows |

## 6. Environment composition

The environment selects `mncs-stdlib` by repository name and binds:

- `mncs.stdlib-manifest/1` → `tools/stdlib_info.py` (index, module
  lookup, compatibility verdict — cheap, no toolchain);
- `mncs.stdlib-tests/*` → integrity suite via manifest test bindings;
- `adapter_library_paths: ["library"]` → session MNCS resolution.

Entry therefore yields `language → compiler → stdlib → lsp → doctor`
without manual configuration; Doctor validates the composition from
the manifest (see `docs/environment.md`).

## 7. Tooling contracts

- `MNCS_STDLIB_ROOT`: explicit stdlib checkout root (single path).
- `MNCS_LIBRARY_PATH`: `:`-separated resolution roots (existing;
  stdlib composes into it, never replaces it).
- `MNCS_STDLIB_BUNDLE`: explicit bundle pin file (existing).
- Toolchain default (no env): the `mncs-stdlib` sibling of the
  language checkout backing the `mncs` binary. Set
  `MNCS_STDLIB_ROOT` to empty to disable for hermetic tests.
- `MNCS_BIN`: explicit toolchain binary for this repo's tests.

## 8. Pressures hosted here vs routed elsewhere

`pressures/` records findings *discovered through* stdlib work with an
explicit owning layer. Language/compiler/runtime/tooling pressures are
filed in the owning repo (or Commons where that is the intake) and
linked from here — never dumped here. See `docs/pressures.md`.

## 9. Non-goals

- No package manager: no registry, fetch, or constraint solving.
- No frozen package syntax beyond what profiles earn.
- No host-service wrappers to look large; every operation earns its
  place (reusable semantics, abstraction boundary, or architectural
  pressure).
- No second implementation of language, compiler, runtime,
  environment, or editor semantics.
- No `mncs-language-part-2`: language contracts stay in
  `mncs-language`; this repo holds library implementation and
  library-owned contracts only.
