from data import *

d = 600
G, stations, info = build_graph(d)

'''
image = plot_graph(G)
image.save('map.png')
'''

distribute(G, d, 0, 0)

#print(number_of_nodes(G))
#print(number_of_edges(G))
#print(number_of_connected_components(G))

'''
image2 = plot_route('Rambla del Raval 13, Provença 501', G, d, info)
image2.save('route.png')
'''
'''
print("xmin, ymin, xmax, ymax in coordinates: ", bbox(G))
'''
