# Contributing

`mncs-stdlib` is the canonical MNCS standard library. Contributions
should make library behavior narrower to test and architectural
pressure more visible.

## Before opening a change

- Read `ARCHITECTURE.md`, `docs/adding-a-module.md`, and
  `docs/compatibility.md`.
- Query the index before adding anything:
  `python3 tools/stdlib_info.py list`.
- Check `pressures/registry.json` for the gap you are about to hit.

## Change categories

### New library facility

Requires: source module, executable contract (corpus + generator),
witness or test coverage, bundle + manifest regeneration, catalog
entry in `library/README.md`. Follow `docs/adding-a-module.md`.
Substantial new surface (new namespace, capability-bearing API,
semantic commitment) requires an RFC in `rfcs/`.

### Library behavior fix

The corpus pins the contract: a behavior change updates source,
generator, and committed outputs together, with a note explaining
which consumers were checked. If the old behavior was load-bearing
elsewhere, that is a compatibility finding — say so in the change.

### Contract-only change (corpus/generator)

Same atomicity: generator + outputs + a passing regen test. Never
hand-edit a generated file.

### Tooling / docs / pressure

Tooling changes must keep the integrity suite green without a
toolchain installed. Pressure records follow `docs/pressures.md`.

## Local checks

```bash
python3 -m pytest tests/ -k "not toolchain" -q   # no toolchain needed
python3 -m pytest tests/ -q                       # full suite (needs MNCS_BIN or sibling checkout)
./tools/regen.sh --check                          # artifacts current
```

## RFC naming

Use the next available four-digit number:

```text
rfcs/0002-short-descriptive-name.md
```

An RFC should contain: status, summary, motivation, terminology,
proposed library semantics, validation obligations, trust/security
consequences, alternatives, unresolved questions, compatibility and
migration notes.

## Pull requests

Keep pull requests centered on one module, one contract, or one
tooling milestone. Explain what is normative, what is experimental,
and what pressure remains open.
