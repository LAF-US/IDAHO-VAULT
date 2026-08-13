import heapq
import json
import math
from pathlib import Path
from collections import defaultdict

base = Path('/home/ubuntu/idaho-highway-map/client/src/data')
raw = json.loads((base / 'osm_roads.json').read_text())

def key(point):
    return (round(point[0], 4), round(point[1], 4))

def distance(a, b):
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    x = (lon2 - lon1) * math.cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    return 6371000 * math.sqrt(x*x + y*y)

graph = defaultdict(list)
edge_geometry = {}
all_points = set()
for way in raw.get('elements', []):
    geometry = way.get('geometry') or []
    if len(geometry) < 2:
        continue
    points = [key((p['lat'], p['lon'])) for p in geometry]
    for a, b in zip(points, points[1:]):
        if a == b:
            continue
        weight = distance(a, b)
        graph[a].append((b, weight))
        graph[b].append((a, weight))
        edge_geometry[(a, b)] = [a, b]
        edge_geometry[(b, a)] = [b, a]
        all_points.add(a); all_points.add(b)

start = key((44.18073, -116.29248))
target = key((44.72989, -116.43820))

def nearest(point):
    return min(all_points, key=lambda candidate: distance(point, candidate))

start_node = nearest(start)
target_node = nearest(target)
print('start node', start_node, 'target node', target_node)

queue = [(0.0, start_node)]
dist = {start_node: 0.0}
prev = {}
while queue:
    cost, node = heapq.heappop(queue)
    if cost != dist.get(node):
        continue
    if node == target_node:
        break
    for nxt, weight in graph.get(node, []):
        new_cost = cost + weight
        if new_cost < dist.get(nxt, float('inf')):
            dist[nxt] = new_cost
            prev[nxt] = node
            heapq.heappush(queue, (new_cost, nxt))

if target_node not in dist:
    raise SystemExit('no route found')

nodes=[]
node=target_node
while node != start_node:
    nodes.append(node)
    node=prev[node]
nodes.append(start_node)
nodes.reverse()

# retain the exact path geometry, with duplicate consecutive vertices removed
points=[]
for node in nodes:
    if not points or points[-1] != list(node):
        points.append(list(node))

out = {
    'name': 'Ola to Council existing OSM network trace',
    'start': list(start_node),
    'end': list(target_node),
    'distance_m': round(dist[target_node]),
    'points': points,
}
(base / 'corridorNetworkTrace.ts').write_text('// Generated from OpenStreetMap road-network geometry.\nexport const corridorNetworkTrace = ' + json.dumps(out, separators=(',', ':')) + ' as const;\n', encoding='utf-8')
print('route distance m', round(dist[target_node]), 'vertices', len(points))
