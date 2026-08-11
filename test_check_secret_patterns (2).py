"""Tests for the content-based secret-pattern guard."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_secret_patterns as guard


def rules_for(path: str, text: str) -> set[str]:
    return {finding.rule for finding in guard.content_findings(path, text.encode())}


class GenericSecretAssignmentTest(unittest.TestCase):
    def test_bundled_javascript_identifiers_are_not_secret_literals(self):
        source = "\n".join(
            (
                "config.apiKey = DEFAULT_APPLICATION_CONFIGURATION_KEY",
                "const value = {token: exportedAuthenticationTokenFactory}",
                "const request = {password: PasswordCredentialRequestOptions}",
                "const result = {secret: cryptoProvider.deriveApplicationSecret}",
            )
        )
        self.assertNotIn("generic_secret_assignment", rules_for("plugin/main.js", source))

    def test_quoted_credential_literal_is_detected_in_source(self):
        source = 'const config = {apiKey: "aB3dE5fG7hJ9kL2mN4pQ6rS8tV0xY1zC"};'  # secret-pattern: allow
        self.assertIn("generic_secret_assignment", rules_for("plugin/main.js", source))

    def test_quoted_credential_literal_is_detected_in_ajson(self):
        source = '{"api_key": "' + ("x7" * 20) + '"}'
        self.assertIn("generic_secret_assignment", rules_for("registry.ajson", source))

    def test_unquoted_credential_is_detected_in_declarative_config(self):
        source = "api_key: aB3dE5fG7hJ9kL2mN4pQ6rS8tV0xY1zC"
        self.assertIn("generic_secret_assignment", rules_for("config.yaml", source))

    def test_unquoted_identifier_is_not_scanned_as_data_in_python(self):
        source = "api_key = DEFAULT_APPLICATION_CONFIGURATION_KEY"
        self.assertNotIn("generic_secret_assignment", rules_for("settings.py", source))

    def test_placeholder_and_endpoint_literals_are_allowed(self):
        source = "\n".join(
            (
                'api_key = "replace-with-development-key"',
                'token = "https://example.test/authentication/endpoint"',
            )
        )
        self.assertNotIn("generic_secret_assignment", rules_for("settings.py", source))

    def test_dedicated_token_detector_is_unchanged(self):
        source = "value = 'ghp_" + ("A" * 40) + "'"
        self.assertIn("github_token", rules_for("settings.py", source))

    def test_attested_full_calendar_vendor_key_is_allowed_only_in_vendor_bundle(self):
        value = "AIzaSyDIiklFwJ" + "XaLWuT_4y6I9ZRVVsPuf4xGrk"
        source = f'googleCalendarApiKey: "{value}",'
        vendor_path = ".obsidian/plugins/obsidian-full-calendar/main.js"
        self.assertNotIn("google_api_key", rules_for(vendor_path, source))
        self.assertIn("google_api_key", rules_for("copied-plugin/main.js", source))

    def test_changed_full_calendar_key_is_not_allowed(self):
        source = 'googleCalendarApiKey: "' + "AIza" + ("A" * 35) + '",'
        vendor_path = ".obsidian/plugins/obsidian-full-calendar/main.js"
        self.assertIn("google_api_key", rules_for(vendor_path, source))


if __name__ == "__main__":
    unittest.main()
