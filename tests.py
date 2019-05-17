from data_v2 import *

G, info = build_graph(1000)
print(number_of_nodes(G))
print(number_of_edges(G))
print(number_of_connected_components(G))

# print(G.edges)

plot_route('Tibidabo', 'Pl. Catalunya', G, 1000)

'''
print("xmin, ymin, xmax, ymax in coordinates: ", bbox(G))
image = plot_graph(G)
image.save('map.png')
'''
