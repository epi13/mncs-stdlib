# Migration record: mncs-language → mncs-stdlib (Stage F)

Executed 2026-10-02. Source: `mncs-language` main at `425de20`
(bundle pin generated from `f306bc0`-era tree; see below for pin
lineage). This document is the complete move list and the repair log.

## Ownership rule applied

Move iff library implementation or a library-owned contract:

- `library/{core,std}/**` — portable library implementation;
- `library/{family,jit}/**` — hosted transiently (shares the module
  closure and test machinery; pressures STDLIB-P-001/-002 track the
  long-term owner question);
- corpora pinning module behavior + their generators (outputs live
  with their generator; harnesses read across repos);
- fixtures importing `mncs.*` + fixtures pairing with moved corpora;
- the bundle pin (generation moves here; the format stays compiler).

Stayed in `mncs-language`: syntax, semantics, profiles, module rules,
reference compiler + backends, bundle format, language-direction docs
(amended), conformance harnesses, language-feature fixtures/corpora,
host-effect/capability boundary tests, family provider metadata.

## Moved (61 modules)

`library/core/` (23), `library/std/` (27), `library/family/` (3),
`library/jit/` (8), `library/capability/` reservation (documented;
was an empty dir). `library/README.md` rewritten as this repo's
`library/README.md` with a regenerated-accurate catalog (the old
table had stale profiles, e.g. `clock` 0.8 → actual 0.10).

## Moved (86 corpora + 17 generators + 29 fixtures)

- 86 files under `examples/execution/` (see `docs/MIGRATION-corpora.md`
  for the per-file list with owning test);
- 17 generator scripts under `scripts/` (pure-Python, repo-relative,
  zero-edit moves except repairs below);
- 28 fixtures under `examples/source/` + `examples/consumers/`.

## Repairs during migration (generator/corpus drift)

The language tree claimed "committed generated files must match the
generator output" but no test enforced it. Repair log:

1. `gen-library-core-corpora.py` emitted a dead
   `library-core-ravel-differential-corpus.json` (superseded by the
   linked witness; nothing consumed it) — emit + dead function removed.
2. Same generator emitted `step_budget=1024` for the four `wide-*`
   text-map cases; committed truth was `8192` (newer) — generator
   updated to 8192.
3. `gen_text_scan_corpus.py` was missing 11 committed `equals-*` /
   `folded-*` cases — emission reconstructed from committed bytes
   (verified case-identical; only a trailing newline differed).
4. `gen_sha256_corpus.py` read `examples/fs-fixture/sub/b.txt` from
   the language tree — replaced with a synthetic deterministic
   156-byte blob so generation is self-contained; corpus regenerated
   (digests differ by construction; chunking-independence meaning kept).
5. `semantic-arithmetic-corpus.json` deliberately NOT moved (pins
   language arithmetic, not stdlib).

All 17 generators now reproduce committed bytes exactly, enforced by
`tests/test_regen.py`.

## What language kept as a dependency (lockfile, not a copy)

`mncs-language` vendors the pin at `stdlib-pin/stdlib-bundle.json`:
a content-addressed lockfile, identity-checked at build and test
time, updated by copying this repo's `dist/stdlib-bundle.json`.
Language tests resolve stdlib sources via `MNCS_STDLIB_ROOT`, else
the `mncs-stdlib` sibling checkout, else fail closed with a clear
message; the `mncs` binary additionally defaults to the sibling for
ordinary development use.
