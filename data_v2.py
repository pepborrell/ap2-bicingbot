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
        G.add_node(st.Index, pos=position) ##No hauria de ser index en minúscula?
    return G, bicing

'''
To create the edges regarding the maximum distance allowed d, we'll create out of our map
(using its corresponding bounding box) a grid made of little squares of size d^2.
The origin will correspond to the left-down side of the bounding box with increasing x's to the right
and increasing y's above.
Likewise, the little squares' location within the grid will be expressed like a Matrix.
The leftest and lowest square will have coordinates (x,y) = (0,0).

##Shall we start at 1 like in Python????

Therefore, finding the neighbours of a node that satisfy the condition of proximity will have
a linear cost instead of a quadratic one.
'''

#Returns the latitude of a node.
def lat (node):
    return node[1]['pos'][0]

#Returns the longitude of a node.
def lon (node):
    return node[1]['pos'][1]
'''
Returns the dimensions of the corresponding bounding box of G and the minimum longitude and latitude.
'''
def bbox (G):
    # We initialize the maximums and minimums of longitude and latitude to the first node
    position = G.nodes[0]['pos']
    xmax = xmin = position[0] # No sé com fer-ho per només haver d'accedir al 1er node. Així millor?
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
def square (node, xmin, ymin, d, n):
    x = haversine ((xmin, lon(node)), node[1]['pos'], unit='m')
    y = haversine ((lat(node), ymin), node[1]['pos'], unit='m')
    column = x // d #+1 if we started at (1,1) (see comment above)
    row = y // d #+1
    return y*n + x

'''
Returns a map matching each square with all the nodes within it
'''
def grid (G, d):
    xmin, ymin, xmax, ymax = bbox (G)
    width = haversine ((xmin, ymin), (xmax, ymin), unit='m')
    height = haversine ((xmin, ymin), (xmin, ymax), unit='m')
    print ('width and height of bbox in meters: ', width, height)

    n_columns = width // d + 1
    n_rows = height // d #+1

    nodes_per_square = {}
    for node in list(G.nodes(data=True)):
        square = square (node, xmin, ymin, d, n_rows)
        nodes_per_square[square].append(node)
    return nodes_per_square


##en funció de d
##incloure ja els pesos en cada cas entre estacions (distancia/velocitat = temps)
def get_edges(G, d, how):
    ##bbox i map amb quadrat de la quadricula i llista de nodes a dins
    for node in list(G.nodes(data=True)):
        square = square(node)
        """
        for neighbour in ##square del mapa
            G.add_edge()
        """
    return G

def number_of_nodes(G):
    return G.number_of_nodes()

def number_of_edges(G):
    return G.number_of_edges()

def number_of_connected_components(G):
    return nx.number_connected_components(G)


'''
Plots the graph as a map, using the coordinates of the nodes.
Takes a NetworkX Graph and returns the image
'''
def plot_graph(G):
    map = StaticMap(800, 800)
    # Plotting nodes
    for node in list(G.nodes(data=True)):
        marker = CircleMarker(node[1]['pos'], 'red', 4) ##Perquè poses ['pos'] si node[1] ja és la posició?
        map.add_marker(marker)
    # Plotting edges
    for edge in list(G.edges()):
        line = Line(G.nodes[edge[0]]['pos'], G.nodes[edge[1]]['pos'], 'blue', 3)
        map.add_line(line)
    image = map.render()
    return image

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

def route(addresses, G):
    '''
    Returns the shortest path in time between two given addresses
    taking into account the corresponding velocities when walking or by bike.
    '''
    coords = addressesTOcoordinates(addresses)
    if coords is None: print("Adreça no trobada")
    else:
        # Adding 2 nodes to the graph (taking d into account)
        coord_origen, coord_desti = coords
        G.add_node('o', pos=coord_origen)
        G.add_node('d', pos=coord_desti)

        #for funcio < d, add edge amb pes el que sigui (inclos a la funcio)
        ## min cami

        ##esborrar nodes del graf
        G.remove_node('o')
        G.remove_node('d')
