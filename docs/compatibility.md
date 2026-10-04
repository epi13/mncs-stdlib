# Compatibility model

Stdlib compatibility is capability/profile-based, not SemVer. Three
machine-readable facts compose:

```text
language contract X        mncs-language: supported source profiles
      ↓                    (spec/, docs/language-capabilities.json)
compiler supports X        toolchain: max supported profile + backend
      ↓                    envelopes (mncs experiment matrix)
stdlib requires X          this repo: requires_profile + bundle identity
      ↓                    (stdlib-manifest.json)
composition verdict        requires_profile.max ≤ toolchain max, and the
                           bundle verifies byte-for-byte
```

## The manifest

`stdlib-manifest.json` (schema `mncs.stdlib-manifest/1`) is generated
from the bundle pin by `tools/gen_manifest.py`:

- `bundle_identity`: `mncs:stdlib-bundle:{hex}` over sorted
  `(name, content_sha256)` pairs — the pin names content, never a
  path, timestamp, or branch;
- `requires_profile: {min, max}`: minimum and maximum declared
  source profiles across modules (today: min `0.5`, max `0.18`);
- `modules[]`: name, library-relative path, declared profile, and
  `content_sha256` per module;
- `source`: repository + commit the manifest was generated from.

`tools/gen_manifest.py --check` fails closed on any drift between the
manifest, the bundle, and the working tree. The integrity suite runs
this check without a toolchain installed.

## Answering "can these compose?"

```bash
python3 tools/stdlib_info.py compatible --max-profile 0.18
# {"compatible": true, "requires_profile": {"min": "0.5", "max": "0.18"},
#  "bundle_identity": "mncs:stdlib-bundle:...", "reason": "..."}
```

Rules:

1. Every module profile must be ≤ the toolchain's max supported
   profile (numeric `major.minor` comparison; profiles are ordered).
2. The bundle pin must verify: every per-module hash and the bundle
   identity recompute exactly.
3. Backend envelopes are orthogonal: a supported profile does not
   imply every backend realizes every module. Envelope facts
   (`SUPPORTED`/`UNSUPPORTED`/`UNKNOWN`) come from corpus execution,
   recorded per run — never from this manifest.

Doctor (findings folded into the `toolchain-health` check; a dedicated
`stdlib-health` id waits on `mncs-doctor` pressure DOC-P-023) and the
environment composition read this manifest; they never guess from paths
or branches.

## Profile discipline for contributors

- Declare the lowest profile the module actually needs. A higher
  profile raises `requires_profile.max` for every consumer when it
  becomes the maximum — today that cost is carried by
  `mncs.std.process.v1` (0.18) alone.
- A module may only use syntax/semantics its declared profile
  provides; the toolchain elaborates each module at its profile.
- Raising a module's profile is a compatibility change: note it in
  the change, confirm the toolchain floor still satisfies it, and
  regenerate the manifest.

## Backend envelope (observed, not promised)

Corpora execute on reference, research-bytecode, portable-WASM, C11,
LLVM, and Cranelift paths through the language conformance harnesses.
Agreement rows describe observed envelopes. Exact-cost obligations
remain `UNKNOWN` where profiles cannot discharge them; sequences of
masks/vectors and logical `[bool; N]` windows follow the documented
substrate rules. When an envelope changes, the execution record —
not this file — is the authority.
