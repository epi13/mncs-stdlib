# Adding a library facility

## Before you write

1. Query the index: `python3 tools/stdlib_info.py list` and
   `... show <module>`. If the facility exists, use it.
2. Check `pressures/registry.json`: the gap may already be recorded
   with an owning layer and a workaround policy.
3. Read the namespace rules in `ARCHITECTURE.md` and the honesty
   properties in `library/README.md`.

A facility earns its place by providing reusable semantics, a
meaningful abstraction boundary, or useful architectural pressure.
One-off conveniences, host-service wrappers, and clones of another
language's hierarchy do not belong here.

## The triple

Every module ships three parts atomically:

1. **Source**: `library/<ns>/<name>.mncs`, one module per file.
   Header form:
   ```text
   mncs <lowest-profile-that-fits>;
   // mncs.<ns>.<name> — one-line summary ending in a period.
   // (further contract/backpressure notes as needed)
   module mncs.<ns>.<name>.v1;
   ```
   Total and effect-free unless a capability design exists and is
   declared. Respect namespace imports (`core` ← `std`; `family`/`jit`
   ← `core` only). Never map `UNKNOWN` to `PASS` or delete `FAIL`.
2. **Executable contract**: bounded corpus under
   `examples/execution/` pinning behavior case by case, plus a
   consumer witness under `examples/source/` when the module is
   consumer-facing.
3. **Generator**: deterministic pure-Python script under `scripts/`
   whose output matches the committed corpus byte-for-byte.
   Self-contained: no toolchain, no sibling-repo reads.

Then regenerate and verify:

```bash
./tools/regen.sh
python3 -m pytest tests/ -q
```

## Checklist

- [ ] Lowest honest profile declared; manifest `requires_profile`
      impact understood.
- [ ] Corpus covers acceptance *and* rejection behavior.
- [ ] `library/README.md` catalog row added (header line feeds it).
- [ ] Bundle + manifest regenerated; freshness tests green.
- [ ] Toolchain tests compile the module (`tests/test_toolchain.py`).
- [ ] Pressures recorded for anything MNCS could not express cleanly.
- [ ] Backend envelope observed (or explicitly `UNKNOWN`), never claimed.
