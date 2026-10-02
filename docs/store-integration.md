# Store integration (reserved design)

Status: **designed, not yet implemented** (pressure STDLIB-P-003).

## Intent

Stdlib semantic indexes should persist as Store objects under a
stdlib-owned domain schema, with all query structures as disposable
projections — so language service, environment, and agents share one
verified index instead of reparsing 61 modules per consumer.

## Reserved schema

- Domain schema: `mncs.stdlib.index/1` (index documents keyed by
  bundle identity + module name).
- Publication: content-addressed put with `expected_generation` CAS,
  relations to the bundle identity, provenance naming generator +
  source commit.
- Query: domain-prefix find for module entries; `commit-feed/1` for
  incremental rebuild on new pins.
- Index structures themselves stay disposable derivatives owned by
  the projecting consumer (mncs-index owns discovery; Store owns
  durability).

## Why not yet

The current consumers resolve correctly through filesystem roots and
the bundle pin; Store publication adds a persistence dependency to
the stdlib integrity path before any consumer needs incremental
index reuse. The environment's projection store already persists
projections via Store, so the projected index summary rides that
path today.

## Activation criteria

Implement when a consumer (language-service resident index or
environment projection) demonstrates repeated full reparse cost
worth caching, or when cross-session index sharing is required.
The manifest's bundle identity is the cache key; stale pins are
impossible by construction (identity mismatch fails closed).
