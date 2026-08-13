import json
from pathlib import Path
import requests

bbox = '(43.80,-116.60,44.05,-116.25)'
query = f'''[out:json][timeout:90];way[highway][name]{bbox};out tags geom;'''
for endpoint in ['https://overpass.private.coffee/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']:
    try:
        response = requests.get(endpoint, params={'data': query}, headers={'User-Agent':'idaho-highway-map-research/1.0'}, timeout=120)
        response.raise_for_status()
        data = response.json()
        break
    except Exception as error:
        print('failed', endpoint, error)
else:
    raise SystemExit('all endpoints failed')
Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_emmett_sweet_roads.json').write_text(json.dumps(data), encoding='utf-8')
seen = set()
for way in data.get('elements', []):
    tags = way.get('tags', {})
    name = tags.get('name','')
    if name not in seen:
        seen.add(name)
        print(name, '|', tags.get('ref',''), '|', tags.get('highway',''))
print('saved', len(data.get('elements', [])), 'ways')
