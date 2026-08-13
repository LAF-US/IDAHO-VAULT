import json
from pathlib import Path
import requests

bbox = '(43.35,-117.05,45.05,-115.75)'
query = f'''[out:json][timeout:90];way[highway~"motorway|trunk|primary|secondary"][name]{bbox};out tags geom;'''
for endpoint in ['https://overpass.kumi.systems/api/interpreter', 'https://overpass.private.coffee/api/interpreter']:
    try:
        response = requests.get(endpoint, params={'data': query}, headers={'User-Agent': 'idaho-highway-map-research/1.0'}, timeout=120)
        response.raise_for_status()
        raw = response.json()
        break
    except Exception as error:
        print('endpoint failed:', endpoint, error)
else:
    raise SystemExit('all endpoints failed')

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
