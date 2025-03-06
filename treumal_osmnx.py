import csv
import folium
import os
import networkx as nx

# Define paths
DATA_PATH = "data"
ROUTES_PATH = "routes"
IMAGES_PATH = os.path.join(ROUTES_PATH, "images")
DB_NAME = "camping_data.csv"
MAP_NAME = "route_map.html"
DB_FILENAME = os.path.join(DATA_PATH, DB_NAME)
MAP_FILENAME = os.path.join(ROUTES_PATH, MAP_NAME)

# Ensure the routes directory exists
os.makedirs(ROUTES_PATH, exist_ok=True)

def load_camping_data():
    """Load camping data (points and roads) from CSV."""
    points, roads = {}, []
    graph = nx.Graph()
    
    with open(DB_FILENAME, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row["source"] == "road":
                waypoints = []
                for i in range(1, 10):  # Dynamic waypoints
                    lat_key = f"lat_{i}"
                    lon_key = f"lon_{i}"
                    if lat_key in row and lon_key in row and row[lat_key] and row[lon_key]:
                        waypoints.append((float(row[lat_key]), float(row[lon_key])))
                
                if len(waypoints) >= 2:
                    roads.append({"name": row["name"], "points": waypoints, "road_direction": row["road_direction"]})
                    for j in range(len(waypoints) - 1):
                        graph.add_edge(waypoints[j], waypoints[j+1], weight=1)
            else:
                if row["latitude"] and row["longitude"]:
                    points[row["name"]] = {
                        "coords": (float(row["latitude"]), float(row["longitude"])),
                        "image": row["image"] if row["image"] else None
                    }
    
    return points, roads, graph

def find_shortest_path(graph, points, start_name, end_name):
    """Find the shortest path between two points using NetworkX."""
    if start_name not in points or end_name not in points:
        print("❌ Error: One or both locations not found.")
        return []
    
    start = points[start_name]["coords"]
    end = points[end_name]["coords"]
    
    if start in graph and end in graph:
        return nx.shortest_path(graph, source=start, target=end, weight="weight")
    else:
        print("❌ No valid path found.")
        return []

def generate_route_map(start_name, end_name, points, roads, graph):
    """Generate a map with a route between two locations."""
    if start_name not in points or end_name not in points:
        print("❌ Error: One or both locations not found.")
        return
    
    m = folium.Map(location=points[start_name]["coords"], zoom_start=17)
    
    # Add markers with default arrow icon but show image in popup if available
    for loc_name in [start_name, end_name]:
        loc = points[loc_name]
        popup_text = f"<b>{loc_name}</b><br>({loc['coords'][0]}, {loc['coords'][1]})"
        if loc["image"]:
            popup_text += f'<br><img src="images/{loc["image"]}" width="100">'
        folium.Marker(loc["coords"], popup=folium.Popup(popup_text, max_width=250), icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)
    
    # Draw all roads
    for road in roads:
        folium.PolyLine(road["points"], color="blue", weight=3, opacity=0.7).add_to(m)
    
    # Draw the shortest path
    path = find_shortest_path(graph, points, start_name, end_name)
    if path:
        folium.PolyLine(path, color="red", weight=4, opacity=0.9).add_to(m)
    
    m.save(MAP_FILENAME)
    print(f"✅ Route map saved as {MAP_FILENAME}")

def main():
    points, roads, graph = load_camping_data()
    start_location = "Reception"
    end_location = "Bungalow 75"
    generate_route_map(start_location, end_location, points, roads, graph)

if __name__ == "__main__":
    main()