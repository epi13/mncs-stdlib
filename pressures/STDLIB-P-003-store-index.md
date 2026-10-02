# STDLIB-P-003: Store-backed stdlib index publication

- Date: 2026-10-02, status: **open**
- Owning layer: mncs-stdlib (publisher) + mncs-store (substrate)
- Upstream: design reserved in `docs/store-integration.md`

Stdlib semantic indexes should persist as Store objects under
`mncs.stdlib.index/1` so consumers share one verified index instead
of reparsing. Deferred: current consumers resolve correctly via
filesystem/bundle, and no consumer has demonstrated reparse cost
worth caching. Activation criteria are documented; the bundle
identity is the future cache key.
