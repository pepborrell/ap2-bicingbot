from data import *

d = 500
G, bicing, info = build_graph(d)
print (bicing)

#No creus que podríem evitar fer la bbox cada cop?
#En plan podríem fer la funció get_nodes fora de build graph (així només la faíem un cop)
#i llavors ja per cada d dibuixar els edges.

image = plot_graph(G)
image.save('map.png')

#print(number_of_nodes(G))
#print(number_of_edges(G))
#print(number_of_connected_components(G))
image2 = plot_route('Rambla del Raval 13, Provença 501', G, d, info)
image2.save('route.png')

'''
print("xmin, ymin, xmax, ymax in coordinates: ", bbox(G))

'''