import json
from collections import defaultdict
from pathlib import Path

raw = json.loads(Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_emmett_sweet_roads.json').read_text())
by_name = defaultdict(list)
for way in raw.get('elements', []):
    tags = way.get('tags', {})
    highway = tags.get('highway','')
    if highway not in {'motorway','trunk','primary','secondary','tertiary','unclassified'}:
        continue
    geometry = way.get('geometry') or []
    if not geometry:
        continue
    lats = [p['lat'] for p in geometry]
    lons = [p['lon'] for p in geometry]
    by_name[(tags.get('name',''), tags.get('ref',''), highway)].append((min(lats), max(lats), min(lons), max(lons)))
for key, extents in sorted(by_name.items()):
    min_lat=min(x[0] for x in extents); max_lat=max(x[1] for x in extents)
    min_lon=min(x[2] for x in extents); max_lon=max(x[3] for x in extents)
    print(key, 'ways=',len(extents), 'extent=', tuple(round(x,5) for x in (min_lat,max_lat,min_lon,max_lon)))
