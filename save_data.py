import csv
import folium
import os
from predefined_points import predefined_locations, roads  # Import roads separately

# Define the directory for saving files
DATA_PATH = "data"
DB_NAME = "camping_data.csv"
MAP_NAME = "select_points_map.html"
DB_FILENAME = os.path.join(DATA_PATH, DB_NAME)
MAP_FILENAME = os.path.join(DATA_PATH, MAP_NAME)

# Ensure the directory exists
os.makedirs(DATA_PATH, exist_ok=True)

def convert_old_road_format():
    """Convert roads using 'start'/'end' to the new 'points' format if necessary."""
    for road in roads:
        if "points" not in road and "start" in road and "end" in road:
            road["points"] = [road["start"], road["end"]]
            del road["start"], road["end"]

def get_max_waypoints():
    """Determine the maximum number of waypoints across all roads."""
    return max(len(road["points"]) for road in roads) if roads else 2

def save_data_to_csv():
    """Save predefined locations and roads to a CSV file."""
    convert_old_road_format()
    max_waypoints = get_max_waypoints()
    
    with open(DB_FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        waypoint_headers = [f"lat_{i},lon_{i}" for i in range(1, max_waypoints + 1)]
        writer.writerow(["name", "latitude", "longitude", "image"] + waypoint_headers + ["road_direction", "source"])

        for location in predefined_locations:
            lat = location.get("latitude", "") or ""
            lon = location.get("longitude", "") or ""
            image = location.get("image", "") or ""
            writer.writerow([
                location["name"], lat, lon, image
            ] + ["" for _ in range(2 * max_waypoints)] + [location.get("road_direction", ""), location["source"]])

        for road in roads:
            waypoints = [coord for point in road["points"] for coord in point]
            waypoints += ["", ""] * (max_waypoints - len(road["points"]))
            writer.writerow([
                road["name"], "", "", ""  # Empty columns for single lat/lon and image (not needed for roads)
            ] + waypoints + [road["road_direction"], "road"])
    
    print(f"✅ Updated {DB_FILENAME} with {len(predefined_locations) + len(roads)} locations.")

def main():
    save_data_to_csv()

if __name__ == "__main__":
    main()
