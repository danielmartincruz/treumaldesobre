#Script to generate the camping and define the data. 
import csv
import folium
import os
from predefined_points import predefined_locations  # Import categorized locations

# Define the directory for saving files
path = "data"
db_name = "camping_data.csv"
map_name = "select_points_map.html"

# Define full paths
db_filename = os.path.join(path, db_name)
map_filename = os.path.join(path, map_name)

# Ensure the directory exists
os.makedirs(path, exist_ok=True)

# Initialize CSV file with headers and predefined locations
existing_points = set()

# Check if the file already exists and read existing data
if os.path.exists(db_filename):
    with open(db_filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            existing_points.add(tuple(row))  # Store existing data to avoid duplicates

# Write predefined locations (only if not already present)
with open(db_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["name", "latitude", "longitude", "road_direction", "source"])  # Headers

    for location in predefined_locations:
        row = (
            location["name"], 
            location["latitude"], 
            location["longitude"], 
            location.get("road_direction", None),  # Ensures missing values are set to None
            location["source"]
        )
        if row not in existing_points:  # Avoid duplicate entries
            writer.writerow(row)

# Create an interactive map centered at Camping Treumal
camping_center = (41.8355, 3.0870)
m = folium.Map(location=camping_center, zoom_start=17)

# JavaScript script for click event
click_script = f"""
<script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = {m.get_name()};  // Get the Folium-generated map name

        map.on('click', function(e) {{
            var lat = e.latlng.lat.toFixed(7);  // Ensure 7 decimal places
            var lng = e.latlng.lng.toFixed(7);

            // Remove existing marker if any
            if (window.selectedMarker) {{
                map.removeLayer(window.selectedMarker);
            }}

            // Add a new marker at clicked location
            window.selectedMarker = L.marker(e.latlng).addTo(map)
                .bindPopup("Lat: " + lat + "<br>Lng: " + lng)
                .openPopup();
        }});
    }});
</script>
"""

# Inject JavaScript into the HTML
m.get_root().html.add_child(folium.Element(click_script))

# Save map to file
m.save(map_filename)

print(f"Open {map_filename} in a browser to select points. Click anywhere to see precise coordinates.")
