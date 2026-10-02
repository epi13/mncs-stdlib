#!/usr/bin/env bash
# Regenerate stdlib distribution artifacts from library/.
#   ./tools/regen.sh          regenerate dist/ + stdlib-manifest.json
#   ./tools/regen.sh --check  verify committed artifacts are current
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECK=0
if [[ "${1:-}" == "--check" ]]; then CHECK=1; fi

MNCS_BIN="${MNCS_BIN:-}"
if [[ -z "$MNCS_BIN" ]]; then
    for candidate in "$ROOT/../mncs-language/target/release/mncs" \
                     "$ROOT/../mncs-language/target/debug/mncs"; do
        if [[ -x "$candidate" ]]; then MNCS_BIN="$candidate"; break; fi
    done
fi
if [[ -z "$MNCS_BIN" || ! -x "$MNCS_BIN" ]]; then
    echo "error: no mncs binary; set MNCS_BIN or check out mncs-language as a sibling" >&2
    exit 2
fi

if [[ "$CHECK" == 1 ]]; then
    TMP="$(mktemp -d)"
    trap 'rm -rf "$TMP"' EXIT
    "$MNCS_BIN" bundle generate --library "$ROOT/library" --output "$TMP/bundle.json" \
        --commit "$(cd "$ROOT" && git rev-parse --short HEAD 2>/dev/null || echo unknown)" >/dev/null
    # Compare modulo the source_commit stamp: identity + modules must match.
    python3 - "$ROOT/dist/stdlib-bundle.json" "$TMP/bundle.json" <<'EOF'
import json, sys
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
aa = {k: v for k, v in a.items() if k != "source_commit"}
bb = {k: v for k, v in b.items() if k != "source_commit"}
if aa != bb or a["bundle_identity"] != b["bundle_identity"]:
    sys.exit("error: dist/stdlib-bundle.json drifts from library/; run ./tools/regen.sh")
EOF
    python3 "$ROOT/tools/gen_manifest.py" --root "$ROOT" --check
    echo "artifacts current"
    exit 0
fi

mkdir -p "$ROOT/dist"
"$MNCS_BIN" bundle generate --library "$ROOT/library" \
    --output "$ROOT/dist/stdlib-bundle.json" \
    --commit "$(cd "$ROOT" && git rev-parse --short HEAD 2>/dev/null || echo unknown)"
python3 "$ROOT/tools/gen_manifest.py" --root "$ROOT"
"$MNCS_BIN" bundle verify "$ROOT/dist/stdlib-bundle.json"
