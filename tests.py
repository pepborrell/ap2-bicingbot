from data import get_nodes, number_of_nodes, number_of_edges, plot_graph

G, bicing = get_nodes()
print(number_of_nodes(G))
print(number_of_edges(G))
image = plot_graph(G)
image.save('map.png')
