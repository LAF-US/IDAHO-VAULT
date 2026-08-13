import json
from pathlib import Path
import requests

boxes = {
    'south': '(44.25,-116.22,44.48,-115.9)',
    'north': '(44.45,-116.75,44.95,-116.15)',
}
all_elements=[]
for label, bbox in boxes.items():
    query = f'''[out:json][timeout:120];way[highway][name]{bbox};out tags geom;'''
    for endpoint in ['https://overpass.private.coffee/api/interpreter', 'https://overpass.kumi.systems/api/interpreter']:
        try:
            response = requests.get(endpoint, params={'data': query}, headers={'User-Agent': 'idaho-highway-map-research/1.0'}, timeout=180)
            response.raise_for_status()
            data = response.json()
            all_elements.extend(data.get('elements', []))
            print(label, len(data.get('elements', [])), 'ways from', endpoint)
            break
        except Exception as error:
            print(label, 'endpoint failed:', endpoint, error)
    else:
        raise SystemExit(f'all endpoints failed for {label}')

Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_northern_named_roads.json').write_text(json.dumps({'elements': all_elements}), encoding='utf-8')
print('saved', len(all_elements), 'named ways')
