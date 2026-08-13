import json
from collections import defaultdict
from pathlib import Path

raw = json.loads(Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_roads.json').read_text())
by_name = defaultdict(list)
for way in raw.get('elements', []):
    tags = way.get('tags', {})
    geometry = way.get('geometry') or []
    if not geometry:
        continue
    lats = [p['lat'] for p in geometry]
    lons = [p['lon'] for p in geometry]
    if max(lats) < 44.2 or min(lats) > 44.65 or max(lons) < -116.35 or min(lons) > -115.85:
        continue
    key = (tags.get('name',''), tags.get('ref',''), tags.get('highway',''))
    by_name[key].append((min(lats), max(lats), min(lons), max(lons)))
for key, extents in sorted(by_name.items()):
    if not key[0] and not key[1]:
        continue
    print(key, 'ways=', len(extents), 'extent=', tuple(round(x,5) for x in (min(x[0] for x in extents), max(x[1] for x in extents), min(x[2] for x in extents), max(x[3] for x in extents))))
