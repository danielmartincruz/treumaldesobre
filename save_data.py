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

# ✅ Overwrite camping_data.csv with the latest data
with open(db_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    # ✅ Add new headers for roads (start_lat, start_lon, end_lat, end_lon)
    writer.writerow(["name", "latitude", "longitude", "start_lat", "start_lon", "end_lat", "end_lon", "road_direction", "source"])  

    # ✅ Write all predefined locations (bungalows, intersections, special locations)
    for location in predefined_locations:
        writer.writerow([
            location["name"], 
            location["latitude"], 
            location["longitude"], 
            "", "", "", "",  # Empty columns for start/end coordinates (not needed for single points)
            location.get("road_direction", ""),  
            location["source"]
        ])

    # ✅ Write roads with start & end coordinates
    for road in roads:
        writer.writerow([
            road["name"], 
            "", "",  # Empty columns for single lat/lon (not needed for roads)
            road["start"][0], road["start"][1],  # Start coordinates
            road["end"][0], road["end"][1],  # End coordinates
            road["road_direction"],  
            "road"
        ])

print(f"✅ Updated {db_filename} with {len(predefined_locations) + len(roads)} locations.")

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

print(f"✅ Open {map_filename} in a browser to select points. Click anywhere to see precise coordinates.")
