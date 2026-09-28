import sys
from pathlib import Path

from cli_path_guard import repo_path

# Paths accept command-line overrides, containment-checked to repository files.
_REPO = Path(__file__).resolve().parent
path = repo_path(sys.argv[1]) if len(sys.argv) > 1 else _REPO / 'cron_clock_gregorian_floating.ics'
text = path.read_text(encoding='utf-8')
normalized = text.replace('\r\n', '\n').replace('\r', '\n').rstrip('\n') + '\n'
path.write_bytes(normalized.replace('\n', '\r\n').encode('utf-8'))
print(f'Normalized {path} to CRLF content lines.')
