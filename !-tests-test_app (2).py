from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def load_app_module():
    repo_root = Path(__file__).resolve().parents[2]
    module_path = repo_root / "main.py"
    spec = importlib.util.spec_from_file_location("vault_main", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load app module from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AppRouteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_module = load_app_module()
        cls.client = cls.app_module.app.test_client()

    def test_post_handler_returns_ok(self):
        response = self.client.post("/")
        self.assertEqual(200, response.status_code)
        self.assertEqual("OK", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
