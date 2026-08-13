import json
from pathlib import Path
from collections import defaultdict

base = Path('/home/ubuntu/idaho-highway-map/client/src/data')
files = ['osm_corridor_roads.json', 'osm_roads.json', 'osm_emmett_sweet_roads.json']
raw_elements=[]
for filename in files:
    path=base / filename
    if path.exists():
        raw_elements.extend(json.loads(path.read_text()).get('elements', []))

segments = defaultdict(list)
seen=set()
for way in raw_elements:
    tags=way.get('tags', {})
    geometry=way.get('geometry') or []
    if not geometry:
        continue
    points=[[round(p['lat'],5),round(p['lon'],5)] for p in geometry]
    ref=tags.get('ref','')
    name=tags.get('name','')
    if ref == 'ID 16':
        group='id16'
    elif ref == 'ID 52':
        group='id52'
    elif name == 'Sweet Ola Highway':
        group='sweetOla'
    elif name in {'High Valley Road','Cabarton High Valley Road','Third Fork Road','Second Fork Road'}:
        group='existingRoadCandidates'
    elif name in {'Council Cuprum Road','Council Road'}:
        group='adamsCandidate'
    else:
        continue
    signature=(group, name, ref, tuple(map(tuple, points)))
    if signature in seen:
        continue
    seen.add(signature)
    segments[group].append({'name':name or ref or 'OSM road','ref':ref,'highway':tags.get('highway',''),'points':points})

header='// Generated from OpenStreetMap road geometry, retrieved 2026-08-13.\n'
text=header+'export type CorridorSegment = { name: string; ref: string; highway: string; points: [number, number][] };\nexport const corridorSegments: Record<string, CorridorSegment[]> = '+json.dumps(dict(segments),separators=(',',':'))+';\n'
(base/'corridorRoadData.ts').write_text(text,encoding='utf-8')
for key,items in segments.items(): print(key,len(items))
