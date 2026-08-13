import json
from pathlib import Path
import requests

bbox = '(43.35,-117.25,44.9,-115.75)'
query = f'''[out:json][timeout:120];(
  way[ref="ID 16"]{bbox};
  way[ref="I 84"]{bbox};
  way[name="Sweet Ola Highway"]{bbox};
  way[name="High Valley Road"]{bbox};
  way[name="Cabarton High Valley Road"]{bbox};
  way[name="Council Cuprum Road"]{bbox};
  way[name="Council Road"]{bbox};
  way[name="Emmett Road"]{bbox};
);out tags geom;'''
endpoints = ['https://overpass.private.coffee/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']
for endpoint in endpoints:
    try:
        response = requests.get(endpoint, params={'data': query}, headers={'User-Agent': 'idaho-highway-map-research/1.0'}, timeout=180)
        response.raise_for_status()
        data = response.json()
        break
    except Exception as error:
        print('endpoint failed:', endpoint, error)
else:
    raise SystemExit('all endpoints failed')

out = Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_corridor_roads.json')
out.write_text(json.dumps(data), encoding='utf-8')
from collections import Counter
summary = Counter((e.get('tags', {}).get('name', ''), e.get('tags', {}).get('ref', ''), e.get('tags', {}).get('highway', '')) for e in data.get('elements', []))
print('saved', len(data.get('elements', [])), 'road ways')
for item, count in sorted(summary.items()):
    print(count, item)
