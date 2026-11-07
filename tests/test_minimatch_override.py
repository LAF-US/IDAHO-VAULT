"""Tests for the minimatch security override (GHSA-g3hv-75wg-m249, #1100)."""

import json
from pathlib import Path

_ROOT = Path(__file__).parents[1]
PACKAGE_JSON = _ROOT / "package.json"
PACKAGE_LOCK = _ROOT / "package-lock.json"

# GHSA-g3hv-75wg-m249 (CWE-405, globparts amplification DoS) affects minimatch 7.0.0 through 11.0.0.
PATCHED = (11, 0, 1)


def _release(version):
    """Parse a semver string into a comparable release tuple."""
    core = version.split("-", 1)[0].split("+", 1)[0]
    return tuple(int(part) for part in core.split("."))


def _floor(spec):
    """Return the lowest release a caret, tilde or minimum-range spec allows."""
    if "||" in spec:
        raise ValueError(f"OR range may allow a vulnerable release: {spec}")
    for prefix in (">=", "^", "~", "="):
        if spec.startswith(prefix):
            return _release(spec[len(prefix) :].strip().split()[0])
    return _release(spec.strip().split()[0])


def test_floor_handles_compound_ranges_and_rejects_or_ranges():
    """A multi-token range uses its first bound; an OR range fails closed."""
    assert _floor(">=11.0.1 <12") == (11, 0, 1)
    assert _floor("^11.0.1") == (11, 0, 1)
    try:
        _floor("^11.0.1 || ^10.0.0")
    except ValueError:
        return
    raise AssertionError("_floor accepted an OR range that still allows 10.x")


def test_package_json_pins_minimatch_above_the_advisory():
    """The override must resolve minimatch to a patched 11.x release."""
    package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
    spec = package.get("overrides", {}).get("minimatch")
    assert spec, "package.json is missing an overrides.minimatch entry"
    assert _floor(spec) >= PATCHED, f"overrides.minimatch {spec} still allows a vulnerable release"


def test_lockfile_resolves_every_minimatch_to_a_patched_release():
    """No lockfile entry, top-level or nested, may stay below the patched floor."""
    lock = json.loads(PACKAGE_LOCK.read_text(encoding="utf-8"))
    entries = {
        name: entry["version"]
        for name, entry in lock["packages"].items()
        if name == "node_modules/minimatch" or name.endswith("/node_modules/minimatch")
    }
    assert entries, "package-lock.json has no minimatch entry"
    stale = {name: ver for name, ver in entries.items() if _release(ver) < PATCHED}
    assert stale == {}, f"vulnerable minimatch still resolved: {stale}"
