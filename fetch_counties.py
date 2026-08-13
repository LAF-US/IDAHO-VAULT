import json
import requests
query = '''[out:json][timeout:60];relation[boundary=administrative][admin_level=6][name~"^(Gem|Adams|Valley) County$"](43.45,-116.85,44.60,-115.95);out geom;'''
for endpoint in ['https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter']:
    try:
        response = requests.get(endpoint, params={'data': query}, headers={'User-Agent':'idaho-highway-map-research/1.0'}, timeout=75)
        response.raise_for_status()
        data = response.json()
        with open('/home/ubuntu/idaho-highway-map/osm_counties.json','w',encoding='utf-8') as handle:
            json.dump(data, handle)
        print('saved', len(data.get('elements',[])), 'county relations from', endpoint)
        break
    except Exception as error:
        print('endpoint failed:', endpoint, error)
else:
    raise SystemExit('all endpoints failed')
