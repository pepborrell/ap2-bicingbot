from data_v2 import *

d = 1000
G, bicing, info = build_graph(d)
image = plot_graph(G)
image.save('map.png')

#print(number_of_nodes(G))
#print(number_of_edges(G))
#print(number_of_connected_components(G))

# print(G.edges)

plot_route('Passeig de Gràcia 92, La Rambla 51', G, d, info)

'''
print("xmin, ymin, xmax, ymax in coordinates: ", bbox(G))

'''
