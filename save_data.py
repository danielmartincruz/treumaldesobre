import csv
import folium
import os
from predefined_points import predefined_locations, roads  # Import roads separately

# Define the directory for saving files
path = "data"
db_name = "camping_data.csv"
map_name = "select_points_map.html"

# Define full paths
db_filename = os.path.join(path, db_name)
map_filename = os.path.join(path, map_name)

# Ensure the directory exists
os.makedirs(path, exist_ok=True)

# Determine the maximum number of waypoints across all roads
max_waypoints = max(len(road["points"]) for road in roads) if roads else 2

# ✅ Overwrite camping_data.csv with the latest data
with open(db_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # ✅ Dynamically generate headers for road waypoints
    waypoint_headers = [f"lat_{i},lon_{i}" for i in range(1, max_waypoints + 1)]
    writer.writerow(["name", "latitude", "longitude"] + waypoint_headers + ["road_direction", "source"])  

    # ✅ Write all predefined locations (bungalows, intersections, special locations)
    for location in predefined_locations:
        writer.writerow([
            location["name"], 
            location["latitude"], 
            location["longitude"]
        ] + ["" for _ in range(2 * max_waypoints)] + [location.get("road_direction", ""), location["source"]])

    # ✅ Write roads with flexible waypoints
    for road in roads:
        waypoints = [coord for point in road["points"] for coord in point]  # Flatten list
        waypoints += ["", ""] * (max_waypoints - len(road["points"]))  # Pad to max length
        
        writer.writerow([
            road["name"], "", ""  # Empty columns for single lat/lon (not needed for roads)
        ] + waypoints + [road["road_direction"], "road"])

print(f"✅ Updated {db_filename} with {len(predefined_locations) + len(roads)} locations.")

# Create an interactive map centered at Camping Treumal
camping_center = (41.8355, 3.0870)
m = folium.Map(location=camping_center, zoom_start=17)
