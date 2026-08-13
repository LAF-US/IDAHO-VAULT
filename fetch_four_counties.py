import json
from pathlib import Path
import requests

query = '''[out:json][timeout:60];relation[boundary=administrative][admin_level=6][name~"^(Ada|Gem|Adams|Washington) County$"](43.15,-117.25,45.15,-115.55);out geom;'''
endpoint = 'https://overpass.private.coffee/api/interpreter'
response = requests.get(endpoint, params={'data': query}, headers={'User-Agent': 'idaho-highway-map-research/1.0'}, timeout=90)
response.raise_for_status()
data = response.json()

counties = []
for relation in data.get('elements', []):
    name = relation.get('tags', {}).get('name', '')
    segments = []
    for member in relation.get('members', []):
        if member.get('type') == 'way' and member.get('geometry'):
            points = [[round(p['lat'], 5), round(p['lon'], 5)] for p in member['geometry']]
            segments.append({'role': member.get('role', ''), 'points': points})
    counties.append({'name': name, 'segments': segments})

out = Path('/home/ubuntu/idaho-highway-map/client/src/data/countyData.ts')
header = '// Generated from OpenStreetMap Overpass extracts, retrieved 2026-08-13.\n'
out.write_text(header + 'export type CountySegment = { role: string; points: [number, number][] };\nexport type County = { name: string; segments: CountySegment[] };\nexport const counties: County[] = ' + json.dumps(counties, separators=(',', ':')) + ';\n', encoding='utf-8')
print('saved', len(counties), 'counties including Washington County')
