import json
from pathlib import Path
import requests

bbox = '(43.15,-117.25,45.15,-115.55)'
query = f'''[out:json][timeout:180];way[highway~"motorway|trunk|primary|secondary|tertiary|unclassified"][name]{bbox};out tags geom;'''
endpoint = 'https://overpass.private.coffee/api/interpreter'
response = requests.get(endpoint, params={'data': query}, headers={'User-Agent': 'idaho-highway-map-research/1.0'}, timeout=240)
response.raise_for_status()
raw = response.json()

keep_local = ('sweet', 'ola', 'high valley', 'cabarton', 'council', 'emmett', 'horseshoe bend', 'weiser', 'payette', 'midvale', 'cambridge', 'idaho city', 'boise', 'eagle', 'meridian', 'star', 'middleton')
keep_classes = {'motorway', 'trunk', 'primary', 'secondary'}
roads = []
for way in raw.get('elements', []):
    tags = way.get('tags', {})
    highway = tags.get('highway', '')
    name = tags.get('name', '')
    if not name or not way.get('geometry'):
        continue
    lower = name.lower()
    if highway not in keep_classes and not (highway == 'tertiary' and (tags.get('ref') or any(token in lower for token in keep_local))) and not any(token in lower for token in keep_local):
        continue
    geom = way['geometry']
    lats = [p['lat'] for p in geom]
    lons = [p['lon'] for p in geom]
    if max(lats) < 43.15 or min(lats) > 45.15 or max(lons) < -117.25 or min(lons) > -115.55:
        continue
    points = [[round(p['lat'], 5), round(p['lon'], 5)] for p in geom]
    roads.append({'highway': highway, 'ref': tags.get('ref', ''), 'name': name, 'points': points})

out = Path('/home/ubuntu/idaho-highway-map/client/src/data/roadData.ts')
header = '// Generated from OpenStreetMap Overpass extracts, retrieved 2026-08-13.\n'
out.write_text(header + 'export type Road = { highway: string; ref: string; name: string; points: [number, number][] };\nexport const roads: Road[] = ' + json.dumps(roads, separators=(',', ':')) + ';\n', encoding='utf-8')
print('saved', len(roads), 'roads for four-county extent')
