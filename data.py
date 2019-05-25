import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
import networkx as nx
from staticmap import StaticMap, CircleMarker, Line

'''
Downloads the data from the internet and places the stations in a NetworkX Graph.
Returns the graph, with the index and position in the node's own data and the
DataFrame containing all the downloaded data.
The position data is a tuple of the form (latitude, longitude)
'''
def get_nodes():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    G = nx.Graph()
    for st in bicing.itertuples():
        position = (st.lat, st.lon)
        G.add_node(st.Index, pos=position)
    return G, bicing

'''
Returns the latitude of a node.
'''
def lat (node):
    return node[1]['pos'][0]

'''
Returns the longitude of a node.
'''
def lon (node):
    return node[1]['pos'][1]

'''
To create the edges regarding the maximum distance allowed d, we'll create out of our map
(using its corresponding bounding box) a grid made of little squares of size d^2.
The little squares' location within the grid will be expressed with an identification number starting
from the leftest and highest whose number will be set to 0. Increasing identify numbers will be set
firstly through columns and then through rows.

Therefore, finding the neighbours of a node that satisfy the condition of proximity will have
a linear cost instead of a quadratic one.
'''

'''
Returns the dimensions of the corresponding bounding box of G and the minimum longitude and latitude.
'''
def bbox (G):
    # We initialize the maximums and minimums of longitude and latitude to the first node
    position = G.nodes[1]['pos']
    xmax = xmin = position[0]
    ymax = ymin = position[1]

    for node in list(G.nodes(data=True)):
        x, y = lat(node), lon(node)
        if x > xmax:
            xmax = x
        if x < xmin:
            xmin = x
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y

    return xmin, ymin, xmax, ymax

'''
Returns the square of the grid in which the node is located.
The grid is numbered in the following way:
| 0 | 1 | ... | m-1  |
| . | . | ... | ...  |
| . | . | ... |n*m-1 |
In this way, a node in column x and row y is in the square number y*n + x,
The input node is a NetworkX graph node.
Remember: The haversine function wants the input to be 2 tuples of the form (lat, lon)
'''
def square (node, xmin, ymin, d, n_columns):
    x = haversine ((xmin, lon(node)), node[1]['pos'], unit='m')
    y = haversine ((lat(node), ymin), node[1]['pos'], unit='m')
    column = x // d
    row = y // d
    return int(row*n_columns + column)

