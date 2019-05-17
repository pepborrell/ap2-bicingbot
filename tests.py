from data_v2 import *

G = build_graph(1000)
print(number_of_nodes(G))
print(number_of_edges(G))
print(number_of_connected_components(G))

print("xmin, ymin, xmax, ymax in coordinates: ", bbox(G))
grid (G, 1000)
image = plot_graph(G)
image.save('map.png')
