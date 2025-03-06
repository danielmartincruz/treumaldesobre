import csv
import folium
import os

# Define paths
DATA_PATH = "data"
ROUTES_PATH = "routes"
IMAGES_PATH = "images"
DB_NAME = "camping_data.csv"
MAP_NAME = "route_map.html"
DB_FILENAME = os.path.join(DATA_PATH, DB_NAME)
MAP_FILENAME = os.path.join(ROUTES_PATH, MAP_NAME)

# Ensure the routes directory exists
os.makedirs(ROUTES_PATH, exist_ok=True)

def load_camping_data():
    """Load camping data (points and roads) from CSV."""
    points, roads = {}, []
    
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
            else:
                if row["latitude"] and row["longitude"]:
                    points[row["name"]] = (float(row["latitude"]), float(row["longitude"]))
    
    return points, roads

def find_shortest_path(points, roads, start_name, end_name):
    """Find the shortest path between two points using roads."""
    from networkx import Graph, shortest_path
    
    graph = Graph()
    for road in roads:
        for i in range(len(road["points"]) - 1):
            graph.add_edge(road["points"][i], road["points"][i + 1], weight=1)
    
    if start_name in points and end_name in points:
        start_coord, end_coord = points[start_name], points[end_name]
        if start_coord in graph and end_coord in graph:
            return shortest_path(graph, source=start_coord, target=end_coord, weight='weight')
    
    return []

def generate_route_map(start_name, end_name, points, roads):
    """Generate a map with a route between two locations."""
    if start_name not in points or end_name not in points:
        print("❌ Error: One or both locations not found.")
        return
    
    m = folium.Map(location=points[start_name], zoom_start=17)
    
    # Add images to markers
    def add_marker_with_image(map_obj, name, coord, image_filename):
        image_path = os.path.join(IMAGES_PATH, image_filename)
        popup_html = f'<img src="{image_path}" width="150"><br>{name}<br>({coord[0]}, {coord[1]})'
        folium.Marker(coord, popup=folium.Popup(popup_html, max_width=200), icon=folium.Icon(color="green" if name == start_name else "red")).add_to(map_obj)
    
    add_marker_with_image(m, start_name, points[start_name], "Reception.jpeg")
    add_marker_with_image(m, end_name, points[end_name], "bungalow_75.jpeg")
    
    # Find and draw the shortest path
    path = find_shortest_path(points, roads, start_name, end_name)
    if path:
        folium.PolyLine(path, color="blue", weight=3, opacity=0.7).add_to(m)
    
    m.save(MAP_FILENAME)
    print(f"✅ Route map saved as {MAP_FILENAME}")

def main():
    points, roads = load_camping_data()
    start_location = "Reception"
    end_location = "Bungalow 75"
    generate_route_map(start_location, end_location, points, roads)

if __name__ == "__main__":
    main()
