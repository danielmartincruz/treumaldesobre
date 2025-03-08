import csv
import folium
import os
import networkx as nx
import numpy as np
from geopy.distance import geodesic

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
    points, roads = {}, []
    graph = nx.Graph()
    road_start_points = {}  # Track road starts to match with endpoints

    with open(DB_FILENAME, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row["source"] == "road":
                if "End" in row["name"]:
                    road_name = row["name"].replace(" End", "")
                    if road_name in road_start_points:
                        roads.append({
                            "name": road_name,
                            "start": road_start_points[road_name],
                            "end": (float(row["latitude"]), float(row["longitude"])),
                            "road_direction": row["road_direction"]
                        })
                        graph.add_edge(roads[-1]["start"], roads[-1]["end"], weight=geodesic(roads[-1]["start"], roads[-1]["end"]).meters)
                else:
                    road_start_points[row["name"]] = (float(row["latitude"]), float(row["longitude"]))
            else:
                points[row["name"]] = {
                    "coords": (float(row["latitude"]), float(row["longitude"])),
                    "image": row["image"] if row["image"] else None
                }
    
    return points, roads, graph

def closest_point_on_line(p, a, b):
    p, a, b = np.array(p), np.array(a), np.array(b)
    ap = p - a
    ab = b - a
    t = np.dot(ap, ab) / np.dot(ab, ab)
    t = max(0, min(1, t))

    return tuple(a + t * ab)

def find_trimmed_road(point, roads, graph):
    closest_road = None
    closest_point = None
    min_distance = float('inf')

    for road in roads:
        a, b = road["start"], road["end"]
        closest = closest_point_on_line(point, a, b)
        distance = geodesic(point, closest).meters
        if distance < min_distance:
            min_distance = distance
            closest_point = closest
            closest_road = road

    graph.add_node(closest_point)
    graph.add_edge(closest_road["start"], closest_point, weight=geodesic(closest_road["start"], closest_point).meters)
    graph.add_edge(closest_point, closest_road["end"], weight=geodesic(closest_point, closest_road["end"]).meters)

    return [closest_road["start"], closest_point], [closest_point, closest_road["end"]], tuple(closest_point)

def generate_route_map(points, roads, graph, start_point, end_point):
    m = folium.Map(location=points[start_point]["coords"], zoom_start=17)

    for point_name in [start_point, end_point]:
        point_data = points[point_name]
        popup_text = f"<b>{point_name}</b><br>({point_data['coords'][0]}, {point_data['coords'][1]})"
        if point_data["image"]:
            popup_text += f'<br><img src="images/{point_data["image"]}" width="100">'
        folium.Marker(point_data["coords"], popup=popup_text, icon=folium.Icon(color="blue", icon="info-sign")).add_to(m)

    trimmed_road_A, _, node_A = find_trimmed_road(points[start_point]["coords"], roads, graph)
    trimmed_road_B, _, node_B = find_trimmed_road(points[end_point]["coords"], roads, graph)

    folium.PolyLine(trimmed_road_A, color="blue", weight=3, opacity=0.7).add_to(m)
    folium.PolyLine(trimmed_road_B, color="blue", weight=3, opacity=0.7).add_to(m)

    path = nx.shortest_path(graph, source=node_A, target=node_B, weight="weight")
    folium.PolyLine(path, color="red", weight=4, opacity=0.9).add_to(m)

    m.save(MAP_FILENAME)
    print(f"✅ Route map saved as {MAP_FILENAME}")

def main():
    points, roads, graph = load_camping_data()
    start_location = "Reception"
    end_location = "Bungalow 75"
    generate_route_map(points, roads, graph, start_location, end_location)

if __name__ == "__main__":
    main()
