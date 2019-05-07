import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
import networkx as nx
from staticmap import StaticMap, CircleMarker, Line

def get_nodes():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    G = nx.Graph()
    for st in bicing.itertuples():
        position = (st.lon, st.lat)
        G.add_node(st.Index, pos=position)
    return G

def number_of_nodes(G):
    return G.number_of_nodes()

def number_of_edges(G):
    return G.number_of_edges()

def plot_graph(G):
    m_bcn = StaticMap(800, 800)
    for node in list(G.nodes(data=True)):
        marker = CircleMarker(node[1]['pos'], 'red', 4)
        m_bcn.add_marker(marker)
    for edge in list(G.edges()):
        line = Line(coords, 'blue', 3)
        m_bcn.add_line(line)
    image = m_bcn.render()
    return image
