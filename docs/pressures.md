# Implementation pressure

Stdlib is a proving ground for pure MNCS development — and therefore
a pressure source for the whole stack. Pressure is output, not noise.

## Rule

When MNCS cannot express something cleanly, the compiler lacks
support, a backend cannot realize valid semantics, or tooling is
missing: **record it, route it, then implement the best clean MNCS
available.** Never hide the gap behind host code. A host-side shim
behind an explicit contract documenting the missing capability is a
last resort, and it still gets a pressure record.

## Records

One file per finding under `pressures/`, named
`STDLIB-P-<nnn>-<slug>.md`, indexed in `pressures/registry.json`:

- title, date, status (`open` / `routed` / `resolved`);
- owning layer + owning repository (language, compiler, vm/runtime,
  environment, language-service, doctor, store, forge, test, other);
- minimal reproducer (MNCS source, corpus case, or command);
- what was implemented instead and what it costs;
- upstream link once filed (issue, pressure file, or Commons record).

## Routing

File the finding in the repository that owns the problem, following
that repo's intake (e.g. `mncs-compiler/pressure/`,
`mncs-language-service/pressure/`, Commons pressures). This repo keeps
the discovery record and the link — it never becomes the dumping
ground for other layers' issues, and other layers' records never get
fixed by edits here.

## Intake checklist (for the filer)

- [ ] Reproduces from this repo alone (plus toolchain where noted).
- [ ] Owning layer named honestly; no guessing at root cause as fact.
- [ ] Workaround cost stated (what stdlib pays while it is open).
- [ ] Upstream record exists or is explicitly deferred with a reason.
