import json
from pathlib import Path
keep = {'Third Fork Road','Second Fork Road','West Mountain Road','Warm Lake Road','Pine Creek Road','Sage Hen Reservoir Road','Cabarton High Valley Road','High Valley Road'}
raw = json.loads(Path('/home/ubuntu/idaho-highway-map/client/src/data/osm_roads.json').read_text())
for way in raw.get('elements', []):
    tags=way.get('tags',{})
    if tags.get('name') not in keep or not way.get('geometry'):
        continue
    pts=[(round(p['lat'],5),round(p['lon'],5)) for p in way['geometry']]
    print(tags.get('name'), '|', tags.get('highway'), '|', 'start', pts[0], 'end', pts[-1], '|', 'n',len(pts))
