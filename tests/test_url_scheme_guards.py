"""Scheme guards on the urlopen call sites.

`urllib.request.urlopen` honours `file://` and `ftp://`, so a URL that reaches
it decides whether the call is a network request or a local-disk read. These
scripts take their URLs from an environment variable, a CLI flag, and a caller
-supplied list respectively -- all operator-controlled today, none of them
constrained by the type system tomorrow. The scheme is settled where the URL
enters rather than assumed from where it came.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


janitor_sweep = _load("janitor_sweep_under_test", ".github/scripts/janitor_sweep.py")
health_monitor = _load("health_monitor_under_test", "scripts-health_monitor.py")


class SlackWebhookSchemeTest(unittest.TestCase):
    def test_file_scheme_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            janitor_sweep.SlackReporter("file:///etc/passwd")

    def test_plaintext_http_is_refused(self) -> None:
        # A Slack webhook carries the failure report; http would put it on the
        # wire in clear text, and Slack does not serve the endpoint over http.
        with self.assertRaises(ValueError):
            janitor_sweep.SlackReporter("http://hooks.slack.com/services/x")

    def test_https_is_accepted(self) -> None:
        reporter = janitor_sweep.SlackReporter("https://hooks.slack.com/services/x")
        self.assertEqual(reporter.webhook_url, "https://hooks.slack.com/services/x")


class HealthProbeSchemeTest(unittest.TestCase):
    """`main` takes any Iterable[ServiceSpec], so the module defaults are not
    the only URLs that reach the probe."""

    def test_file_scheme_is_reported_unreachable_without_opening_it(self) -> None:
        result = health_monitor.check_service(
            health_monitor.ServiceSpec(name="probe", url="file:///etc/passwd"),
            timeout=1.0,
        )
        self.assertFalse(result.ok)
        self.assertIn("unsupported URL scheme", result.detail)
        self.assertIsNone(result.status_code)

    def test_ftp_scheme_is_refused(self) -> None:
        result = health_monitor.check_service(
            health_monitor.ServiceSpec(name="probe", url="ftp://example.invalid/x"),
            timeout=1.0,
        )
        self.assertFalse(result.ok)
        self.assertIn("unsupported URL scheme", result.detail)


if __name__ == "__main__":
    unittest.main()
