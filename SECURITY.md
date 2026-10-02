# Security Policy

`mncs-stdlib` is experimental research software and must not currently
be relied upon to establish the security or correctness of production
systems.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting feature when available.
Do not publish an exploitable issue before maintainers have had a
reasonable opportunity to assess it.

A useful report includes:

- affected commit or bundle identity;
- module and function involved;
- minimal reproducer (MNCS source plus corpus case where possible);
- expected and observed result;
- whether the issue permits an undeclared effect, capability
  escalation, false evidence, unsound optimization, or verifier bypass;
- known mitigations.

## Research security priorities

The project treats the following as security-sensitive:

- a total operation that is not total (panic, trap, or hang on a
  claimed input);
- `UNKNOWN` laundered into `PASS`, or `FAIL` deleted;
- evidence attached to the wrong property or implementation;
- stale bundle/manifest accepted after an invalidating change;
- digest mismatch not failing closed;
- capability-bearing behavior without a declared capability design;
- host authority reached implicitly from portable `core`/`std`.

## Current limitations

Library meaning is pinned by executable contracts, not by proof.
Consumption across repository boundaries is by content identity and
declared profiles; compromise of the toolchain binary is outside this
repo's verification boundary (see the toolchain's own policy).
