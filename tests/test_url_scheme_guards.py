"""Scheme guards on the urlopen call sites."""

# Deliberately a one-line docstring: Codacy runs D212 (summary on the first
# line) and D213 (summary on the second) together, and no multi-line docstring
# satisfies both -- moving the summary to line 2 to clear D213 raised D212.
# A single-line docstring makes neither rule applicable, so the prose lives
# here instead of being lost.
#
# `urllib.request.urlopen` honours `file://` and `ftp://`, so a URL that
# reaches it decides whether the call is a network request or a local-disk
# read. These scripts take their URLs from an environment variable, a CLI
# flag, and a caller-supplied list respectively -- all operator-controlled
# today, none of them constrained by the type system tomorrow. The scheme is
# settled where the URL enters rather than assumed from where it came.

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str, relative: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        # Not an assert: `python -O` strips those, and a loader that silently
        # became None would then surface as an AttributeError further down.
        raise ImportError(f"cannot load {name} from {path}")
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

    def test_ftp_scheme_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            janitor_sweep.SlackReporter("ftp://hooks.slack.com/services/x")

    def test_missing_scheme_is_refused(self) -> None:
        # urlparse gives these an empty scheme, which is not https.
        for value in ("hooks.slack.com/services/x", "//hooks.slack.com/services/x"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                janitor_sweep.SlackReporter(value)

    def test_error_message_does_not_echo_the_webhook(self) -> None:
        # The webhook URL is the credential -- anyone holding it can post to the
        # channel -- and this message reaches workflow logs.
        with self.assertRaises(ValueError) as exc:
            janitor_sweep.SlackReporter("http://hooks.slack.com/services/SECRETPATH")
        self.assertNotIn("SECRETPATH", str(exc.exception))

    def test_https_is_accepted(self) -> None:
        reporter = janitor_sweep.SlackReporter("https://hooks.slack.com/services/x")
        self.assertEqual(reporter.webhook_url, "https://hooks.slack.com/services/x")


class JanitorFailsOpenTest(unittest.TestCase):
    """A bad webhook must not cost the run its report."""

    # janitor_sweep exists to report a failed workflow. Letting the scheme
    # guard's ValueError escape main() would kill the script before it prints
    # any JSON -- so a misconfigured secret would silently suppress the very
    # alert the script is for.

    def test_bad_webhook_still_prints_json_and_exits_zero(self) -> None:
        event = {
            "workflow_run": {
                "name": "ci", "html_url": "https://example.invalid/run",
                "head_branch": "main", "conclusion": "failure", "id": 1,
            },
            "repository": {"full_name": "LAF-US/IDAHO-VAULT"},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "event.json"
            path.write_text(json.dumps(event), encoding="utf-8")
            env = {
                "GITHUB_EVENT_PATH": str(path),
                "JANITOR_SLACK_WEBHOOK_URL": "file:///etc/passwd",
            }
            buf = io.StringIO()
            with patch.dict(os.environ, env, clear=False), redirect_stdout(buf):
                status = janitor_sweep.main()

        self.assertEqual(status, 0)
        payload = json.loads(buf.getvalue())
        targets = {o["target"]: o for o in payload["outputs"]}
        self.assertIn("SlackReporter", targets)
        self.assertFalse(targets["SlackReporter"]["ok"])
        self.assertNotIn("/etc/passwd", buf.getvalue())


class HealthProbeSchemeTest(unittest.TestCase):
    """Cover the probe's own scheme check."""

    # `main` takes any Iterable[ServiceSpec], so the module's four literal
    # URLs are not the only ones that reach the probe.

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
