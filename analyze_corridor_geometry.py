import json
from pathlib import Path
from collections import defaultdict

raw = json.loads(Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_corridor_roads.json').read_text())
groups = defaultdict(list)
for way in raw.get('elements', []):
    tags = way.get('tags', {})
    key = tags.get('ref') or tags.get('name') or 'unnamed'
    geometry = way.get('geometry') or []
    if not geometry:
        continue
    points = [(p['lat'], p['lon']) for p in geometry]
    groups[key].append((tags.get('name',''), tags.get('highway',''), points))

for key, ways in sorted(groups.items()):
    pts = [p for _,_,points in ways for p in points]
    print('\n', key, 'ways=', len(ways), 'extent=', round(min(p[0] for p in pts),5), round(max(p[0] for p in pts),5), round(min(p[1] for p in pts),5), round(max(p[1] for p in pts),5))
    for i, (name, highway, points) in enumerate(ways[:12]):
        print(' ', i, name, highway, 'start=', tuple(round(x,5) for x in points[0]), 'end=', tuple(round(x,5) for x in points[-1]), 'n=', len(points))
