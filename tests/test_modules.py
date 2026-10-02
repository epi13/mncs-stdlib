"""Module structure, layering, and catalog honesty (no toolchain)."""

import os
import re

MODULE_RE = re.compile(r"^module\s+([\w.]+);", re.M)
PROFILE_RE = re.compile(r"^mncs\s+([0-9.]+);", re.M)
USE_RE = re.compile(r"^use\s+([\w.]+?)(?:\s+as\s+\w+)?;", re.M)

# namespace -> namespaces it may import (mncs.* only; anything else fails).
# core is self-contained but internally layered (acyclic; see the
# no-import-cycles test): e.g. vision builds on image/geometry/contracts.
ALLOWED_IMPORTS = {
    "core": {"core"},
    "std": {"core", "std"},
    "family": {"core"},
    "jit": {"core", "jit"},
    "capability": set(),
}


def iter_modules(library_root):
    for namespace in sorted(os.listdir(library_root)):
        ns_dir = os.path.join(library_root, namespace)
        if not os.path.isdir(ns_dir):
            continue
        for filename in sorted(os.listdir(ns_dir)):
            if filename.endswith(".mncs"):
                yield namespace, filename, os.path.join(ns_dir, filename)


def namespace_of(module_name):
    parts = module_name.split(".")
    assert parts[0] == "mncs" and len(parts) >= 3
    return parts[1]


def test_one_module_per_file_and_mncs_namespace(library_root):
    for namespace, filename, path in iter_modules(library_root):
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        declarations = MODULE_RE.findall(text)
        assert len(declarations) == 1, f"{path}: {declarations}"
        assert declarations[0].startswith("mncs."), path
        assert PROFILE_RE.search(text), f"{path}: no profile header"


def test_layering(library_root):
    violations = []
    for namespace, filename, path in iter_modules(library_root):
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        for imported in USE_RE.findall(text):
            if not imported.startswith("mncs."):
                violations.append(f"{path} imports non-mncs {imported}")
                continue
            target = namespace_of(imported)
            if target not in ALLOWED_IMPORTS[namespace]:
                violations.append(f"{path} ({namespace}) imports {imported}")
    assert not violations, "\n".join(violations)


def test_no_import_cycles(manifest):
    graph = {m["name"]: m.get("imports", []) for m in manifest["modules"]}
    visiting, done = set(), set()

    def visit(node, stack):
        if node in done:
            return
        assert node not in visiting, f"import cycle: {' -> '.join([*stack, node])}"
        visiting.add(node)
        for edge in graph.get(node, []):
            visit(edge, [*stack, node])
        visiting.discard(node)
        done.add(node)

    for name in graph:
        visit(name, [])


def test_capability_reserved(library_root):
    capability = os.path.join(library_root, "capability")
    assert os.path.isdir(capability)
    mncs_files = [
        f for f in os.listdir(capability) if f.endswith(".mncs")
    ]
    assert mncs_files == [], "capability/ must stay empty until its features exist"


def test_header_summary_present(library_root):
    missing = []
    for namespace, filename, path in iter_modules(library_root):
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
        documented = any(
            line.strip().startswith("//")
            and not line.strip().startswith("///")
            and line.strip()[2:].strip()
            for line in lines
        )
        if not documented:
            missing.append(path)
    assert not missing, missing


def test_catalog_lists_every_module(root, manifest):
    with open(os.path.join(root, "library", "README.md"), encoding="utf-8") as handle:
        catalog = handle.read()
    for module in manifest["modules"]:
        assert f"`{module['name']}`" in catalog, module["name"]
        assert f"`{module['path']}`" in catalog, module["path"]
