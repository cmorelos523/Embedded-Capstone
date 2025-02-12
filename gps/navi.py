import osmnx as ox
import networkx as nx

# Load the saved Seattle graph
graph_seattle = ox.load_graphml('seattle_graph.graphml')

# Define start and end coordinates (latitude, longitude)
start_lat, start_lon = 47.6097, -122.3331  # Example: Downtown Seattle
end_lat, end_lon = 47.6205, -122.3493    # Example: Another location in Seattle

# Get the nearest nodes to the start and end locations
start_node = ox.distance.nearest_nodes(graph_seattle, start_lon, start_lat)
end_node = ox.distance.nearest_nodes(graph_seattle, end_lon, end_lat)

# Compute the shortest path between these nodes
route = nx.shortest_path(graph_seattle, start_node, end_node, weight='length')

# Plot the route (optional)
ox.plot_graph_route(graph_seattle, route, route_linewidth=6, node_size=0, bgcolor='k')

# Print the route (list of nodes in the path)
print("Route:", route)


def generate_directions(graph, route):
    directions = []

    for i in range(1, len(route)):
        # Get the start and end nodes of the segment
        start_node = route[i - 1]
        end_node = route[i]

        # Get the edges between start and end nodes
        edge = graph[start_node][end_node]

        # Look at the direction based on the edge
        # Here, we would use logic to generate turn directions
        directions.append(f"Proceed along {edge[0]['name']} towards {end_node}")

    return directions

# Generate directions based on the route
directions = generate_directions(graph_seattle, route)

# Print out the directions
for step in directions:
    print(step)
