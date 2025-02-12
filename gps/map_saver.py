import osmnx as ox

# Define the place for Seattle
place_name = "Seattle, Washington, USA"

# Download the graph for Seattle (street network)
graph_seattle = ox.graph_from_place(place_name, network_type='drive')

# Save the graph to a file (GraphML format)
ox.save_graphml(graph_seattle, 'seattle_graph.graphml')

print("Seattle graph has been saved successfully!")

