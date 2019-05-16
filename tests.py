from data import *

G, bicing = get_nodes()
print(number_of_nodes(G))
print(number_of_edges(G))
print(number_of_connected_components(G))
print(bbox(G))
image = plot_graph(G)
image.save('map.png')
