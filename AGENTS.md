# MNCS agent execution contract (stdlib repository)

Any capable agent entering this repository works under this contract:
MNCS first, pressure routed upstream, evidence honest. This is the
stdlib-side mirror of the language contract (`mncs-language/AGENTS.md`).

## 1. MNCS is the implementation language

New library code is written in MNCS source (`.mncs`) under `library/`.
Do not escape to a host language merely because MNCS lacks a
capability; that lack is a pressure event (section 4). Host code in
`scripts/` and `tools/` is transport (generators, manifest tooling,
test harness), never library semantics: a Python function that
re-implements a library operation instead of testing it is a defect.

## 2. The triple is atomic

A library change ships source + executable contract + generator update
together, with `dist/stdlib-bundle.json` and `stdlib-manifest.json`
regenerated (`./tools/regen.sh`). A module edit without re-pinning
fails the freshness tests instead of drifting downstream. Never hand-edit
a generated file: fix the generator.

## 3. Respect the namespace layering

`core` imports `core` only, acyclic; `std` imports `core`/`std`;
`family`/`jit` import `core` only (plus `jit` internal). One module
per file. Declare
the lowest profile the module actually needs; a higher profile is a
compatibility cost paid by every consumer. `capability/` stays empty
until its language features exist.

## 4. Missing capability becomes pressure, never a workaround

When MNCS cannot express something cleanly, the compiler lacks support,
a backend cannot realize valid semantics, or tooling is missing: record
it under `pressures/` with an honest owning layer, file it upstream
where the owning repo requires, and link it. Then implement the best
clean MNCS available. A host-side shim that hides the gap is forbidden;
a shim behind an explicit contract documenting the missing capability
is a last resort, not a habit.

## 5. Totality and honesty

Library operations are total and effect-free unless a capability design
exists and is declared. Never map `UNKNOWN` to `PASS` or delete `FAIL`.
Preconditions the profiles cannot discharge go in comments, not in
undeclared contract clauses. Backend-envelope facts stay explicit
(`SUPPORTED`/`UNSUPPORTED`/`UNKNOWN`); never claim execution from
emission alone.

## 6. Discover before inventing

Before adding a helper, query the index (`python3 tools/stdlib_info.py
list`, `... show <module>`) and read the module catalog
(`library/README.md`). Coherent, reusable, machine-native abstractions
only; no one-off conveniences, no clones of another language's stdlib
hierarchy, no host-service wrappers.

## 7. Validate like the ecosystem watches

Run the integrity suite for every change (`python3 -m pytest tests/ -q`
with a toolchain for the full suite). Cross-backend disagreement is
pressure: classify it (ambiguous semantics, compiler bug, stdlib bug,
backend bug, unsupported capability, intentional difference) and make
intentional differences explicit. Severity order for triage:
correctness of meaning first, then contract coverage, then performance.
