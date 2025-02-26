import gps
import osmnx as ox
import networkx as nx
import time

# Load the saved Seattle graph
graph_seattle = ox.load_graphml('seattle_graph.graphml')

# Create a GPS session
session = gps.gps("localhost", "2947")
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)

def get_gps_location():
    try:
        report = session.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                return report.lat, report.lon
    except StopIteration:
        pass
    return None
def generate_directions(graph, route):
    directions = []

    for i in range(1, len(route)):
        # Get the start and end nodes of the segment
        start_node = route[i - 1]
        end_node = route[i]
        # Get the edges between start and end nodes
        edge = graph[start_node][end_node]

        if len(route) - 1 is not i:
            next_node = route[i + 1]
            next_edge = graph[end_node][next_node]    
            next_street = next_edge[0].get('name')
        else:
            next_street = "Destination"


        # Look at the direction based on the edge
        # Here, we would use logic to generate turn directions
        directions.append(f"Proceed along {edge[0]['name']} towards {next_street}")

    return directions

def navigate(start_lat, start_lon, end_lat, end_lon):

    # Get the nearest nodes to the start and end locations
    start_node = ox.distance.nearest_nodes(graph_seattle, start_lon, start_lat)
    end_node = ox.distance.nearest_nodes(graph_seattle, end_lon, end_lat)

    # Compute the shortest path between these nodes
    route = nx.shortest_path(graph_seattle, start_node, end_node, weight='length')

    # Plot the route (optional)
    # ox.plot_graph_route(graph_seattle, route, route_linewidth=6, node_size=0, bgcolor='k')

    # Print the route (list of nodes in the path)
    print("Route:", route)

    # Generate directions based on the route
    directions = generate_directions(graph_seattle, route)

    # Print out the directions
    for step in directions:
        print(step)


while True:
    location = get_gps_location()
    if location:
        start_lat, start_lon = location
        print(f"Current location: {start_lat}, {start_lon}")
        
        # Define your destination
        end_lat, end_lon = 47.6205, -122.3493  # Example destination
        
        # Call your navigation function
        navigate(start_lat, start_lon, end_lat, end_lon)
    else:
        print("Waiting for GPS fix...")
    
    time.sleep(5)  # Wait for 5 seconds before the next update
