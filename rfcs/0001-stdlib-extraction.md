# RFC 0001: Standard-library extraction (Stage F)

- Status: **accepted / implemented** (2026-10-02)
- Summary: move the MNCS standard library out of `mncs-language`
  into the independently owned `mncs-stdlib` repository, and
  integrate it as a first-class environment component.
- Motivation: the library outgrew colocation. Language evolution and
  library evolution need separate change velocities, separate
  authority, and a machine-readable composition contract. The
  `mncs-language` direction doc (`docs/core-standard-library.md`)
  deferred this split to "Stage F (future)" pending a stable
  semantic/package boundary; the module system (Profile 0.6
  elaboration-time linking, 0.9 qualified/aliased routes, binding
  tables), the content-addressed bundle pin (INGEST-P-008), and the
  profile mechanism now constitute that boundary.
- Terminology: *module* (one `mncs.*` source unit), *bundle pin*
  (`mncs.stdlib-bundle/1` content-addressed distribution), *manifest*
  (`mncs.stdlib-manifest/1` compatibility contract), *profile*
  (source-language capability level, the compatibility unit).

## Proposed shape

```text
mncs-language   syntax, semantics, profiles, module rules,
                reference compiler, bundle format, harnesses
mncs-compiler   successor compiler (fellow stdlib consumer)
mncs-stdlib     library sources, executable contracts, bundle pin,
                compatibility manifest, provider contracts
```

Resolution: filesystem roots for development (`MNCS_STDLIB_ROOT`,
`MNCS_LIBRARY_PATH`, toolchain sibling default), bundle pin for
distribution (`MNCS_STDLIB_BUNDLE`, in-process `pinned_bundle()`).
Compatibility: profiles + content identities, no SemVer.
Composition validation: Doctor + environment from the manifest.

## Validation obligations

- Bundle regenerates byte-identically; manifest matches bundle/tree.
- All corpora regenerate byte-identically (newly enforced).
- Language conformance harnesses pass reading across repos.
- Environment entry discovers the stdlib provider; re-entry is quiet.
- Doctor reports composition state; LSP resolves stdlib imports.
- No dependency on `mncs-language/library/` anywhere (removed).

## Trust and security consequences

- The bundle pin is self-verifying (per-module + identity hashes);
  divergence fails closed (`MNE234`).
- The language-vendored pin is a lockfile, identity-checked — a
  pinned dependency, not a second canonical copy.
- Toolchain compromise remains outside the stdlib verification
  boundary (toolchain policy owns it).

## Alternatives considered

- *Keep colocated*: rejected — conflates language and library change
  velocity and authority; the task family needs the boundary now.
- *Split family/jit into further repos immediately*: rejected —
  they share the tested module closure; transient hosting with
  recorded pressures (STDLIB-P-001/-002) avoids inventing boundaries
  prematurely (the same principle that once deferred this split).
- *Symlink `mncs-language/library` at the old path*: rejected —
  preserves the old location as a dependency and hides the boundary.
- *SemVer for compatibility*: rejected — profiles + content
  identities are the existing, better mechanism.

## Unresolved questions

- Long-term owner of `mncs.family.*` (Commons? automation?) and of
  `mncs.jit.*` (compiler? runtime?) — pressures filed.
- Store-backed index publication — schema reserved, activation
  criteria documented, implementation deferred.
- Language-service navigation into library files (SymbolIndex gap) —
  pressure filed in `mncs-language-service`.

## Compatibility and migration notes

See `docs/MIGRATION.md` (move list + repair log) and
`docs/MIGRATION-corpora.md` (per-file appendix). Language tests and
family runners resolve the new location via `MNCS_STDLIB_ROOT`, the
sibling checkout, or the toolchain default; stale
`mncs-language/library` path entries are skipped as missing.
