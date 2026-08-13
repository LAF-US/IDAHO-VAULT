import json
from pathlib import Path

raw = json.loads(Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_roads.json').read_text())
for way in raw.get('elements', []):
    tags = way.get('tags', {})
    name = tags.get('name', '')
    geometry = way.get('geometry') or []
    if not name or not geometry:
        continue
    lats = [p['lat'] for p in geometry]
    lons = [p['lon'] for p in geometry]
    if max(lats) < 44.25 or min(lats) > 44.95 or max(lons) < -116.75 or min(lons) > -115.9:
        continue
    print(name, '|', tags.get('ref',''), '|', tags.get('highway',''), '|', tuple(round(x,5) for x in geometry[0].values()), '->', tuple(round(x,5) for x in geometry[-1].values()))
