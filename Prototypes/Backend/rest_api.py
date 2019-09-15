from flask import Flask, render_template, request, send_file
import osmnx as ox
import networkx as nx
import pandas as pd
import csv
import matplotlib.pyplot as plt

instance = Flask(__name__, template_folder="templates")

@instance.route('/')
def home():
    return render_template('home.html')

def check_if_is_in(target_list, u, v):
    for i in range(len(target_list)):
        try:
            if u==target_list[i] and v==target_list[i+1]:
                return True
        except IndexError:
            break
    return False

@instance.route('/get_map')
def get_image():
    if request.args.get('type') == '1':
        filename = 'smallest_danger_sample.png'
    else:
        filename = 'smallest_danger_sample.png'
    return send_file(filename, mimetype='image/png')


if __name__ == '__main__':
    graph = ox.graph_from_place('Berkeley, Alameda County, California, USA')
    fig, ax = ox.plot_graph(graph)
    nodes, edges = ox.graph_to_gdfs(graph)
    df = nx.from_pandas_edgelist(edges, source='u', target='v', edge_attr=True)
    edges['Crime'] = 0
    crime = pd.read_csv('crime.csv')
    crime_list = crime['Block_Location'].tolist()
    crime_list_coords = []
    for adr in crime_list:
        try:
            cut = adr[adr.index('(') + 1:]
            x = float(cut[:cut.index(',')])
            y = float(cut[cut.index(',') + 2: cut.index(')')])
            crime_list_coords.append((x, y))
        except ValueError:
            pass
    list_of_edges = edges['geometry'].tolist()
    with open('crime_berk.csv', 'r') as f:
        reader = csv.reader(f)
        crime_nodes = list(reader)

    for i in range(edges.shape[0]):
        print(str(i) + ' out of ' + str(edges.shape[0]))
        for j in range(len(crime_nodes)):
            original = crime_nodes[j][0]
            cut = original[original.index(',') + 2:]
            try:
                if edges.at[i, 'u'] == int(cut[:cut.index(',')]) and edges.at[i, 'v'] == int(cut[cut.index(',') + 2:
                cut.index(')')]):
                    edges.at[i, 'Crime'] = edges.at[i, 'Crime'] + 1
            except:
                pass
    df_new = nx.from_pandas_edgelist(edges, source='u', target='v', edge_attr=True)
    shortest_path_distance = nx.dijkstra_path(df, source=1762740812, target=4927326194, weight='Crime')
    ec = ['r' if (check_if_is_in(shortest_path_distance, u, v)) else 'b' for u, v, k in graph.edges(keys=True)]
    fig, ax = ox.plot_graph(graph, node_color='w', node_edgecolor='k', node_size=1, node_zorder=0, edge_color=ec,
                            edge_linewidth=1)
    ox.footprints.plot_footprints(graph, fig=fig, ax=ax, filename='smallest_danger_sample.png', file_format='png',
                                  )


    instance.run(debug=True)
