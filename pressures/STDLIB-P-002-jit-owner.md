# STDLIB-P-002: Long-term owner for `mncs.jit.*` modules

- Date: 2026-10-02, status: **open**
- Owning layer: undecided (successor compiler? runtime?)
- Upstream: not yet filed (decision needed before filing)

`mncs.jit.*` (types/session/binding/depends/lifecycle/plan/profile/
proof) is JIT execution vocabulary per `mncs-language` RFC 0048. It
is execution-architecture surface more than portable library surface,
but it shares the module closure and is consumed through the same
resolution, so the extraction hosts it transiently under
`library/jit/`.

Resolution: when the compiler/runtime boundary earns it, move the
vocabulary toward `mncs-compiler`/runtime ownership with its corpora.
Until then, changes here must stay consistent with RFC 0048.
