# STDLIB-P-001: Long-term owner for `mncs.family.*` modules

- Date: 2026-10-02, status: **open**
- Owning layer: undecided (family governance — Commons? automation? doc?)
- Upstream: not yet filed (decision needed before filing)

`mncs.family.rfc_status/journal/coherence` encode family process
policy (RFC gates, Journal admission, coherence verdicts). They are
not portable library surface, but they share the module closure,
profile machinery, and corpus/test patterns with the stdlib, so the
extraction hosts them transiently under `library/family/` rather
than inventing a premature third home.

Resolution: decide the owning subsystem, move the modules with their
corpora/generators, and delete them here. The stdlib keeps no
family-policy authority either way.
