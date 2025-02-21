import csv
import folium
import networkx as nx
import osmnx as ox
import qrcode
import os

# Define paths
path = "data"
image_path = "images"
db_name = "camping_data.csv"
db_filename = os.path.join(path, db_name)

# Load points and roads from CSV
def load_camping_data():
    points = {}
    roads = []
    with open(db_filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat, lon = float(row["latitude"]), float(row["longitude"])
            points[row["name"]] = (lat, lon)
            if row["road_direction"]:
                roads.append((lat, lon, row["road_direction"]))
    return points, roads

# Create a graph for the internal roads
def build_graph(points, roads):
    G = nx.DiGraph()
    for point_name, (lat, lon) in points.items():
        G.add_node(point_name, pos=(lat, lon))
    
    for lat, lon, direction in roads:
        closest_point = min(points, key=lambda p: (points[p][0] - lat)**2 + (points[p][1] - lon)**2)
        if direction == "one-way":
            G.add_edge("Reception", closest_point, weight=1)
        else:
            G.add_edge("Reception", closest_point, weight=1)
            G.add_edge(closest_point, "Reception", weight=1)
    
    return G

# Add images to specific locations
image_locations = {
    "Reception": "Reception.jpeg",
    "Bungalow 2": "bungalow_2.jpeg"
}

# Generate the route between reception and a chosen location
def generate_route(destination):
    points, roads = load_camping_data()
    G = build_graph(points, roads)
    
    if destination not in points:
        print("Destination not found.")
        return
    
    try:
        route = nx.shortest_path(G, "Reception", destination, weight="weight")
    except nx.NetworkXNoPath:
        print("No valid path found.")
        return
    
    # Create the map
    m = folium.Map(location=points["Reception"], zoom_start=17)
    
    # Draw the route
    route_coords = [points[point] for point in route]
    folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(m)

    # Add markers with images where available
    for point in route:
        lat, lon = points[point]

        # Check if an image exists for this location
        if point in image_locations:
            img_filename = os.path.join(image_path, image_locations[point])
            img_html = f'<img src="{img_filename}" width="200px">'

            popup = folium.Popup(img_html, max_width=250)
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=point,
                icon=folium.Icon(color="green", icon="info-sign")
            ).add_to(m)
        else:
            # Default marker without an image
            folium.Marker(
                location=[lat, lon],
                tooltip=point,
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

    # Save the map
    map_filename = "route_camping.html"
    m.save(map_filename)
    
    # Generate a QR code for the route
    qr = qrcode.make(map_filename)
    qr.save("route_qr.png")
    
    print(f"Route saved as {map_filename} and QR saved as route_qr.png")

# Example usage:
destination = "Bungalow 2"  # Change this to any point from the CSV
generate_route(destination)
