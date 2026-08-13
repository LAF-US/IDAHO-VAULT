import json
from pathlib import Path

base = Path('/home/ubuntu/idaho-highway-map/client/src/data')

with (base / 'osm_counties.json').open(encoding='utf-8') as handle:
    county_raw = json.load(handle)
counties = []
for relation in county_raw.get('elements', []):
    name = relation.get('tags', {}).get('name', '')
    segments = []
    for member in relation.get('members', []):
        if member.get('type') == 'way' and member.get('geometry'):
            points = [[round(p['lat'], 5), round(p['lon'], 5)] for p in member['geometry']]
            segments.append({'role': member.get('role', ''), 'points': points})
    counties.append({'name': name, 'segments': segments})

with (base / 'osm_roads.json').open(encoding='utf-8') as handle:
    road_raw = json.load(handle)
roads = []
keep_local = ('sweet', 'ola', 'high valley', 'cabarton', 'council', 'emmett', 'horseshoe bend', 'gem', 'adams', 'ada', 'pioneer', 'idaho city')
keep_classes = {'motorway', 'trunk', 'primary', 'secondary', 'tertiary'}
for way in road_raw.get('elements', []):
    tags = way.get('tags', {})
    highway = tags.get('highway', '')
    name = tags.get('name', '')
    if not name or not way.get('geometry'):
        continue
    if highway not in keep_classes and not any(token in name.lower() for token in keep_local):
        continue
    geom = way['geometry']
    lats = [p['lat'] for p in geom]
    lons = [p['lon'] for p in geom]
    if max(lats) < 43.15 or min(lats) > 44.85 or max(lons) < -117.05 or min(lons) > -115.65:
        continue
    points = [[round(p['lat'], 5), round(p['lon'], 5)] for p in geom]
    roads.append({'highway': highway, 'ref': tags.get('ref', ''), 'name': name, 'points': points})

with (base / 'osm_places.json').open(encoding='utf-8') as handle:
    place_raw = json.load(handle)
places = []
for node in place_raw.get('elements', []):
    tags = node.get('tags', {})
    name = tags.get('name')
    if not name or 'lat' not in node or 'lon' not in node:
        continue
    places.append({'name': name, 'place': tags.get('place', ''), 'position': [round(node['lat'], 5), round(node['lon'], 5)]})

header = '// Generated from OpenStreetMap Overpass extracts, retrieved 2026-08-13.\n'
(base / 'countyData.ts').write_text(header + 'export type CountySegment = { role: string; points: [number, number][] };\nexport type County = { name: string; segments: CountySegment[] };\nexport const counties: County[] = ' + json.dumps(counties, separators=(',', ':')) + ';\n', encoding='utf-8')
(base / 'roadData.ts').write_text(header + 'export type Road = { highway: string; ref: string; name: string; points: [number, number][] };\nexport const roads: Road[] = ' + json.dumps(roads, separators=(',', ':')) + ';\n', encoding='utf-8')
(base / 'placeData.ts').write_text(header + 'export type Place = { name: string; place: string; position: [number, number] };\nexport const places: Place[] = ' + json.dumps(places, separators=(',', ':')) + ';\n', encoding='utf-8')
print('counties', len(counties), 'roads', len(roads), 'places', len(places))
