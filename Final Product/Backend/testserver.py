from bottle import route, run, request, static_file
import json
from threading import Lock

import osmnx as ox
import networkx as nx
import copy
import numpy as np
import sys
import traceback

import googlemaps

@route('/map')
def serve_map():
    return static_file('map.html', root='html')

@route('/route', method='POST')
def serve_route():
    #query = json.loads(request.json)
    query = request.json
    sys.stderr.write('{}\n'.format(query))
    g_graph_lock.acquire()

    try:
        p0 = get_point_from_query(query['start'])
        p1 = get_point_from_query(query['end'])
        return path_from_coords(p0, p1)
    except Exception as exc:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        sys.stderr.write('EXCEPTION CAUGHT:\n{}'.format(''.join(list(
            traceback.format_exception(exc_type, exc_value, exc_traceback)))))
    finally:
        g_graph_lock.release()
    return {'status' : 1}

@route('/js/<filename:path>')
def serve_js(filename):
    return static_file(filename, root='js')

@route('/css/<filename:path>')
def serve_css(filename):
    return static_file(filename, root='css')

def get_point_from_query(q):
    if q['type'] == 'address':
        return geo_coder(q['address'])
    elif q['type'] == 'coordinate':
        return (q['x'], q['y'])
    else:
        raise RuntimeError('pls')

def path_from_coords(p0, p1):
    n0 = ox.get_nearest_node(g_graph, tuple(reversed(p0)))
    n1 = ox.get_nearest_node(g_graph, tuple(reversed(p1)))
    sys.stderr.write('{} {} {} {}\n'.format(p0, p1, n0, n1))
    path = choose_route(g_graph, iterative_dijkstra(g_graph, n0, n1, 3))
    path_geopoints = []
    path_osmids = []
    path_streetnames = []
    for i in range(len(path)-1):
        d = g_graph.edges._adjdict[path[i]][path[i+1]][0]
        if 'geometry' in d:
            new = list(d['geometry'].coords)
            nnew = len(new)
            path_geopoints += new
        else:
            path_geopoints += [
                (g_graph.nodes[path[i]]['x'], g_graph.nodes[path[i]]['y']),
                (g_graph.nodes[path[i+1]]['x'], g_graph.nodes[path[i+1]]['y'])]
            nnew = 2
        path_osmids += [d['osmid']]*nnew
        if 'name' in d:
            path_streetnames += [d['name']]*nnew
        else:
            path_streetnames += ['Unnamed']*nnew
    ret_data = {
        'status' : 0,
        'path' : {
            'coords' : path_geopoints,
            'osmids' : path_osmids,
            'streetnames' : path_streetnames
        }}
    return ret_data

def crime_meansd(g, path):
  """Return the mean and SD of the distance-normalized crime level over the path.
  Helper function for choose_route."""
  vals = []
  for i in range(len(path)-1):
    d = g.edges[path[i],path[i+1],0]
    vals.append(d['crime']/d['length'])
  return np.mean(vals), np.std(vals)

def choose_route(g, paths):
  """Choose the route with a mean crime leven in the bottom 25% that has the lowest SD."""
  crime_levels = [crime_meansd(g, p) for p in paths]
  by_mean = sorted(range(len(paths)), key=lambda i: crime_levels[i][0])
  bottom25p = by_mean[:len(by_mean)//4+1] # close enough
  best = sorted(bottom25p, key=lambda i: crime_levels[i][1])[0]
  return paths[best]

def multi_path(G, shortest_route_length, start_vertex, end_vertex, N):
  """For graph "G," find all possible paths that fit within the length requirement.
  Uses the length of the shortest route found by Djikstra's and a multiplier N to
  determine the maximum valid path length.
  Returns a list of paths."""
  good_paths = []
  multi_path_helper(G, [start_vertex], start_vertex, end_vertex, shortest_route_length*N, good_paths)
  return good_paths

def multi_path_helper(G, route_so_far, current_vertex, end_vertex, max_distance, good_paths):
  """Tree-recursive helper function for multi_path"""
  print(current_vertex, len(route_so_far), len(good_paths))
  route_length = sum(ox.utils.get_route_edge_attributes(G, route_so_far, attribute = "length"))
  if route_length > max_distance:
    return
  if current_vertex == end_vertex:
    good_paths.append(route_so_far)
    return
  for neighbor in list(G.edges._adjdict[current_vertex].keys()):
    if neighbor not in route_so_far:
      multi_path_helper(G, route_so_far + [neighbor], neighbor, end_vertex, max_distance, good_paths)

def iterative_dijkstra(g, a, b, max_depth=3, _depth=1, r=None, h=None, allh=None):
  if _depth == 1:
    r = set()
    allh = set()
    h = tuple()
    g = copy.deepcopy(g)
    try:
    	path = nx.dijkstra_path(g, a, b)
    except nx.NetworkXNoPath:
      pass
    r.add(tuple(path))
    best_len = sum(ox.utils.get_route_edge_attributes(g, path, attribute='length'))
    sys.stderr.write('min dist: {}\n'.format(best_len))
    g = ox.truncate_graph_dist(g, a, best_len+0.5)
  else:
    try:
    	path = nx.dijkstra_path(g, a, b)
    except nx.NetworkXNoPath:
      return
  r.add(tuple(path))
  if len(path) < 3:
    r.add(tuple(path))
    return
  if _depth == max_depth:
    if _depth == 1:
      return list(r)
    return
  for n in path[1:-1]:
    h2 = tuple(sorted(h+(n,)))
    if h2 in allh:
      continue
    allh.add(h2)

    node_data = g.nodes[n]
    edges_data = g.edges._adjdict[n]
    g.remove_node(n)

    iterative_dijkstra(g, a, b, max_depth, _depth+1, r, h2, allh)

    g.add_node(n, **node_data)
    for n2 in edges_data:
      g.add_edge(n, n2, **edges_data[n2][0])
      g.add_edge(n2, n, **edges_data[n2][0])
  if _depth == 1:
    return list(r)

def geo_coder(address):
  """A function that takes an address and returns the geocoded [lat,lng] as a list."""
  gmaps = googlemaps.Client("AIzaSyCyj7RlD7CmPzHKZRiUSICcY6ldxIDH39A")
  l = gmaps.geocode(address)[0]['geometry']['location']
  return l['lng'], l['lat']

g_graph = nx.read_gpickle('data/city-crime.gpickle')
g_graph_lock = Lock()



if __name__ == '__main__':
    run(host='localhost', port=8080)
