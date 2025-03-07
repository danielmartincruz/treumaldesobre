import networkx as nx
import folium
from geopy.distance import geodesic
import numpy as np

# Sample data: Points, Roads, and Intersections
points = {
    "Reception": (41.8366780, 3.0872467),
    "Bungalow 75": (41.835968, 3.087096)
}

roads = [
    [(41.8367279, 3.0871287), (41.836358, 3.087034)],  # Road 1
    [(41.836358, 3.087034), (41.8362543, 3.0870697)],  # Road 2
    [(41.8362543, 3.0870697), (41.8357347, 3.0869409)]  # Road 3
]

# Step 1: Build the graph with roads as nodes and edges
graph = nx.Graph()
for road in roads:
    for i in range(len(road) - 1):
        graph.add_edge(road[i], road[i + 1], weight=geodesic(road[i], road[i + 1]).meters)

# Step 2: Calculate closest point on a line (using line formula)
def closest_point_on_line(p, a, b):
    # Convert lat/lon to numpy arrays for easier math
    p, a, b = np.array(p), np.array(a), np.array(b)
    
    # Line formula projection: Closest point calculation
    ap = p - a
    ab = b - a
    t = np.dot(ap, ab) / np.dot(ab, ab)
    t = max(0, min(1, t))  # Ensure the closest point is within the segment

    return tuple(a + t * ab)

# Step 3: Find the closest trimmed road points and add them to the graph
def find_trimmed_road(point, roads):
    closest_road = None
    closest_point = None
    min_distance = float('inf')

    for road in roads:
        for i in range(len(road) - 1):
            a, b = road[i], road[i + 1]
            closest = closest_point_on_line(point, a, b)
            distance = geodesic(point, closest).meters
            if distance < min_distance:
                min_distance = distance
                closest_point = closest
                closest_road = (a, closest) if distance < geodesic(a, closest).meters else (closest, b)

    # Add closest point as a new node to the graph
    graph.add_node(closest_point)
    graph.add_edge(closest_road[0], closest_point, weight=geodesic(closest_road[0], closest_point).meters)
    graph.add_edge(closest_point, closest_road[1], weight=geodesic(closest_point, closest_road[1]).meters)

    return closest_road, closest_point

nearest_to_A, trimmed_road_A = find_trimmed_road(points["Reception"], roads)
nearest_to_B, trimmed_road_B = find_trimmed_road(points["Bungalow 75"], roads)

# Step 4: Find the optimal path between the selected road points
path = nx.shortest_path(graph, source=trimmed_road_A, target=trimmed_road_B, weight="weight")

# Step 5: Draw the map
m = folium.Map(location=points["Reception"], zoom_start=17)

# Mark points A and B
folium.Marker(points["Reception"], popup="Reception", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(points["Bungalow 75"], popup="Bungalow 75", icon=folium.Icon(color="red")).add_to(m)

# Highlight the roads except the trimmed segments
for road in roads:
    if not (road[0] == nearest_to_A[0] or road[0] == nearest_to_B[0]):
        folium.PolyLine(road, color="blue", weight=3, opacity=0.7).add_to(m)

# Draw trimmed segments
folium.PolyLine([nearest_to_A[0], trimmed_road_A], color="blue", weight=3, opacity=0.7).add_to(m)
folium.PolyLine([trimmed_road_B, nearest_to_B[1]], color="blue", weight=3, opacity=0.7).add_to(m)

# Highlight the selected trimmed path
folium.PolyLine(path, color="red", weight=4, opacity=0.9).add_to(m)

# Show the map
m.save("mock_route_map.html")
print("✅ Mock route map created as 'mock_route_map.html'")