'''
Returns a list matching each square with all the nodes within it
'''
def grid (G, d, X):
    xmin, ymin, xmax, ymax = X
    width = haversine ((xmin, ymin), (xmax, ymin), unit='m')
    height = haversine ((xmin, ymin), (xmin, ymax), unit='m')
    print ('width and height of bbox in meters: ', width, height)

    n_columns = int(width // d + 1)
    n_rows = int(height // d + 1)

    nodes_per_square = [[] for i in range(n_columns*n_rows)]
    for node in list(G.nodes(data=True)):
        sq = square (node, xmin, ymin, d, n_columns)
        nodes_per_square[sq].append(node)
    return nodes_per_square, n_columns

'''
Checks wether the possible edges from node obey having a distance < d. 
'''
def check_edge (G, d, node, nodes_per_square, n_square, velocity):
    for n_node in nodes_per_square[n_square]:
        distance = haversine(node[1]['pos'],n_node[1]['pos'], unit='m')
        if (distance < d and n_node != node): #<=?
            G.add_edge(node[0], n_node[0], time=distance/velocity)


'''
Connects the node with the nodes of the minimum necessary squares around it.
That is: checking the same node square and the ones located below, below-right, right, above-right of it
(whenever they exist in the grid).
'''
def neighbours (G, d, node, nodes_per_square, bbox_coords, n_columns, velocity):
    pos_grid = square (node, bbox_coords[0], bbox_coords[1], d, n_columns)
    check_edge(G, d, node, nodes_per_square, pos_grid, velocity)

    if pos_grid%n_columns != n_columns-1:
        check_edge(G, d, node, nodes_per_square, pos_grid + 1, velocity)
    if pos_grid >= n_columns:
        check_edge(G, d, node, nodes_per_square, pos_grid - n_columns, velocity)
        if (pos_grid - n_columns)%n_columns != n_columns-1:
            check_edge(G, d, node, nodes_per_square, pos_grid - n_columns + 1, velocity)
    if pos_grid < len(nodes_per_square) - n_columns:
        if (pos_grid + n_columns)%n_columns != n_columns-1:
            check_edge(G, d, node, nodes_per_square, pos_grid + n_columns + 1, velocity)

'''
Connects the node with all possible nodes within its own square and the resting eight around it.(Whenever they exist in the grid).
Used when adding a new node (origin or destiny from route function definde below).
'''
def neighbours_od (G, d, node, nodes_per_square, bbox_coords, n_columns, velocity):
    pos_grid = square (node, bbox_coords[0], bbox_coords[1], d, n_columns)
    check_edge(G, d, node, nodes_per_square, pos_grid, velocity)

    neighbours (G, d, node, nodes_per_square, bbox_coords, n_columns, velocity)

    if pos_grid%n_columns != 0:
        check_edge(G, d, node, nodes_per_square, pos_grid - 1, velocity)
    if pos_grid >= n_columns and (pos_grid - n_columns)%n_columns != 0:
        check_edge(G, d, node, nodes_per_square, pos_grid - n_columns - 1, velocity)
    if pos_grid < len(nodes_per_square) - n_columns:
        check_edge(G, d, node, nodes_per_square, pos_grid + n_columns, velocity)
        if (pos_grid + n_columns)%n_columns != 0:
            check_edge(G, d, node, nodes_per_square, pos_grid + n_columns - 1, velocity)

'''
Connects the nodes of the graph adding edges which obey the condition (distance < d)
and own a weight value that represents the time needed to go through.
'''
def get_edges(G, d):
    bbox_coords = bbox (G)
    bike_v = 1000 # meters/hour
    nodes_per_square, n_columns = grid (G, d, bbox_coords)
    for node in list(G.nodes(data=True)):
        neighbours (G, d, node, nodes_per_square, bbox_coords, n_columns, bike_v)
    return nodes_per_square, bbox_coords, n_columns

'''
Builds the graph taking into account the specified conditions.
'''
def build_graph(d):
    G, bicing = get_nodes()
    info = get_edges(G, d)
    return G, bicing, info

'''
Returns the number of nodes.
'''
def number_of_nodes(G):
    return G.number_of_nodes()

'''
Returns the number of edges.
'''
def number_of_edges(G):
    return G.number_of_edges()

'''
Returns the number of connected components.
'''
def number_of_connected_components(G):
    return nx.number_connected_components(G)

'''
Plots the graph as a map, using the coordinates of the nodes.
Takes a NetworkX Graph and returns the image
'''
def plot_graph(G):
    city_map = StaticMap(1000, 1000)
    # Plotting nodes
    for node in list(G.nodes(data=True)):
        if node[0] == 'o' or node[0] == 'd':
            marker = CircleMarker(node[1]['pos'][::-1], 'green', 4)
        else:
            marker = CircleMarker(node[1]['pos'][::-1], 'red', 4)
        city_map.add_marker(marker)

    # Plotting edges
    for edge in list(G.edges()):
        if edge[0] == 'o' or edge[0] == 'd' or edge[1] == 'o' or edge[1] == 'd':
            line = Line((G.nodes[edge[0]]['pos'][::-1], G.nodes[edge[1]]['pos'][::-1]), 'black', 1)
        else:
            line = Line((G.nodes[edge[0]]['pos'][::-1], G.nodes[edge[1]]['pos'][::-1]), 'blue', 1)
        city_map.add_line(line)

    image = city_map.render()
    return image

'''
Converts addresses to its corresponding coordinates (latitude, longitude).
'''
def addressesTOcoordinates(addresses):
    '''
    Returns the two coordinates of two addresses of Barcelona
    in a single string separated by a comma. In case of failure, returns None.

    Examples:

    >>> addressesTOcoordinates('Jordi Girona, Plaça de Sant Jaume')
    ((41.3875495, 2.113918), (41.38264975, 2.17699121912479))
    >>> addressesTOcoordinates('Passeig de Gràcia 92, La Rambla 51')
    ((41.3952564, 2.1615724), (41.38082045, 2.17357087674997))
    >>> addressesTOcoordinates('Avinguda de Jordi Cortadella, Carrer de Jordi Petit')
    None
    >>> addressesTOcoordinates('foo')
    None
    >>> addressesTOcoordinates('foo, bar, lol')
    None
    '''
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None

'''
Returns the shortest path in time between two given addresses
taking into account the corresponding velocities when walking or by bike.
'''
def route(G, d, info):
    walk_v = 4000 # meters/hour
    neighbours_od (G, d, ('o', G.nodes['o']), info[0], info[1], info[2], walk_v)
    neighbours_od (G, d, ('d', G.nodes['d']), info[0], info[1], info[2], walk_v)

    path = nx.shortest_path(G, source='o', target='d', weight='time')
    return path

'''
Plots the route that takes the minimum time to go through using the coordinates of the "origin" and "destiny" nodes.
It considers the different velocities of walking or riding a bike to compute the quickest way.
Takes two addresses and returns the image with the route ploted.
'''
def plot_route(addresses, G, d, info):
    coords = addressesTOcoordinates(addresses)
    if coords is None: print("Adreça no trobada")
    else:
        # We add the origin and the destination positions to the graph as two new nodes (taking d into account)
        coord_origen, coord_desti = coords
        G.add_node('o', pos=coord_origen)
        G.add_node('d', pos=coord_desti)

        path = route(G, d, info)

        if path is None:
            return None
        H = nx.path_graph(path)

        for x in list(H.nodes()):
            print (G.nodes[x]['pos'])
            H.nodes[x]['pos'] = G.nodes[x]['pos']

        # We remove them for further calculations
        G.remove_node('o')
        G.remove_node('d')

        return plot_graph(H)
