import json
from pathlib import Path

raw = json.loads(Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_corridor_roads.json').read_text())
keep = {'Sweet Ola Highway', 'High Valley Road', 'Cabarton High Valley Road', 'Council Cuprum Road', 'Council Road'}
for way in raw.get('elements', []):
    tags = way.get('tags', {})
    if tags.get('name') not in keep or not way.get('geometry'):
        continue
    pts = [(round(p['lat'], 5), round(p['lon'], 5)) for p in way['geometry']]
    print(tags.get('name'), tags.get('highway'), 'start', pts[0], 'end', pts[-1], 'count', len(pts))
