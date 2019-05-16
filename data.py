import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
import networkx as nx
from staticmap import StaticMap, CircleMarker, Line

"""
Downloads the data from the internet and places the stations in a NetworkX Graph.
Returns the graph, with the index and position in the node's own data and the
DataFrame containing all the downloaded data.
The position data is a tuple of the form (longitude, latitude)
"""
def get_nodes():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    G = nx.Graph()
    for st in bicing.itertuples():
        position = (st.lon, st.lat)
        G.add_node(st.Index, pos=position) ##No hauria de ser index en minúscula?
    return G, bicing

"""
To create the edges regarding the maximum distance allowed d, we'll create out of our map 
(using its corresponding bounding box) a grid made of little squares of size d^2.
Therefore, finding the neighbours of a node that satisfy the condition of proximity will have
a linear cost instead of a quadratic one.
"""

#Returns the dimensions of the corresponding bounding box of G and the minimum longitude and latitude.
def bbox (G):
    #nodes_periphery = periphery(G, e=None, usebounds=False) #Returns a list of nodes in the periphery of the graph
    #for node in nodes_periphery: ##no sé si és necessari fer: list(periphery)
    #O BÉ:

    for node in list(G.nodes(data=True)):
        xmax, xmin, ymax, ymin = 0, 0, 0, 0
        x = node[1]['pos'][0]
        y = node[1]['pos'][1]
        if x > xmax:
            xmax = x
        if x < xmin:
            xmin = x
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y
    

    width = xmax - xmin
    height = ymax - ymin

    return width, height, xmin, ymin

#Returns a map matching each square with all the nodes within it
def grid (G):
    width, height, xmin, ymin= bbox (G)


# Returns in which square of the grid the node is located
def square (G, node):
    return 
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


"""
Plots the graph as a map, using the coordinates of the nodes.
Takes a NetworkX Graph and returns the image
"""

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
    Returns the most shortest path in time between two given addresses
    taking into account the corresponding velocities when walking or by bike.
    '''

    coords = addressesTOcoordinates(addresses)
    if coords is None: print("Adreça no trobada")
    else:
        ##afegir 2 nodes al graf (tenint en compte d)
        coord_origen, coord_desti = coords
        G.add_node('o', pos=coord_origen)
        G.add_node('d', pos=coord_desti)
        
        #for funcio < d, add edge amb pes el que sigui (inclos a la funcio)
        ## min cami

        ##esborrar nodes del graf
        G.remove_node('o')
        G.remove_node('d')
