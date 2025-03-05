import csv
import folium
import os

# Define paths
DATA_PATH = "data"
ROUTES_PATH = "routes"
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

def generate_route_map(start_name, end_name, points, roads):
    """Generate a map with a route between two locations."""
    if start_name not in points or end_name not in points:
        print("❌ Error: One or both locations not found.")
        return
    
    m = folium.Map(location=points[start_name], zoom_start=17)
    folium.Marker(points[start_name], popup=start_name, icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(points[end_name], popup=end_name, icon=folium.Icon(color="red")).add_to(m)
    
    for road in roads:
        folium.PolyLine(road["points"], color="blue", weight=3, opacity=0.7).add_to(m)
    
    m.save(MAP_FILENAME)
    print(f"✅ Route map saved as {MAP_FILENAME}")

def main():
    points, roads = load_camping_data()
    start_location = "Reception"
    end_location = "Bungalow 75"
    generate_route_map(start_location, end_location, points, roads)

if __name__ == "__main__":
    main()
