import json
from pathlib import Path
import requests

bbox = '(43.15,-117.25,45.15,-115.55)'
query = f'''[out:json][timeout:120];way[highway~"motorway|trunk|primary|secondary"][name]{bbox};out tags geom;'''
endpoint = 'https://overpass.private.coffee/api/interpreter'
response = requests.get(endpoint, params={'data': query}, headers={'User-Agent': 'idaho-highway-map-research/1.0'}, timeout=180)
response.raise_for_status()
raw = response.json()

roads = []
for way in raw.get('elements', []):
    tags = way.get('tags', {})
    highway = tags.get('highway', '')
    name = tags.get('name', '')
    if not name or not way.get('geometry'):
        continue
    geom = way['geometry']
    points = [[round(p['lat'], 5), round(p['lon'], 5)] for p in geom]
    roads.append({'highway': highway, 'ref': tags.get('ref', ''), 'name': name, 'points': points})

out = Path('/home/ubuntu/idaho-highway-map/client/src/data/roadData.ts')
header = '// Generated from OpenStreetMap Overpass extracts, retrieved 2026-08-13.\n'
out.write_text(header + 'export type Road = { highway: string; ref: string; name: string; points: [number, number][] };\nexport const roads: Road[] = ' + json.dumps(roads, separators=(',', ':')) + ';\n', encoding='utf-8')
print('saved', len(roads), 'major roads for four-county extent')
