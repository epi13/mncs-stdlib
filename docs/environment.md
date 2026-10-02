# Environment integration

Entering the MNCS environment composes a coherent stack:

```text
language -> selected language contract
compiler -> compatible compiler
stdlib   -> compatible standard library (this repo)
lsp      -> semantic/index context containing stdlib
doctor   -> validates the composition
```

## How this repo is discovered

The environment selects `mncs-stdlib` by repository name in the
workspace scope, then discovers provider contracts from two files:

- `family-semantic-contracts-v1.json` — callable declarations:
  - `mncs.stdlib-manifest/1` → `tools/stdlib_info.py` (index, module
    lookup, compatibility verdict). Cheap: pure Python over the
    manifest, no toolchain, bounded output.
  - `adapter_library_paths: ["library"]` — session MNCS resolution
    includes this repo's library root wherever the session invokes
    through the binding.
- `.mncs/project.json` — repository manifest: `provides` (stdlib
  source/bundle/manifest contracts with fingerprint sources),
  `consumes` (language compiler contract, informational), `tests`
  (integrity suite bindings), and the verification inventory.

No guessed paths, branch assumptions, hardcoded checkouts, or ambient
`PATH` behavior: the manifest names the library root and bundle, and
the info tool answers queries.

## Composition checks

The environment and Doctor validate the selected composition from
machine-readable facts:

| Question | Answered by |
|---|---|
| Is a usable stdlib present? | checkout selected + manifest parses + bundle verifies |
| Is it compatible with the language/compiler? | `requires_profile.max` ≤ toolchain max profile |
| Can the compiler compile it? | toolchain validation over `library/` (stdlib toolchain tests) |
| Are indexes/metadata current? | manifest ↔ bundle ↔ tree freshness (`--check`) |
| Which modules exist? | `stdlib_info.py list` (names, profiles, digests) |

## Agent ergonomics

Agents get stdlib awareness without context dumps:

- `stdlib_info.py list` — compact module index (name, profile, digest);
- `stdlib_info.py show <module>` — header contract + source path;
- `stdlib_info.py compatible --max-profile X` — composition verdict;
- `stdlib_info.py lookup <term>` — symbol discovery across headers.

The environment projection surfaces the index summary; full sources
are fetched on demand by path. Nothing here prints the library into
prompts.

## Startup and caching behavior

- Manifest/bundle reads are plain file reads; verification is
  `sha256` over ~1.4 MB — milliseconds, no subprocesses.
- Toolchain compilation of modules happens only in the toolchain
  test slice and in consumers that import them; fingerprints ride
  the existing elaboration identity machinery.
- Re-entry is quiet: entry reuses the selected session and cached
  bindings; no re-indexing, no reparsing.
