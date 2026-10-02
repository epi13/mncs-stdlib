"""Shared fixtures for the mncs-stdlib integrity suite."""

import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pytest_configure(config):
    config.addinivalue_line("markers", "toolchain: needs an mncs binary")


@pytest.fixture(scope="session")
def root():
    return ROOT


@pytest.fixture(scope="session")
def library_root(root):
    return os.path.join(root, "library")


@pytest.fixture(scope="session")
def manifest(root):
    import json

    with open(os.path.join(root, "stdlib-manifest.json"), encoding="utf-8") as handle:
        return json.load(handle)


@pytest.fixture(scope="session")
def bundle(root):
    import json

    with open(os.path.join(root, "dist", "stdlib-bundle.json"), encoding="utf-8") as handle:
        return json.load(handle)


def resolve_mncs(root):
    override = os.environ.get("MNCS_BIN")
    if override:
        return override
    for candidate in (
        os.path.join(root, "..", "mncs-language", "target", "release", "mncs"),
        os.path.join(root, "..", "mncs-language", "target", "debug", "mncs"),
    ):
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return os.path.abspath(candidate)
    return None


@pytest.fixture(scope="session")
def mncs_bin(root):
    binary = resolve_mncs(root)
    if binary is None:
        pytest.skip(
            "no mncs binary: set MNCS_BIN or check out mncs-language "
            "as a sibling (../mncs-language)"
        )
    return binary
