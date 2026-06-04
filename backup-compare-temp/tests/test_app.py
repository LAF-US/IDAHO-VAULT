from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import swarm.app as app


class AppLoopTest(unittest.TestCase):
    def test_process_document_writes_file_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_root = Path(tmpdir)
            manifest = vault_root / "manifest.json"
            manifest.write_text('{"files": []}\n', encoding="utf-8")

            with patch.object(app, "VAULT_ROOT", vault_root), patch.object(app, "MANIFEST_PATH", manifest):
                entry = app.run("process document")

            created_file = vault_root / entry["path"]
            self.assertTrue(created_file.exists())

            data = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(1, len(data["files"]))
            self.assertEqual(entry["path"], data["files"][0]["path"])
            self.assertEqual("ingest", data["files"][0]["type"])


if __name__ == "__main__":
    unittest.main()
