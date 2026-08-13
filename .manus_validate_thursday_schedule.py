from pathlib import Path

import yaml

root = Path(__file__).resolve().parent
config = yaml.safe_load((root / ".github/dependabot.yml").read_text())
updates = {entry["package-ecosystem"]: entry for entry in config["updates"]}
assert set(updates) == {"github-actions", "gitsubmodule"}
for ecosystem, entry in updates.items():
    assert entry["schedule"] == {
        "interval": "cron",
        "cronjob": "0 12 * * thu%2",
        "timezone": "America/Denver",
    }, ecosystem

assert "every other Thursday at noon America/Denver" in (root / "ENV.md").read_text()
assert "every second Thursday at 12:00 America/Denver" in (
    root / ".crewai/MANIFEST.md"
).read_text()
print("Thursday-noon Dependabot schedule validation passed.")
