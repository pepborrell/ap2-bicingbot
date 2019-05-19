from data_v2 import *

d = 1000
G, bicing, info = build_graph(d)

#No creus que podríem evitar fer la bbox cada cop?
#En plan podríem fer la funció get_nodes fora de build graph (així només la faíem un cop)
#i llavors ja per cada d dibuixar els edges.

image = plot_graph(G)
image.save('map.png')

#print(number_of_nodes(G))
#print(number_of_edges(G))
#print(number_of_connected_components(G))
plot_route('Passeig de Gràcia 92, La Rambla 51', G, d, info)

'''
print("xmin, ymin, xmax, ymax in coordinates: ", bbox(G))

'''