from data import *

G, bicing = get_nodes()
print(number_of_nodes(G))
print(number_of_edges(G))
print(number_of_connected_components(G))

print("xmin, ymin, xmax, ymax in coordinates: ", bbox(G))
grid (G, 1000)
image = plot_graph(G)
image.save('map.png')
