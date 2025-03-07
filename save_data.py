import csv
import folium
import os
from predefined_points import predefined_data  # Import updated data structure

# Define the directory for saving files
DATA_PATH = "data"
DB_NAME = "camping_data.csv"
MAP_NAME = "select_points_map.html"
DB_FILENAME = os.path.join(DATA_PATH, DB_NAME)
MAP_FILENAME = os.path.join(DATA_PATH, MAP_NAME)

# Ensure the directory exists
os.makedirs(DATA_PATH, exist_ok=True)

def save_data_to_csv():
    """Save predefined locations and roads to a CSV file."""
    special_points = predefined_data["special_points"]
    bungalows = predefined_data["bungalows"]
    roads = predefined_data["roads"]

    with open(DB_FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "latitude", "longitude", "image", "road_direction", "source"])

        for location in special_points + bungalows:
            writer.writerow([
                location["name"],
                location["latitude"],
                location["longitude"],
                location["image"],
                location.get("road_direction", ""),
                "special" if location in special_points else "bungalow"
            ])

        for road in roads:
            writer.writerow([
                road["name"],
                road["start"][0], road["start"][1], "",  # Empty image field for roads
                road["road_direction"], "road"
            ])
            writer.writerow([
                road["name"] + " End",
                road["end"][0], road["end"][1], "",
                road["road_direction"], "road"
            ])

    print(f"✅ Updated {DB_FILENAME} with {len(special_points) + len(bungalows) + len(roads)} locations.")

def main():
    save_data_to_csv()

if __name__ == "__main__":
    main()
