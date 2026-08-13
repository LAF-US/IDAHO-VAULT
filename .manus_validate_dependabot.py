from pathlib import Path

import yaml

root = Path(__file__).resolve().parent
config = yaml.safe_load((root / ".github/dependabot.yml").read_text())
assert config["version"] == 2
updates = {entry["package-ecosystem"]: entry for entry in config["updates"]}
assert set(updates) == {"github-actions", "gitsubmodule"}
for ecosystem, entry in updates.items():
    assert entry["directory"] == "/", ecosystem
    assert entry["schedule"] == {
        "interval": "cron",
        "cronjob": "0 9 * * mon%2",
        "timezone": "America/Denver",
    }, ecosystem
assert updates["github-actions"]["open-pull-requests-limit"] == 5
assert updates["github-actions"]["allow"] == [{"dependency-type": "all"}]
assert updates["gitsubmodule"]["open-pull-requests-limit"] == 1

modules = (root / ".gitmodules").read_text()
assert "path = DND-SRD-5.2.1-UPSTREAM" in modules
assert "url = https://github.com/downfallx/dnd-5e-srd-markdown.git" in modules

workflow = (root / ".github/workflows/sync-dependencies.yml").read_text()
assert "uv lock --upgrade" in workflow
assert "uv export --format requirements-txt --no-hashes --output-file requirements.txt" in workflow

for path in (root / "ENV.md", root / ".crewai/MANIFEST.md"):
    text = path.read_text()
    assert "uv sync" in text, path
    assert "uv.lock" in text, path
    assert "Dependabot" in text, path

print("Dependabot configuration and current uv documentation validation passed.")
