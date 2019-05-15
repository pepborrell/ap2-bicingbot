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
        G.add_node(st.Index, pos=position)
    return G, bicing


##def get_edges():
    ##en funció de d
    ##incloure ja els pesos en cada cas entre estacions (distancia/velocitat = temps)

def number_of_nodes(G):
    return G.number_of_nodes()

def number_of_edges(G):
    return G.number_of_edges()

def number_of_connected_components(G):
    return #G.number_connected_components()


"""
Plots the graph as a map, using the coordinates of the nodes.
Takes a NetworkX Graph and returns the image
"""

def plot_graph(G):
    map = StaticMap(800, 800)
    # Plotting nodes
    for node in list(G.nodes(data=True)):
        marker = CircleMarker(node[1]['pos'], 'red', 4)
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
        G.add_node(st.Index, pos=coord_origen)
        G.add_node(st.Index, pos=coord_desti)
        #for within_distance()

        ##esborrar nodes del graf

