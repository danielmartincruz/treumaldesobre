import csv
import folium
import networkx as nx
import qrcode
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Define paths
path = "data"
db_name = "camping_data.csv"
map_filename = "route_camping.html"
CREDENTIALS_FILE = "treumaldesobre.json"  # Service account credentials

# Google Drive Folder ID (your public folder)
GOOGLE_DRIVE_FOLDER_ID = "17I_oJRD-01s5icfCO_MmggjNRh6nRx-4"

# Authenticate Google Drive API
def authenticate_google_drive():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build("drive", "v3", credentials=creds)

# Upload file to Google Drive and return a public link
def upload_to_google_drive(local_file):
    drive_service = authenticate_google_drive()
    
    file_metadata = {
        "name": os.path.basename(local_file),
        "mimeType": "text/html",
        "parents": [GOOGLE_DRIVE_FOLDER_ID]  # Upload inside the shared folder
    }
    
    media = MediaFileUpload(local_file, mimetype="text/html")
    uploaded_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()
    
    file_id = uploaded_file.get("id")

    # Make file publicly accessible
    drive_service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
    ).execute()

    # Generate the public direct link
    return f"https://drive.google.com/uc?id={file_id}"

# Load camping data (points and roads) from CSV
def load_camping_data():
    points = {}
    roads = []
    with open(os.path.join(path, db_name), mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat, lon = float(row["latitude"]), float(row["longitude"])
            points[row["name"]] = (lat, lon)
            if row["road_direction"]:
                roads.append((row["name"], row["road_direction"]))
    return points, roads

# Build a directed graph with road connections
def build_graph(points, roads):
    G = nx.DiGraph()

    # Add nodes (all locations)
    for point_name, (lat, lon) in points.items():
        G.add_node(point_name, pos=(lat, lon))

    # Define manual logical connections to fix missing paths
    connections = {
        "Reception": ["Intersection 1", "Intersection 2"],  # Reception connects to Intersections
        "Intersection 1": ["Road 1", "Intersection 2"],  # Intersections link to roads & each other
        "Intersection 2": ["Road 2", "Intersection 3"],
        "Intersection 3": ["Road 3", "Intersection 4"],
        "Intersection 4": ["Road 4"],

        "Road 1": ["Bungalow 1", "Bungalow 2"],  # Roads link to bungalows
        "Road 2": ["Bungalow 3"],
        "Road 3": ["Bungalow 4"],
        "Road 4": ["Bungalow 5"]
    }

    # Connect nodes based on roads & directionality
    for road, direction in roads:
        if road in connections:
            for connected_point in connections[road]:
                G.add_edge(road, connected_point, weight=1)  # Default forward connection
                if direction == "two-way":
                    G.add_edge(connected_point, road, weight=1)  # Make it bidirectional

    # **Manually connect Reception to intersections** (this was missing)
    G.add_edge("Reception", "Intersection 1", weight=1)
    G.add_edge("Reception", "Intersection 2", weight=1)

    return G




# Generate the shortest route from reception to a chosen location
def generate_route(destination):
    points, roads = load_camping_data()
    G = build_graph(points, roads)

    if destination not in points:
        print("❌ Destination not found.")
        return
    
    try:
        route = nx.shortest_path(G, "Reception", destination, weight="weight")
    except nx.NetworkXNoPath:
        print("❌ No valid path found.")
        return
    
    # Create the map centered at Reception
    m = folium.Map(location=points["Reception"], zoom_start=17)

    # Draw the route on the map
    route_coords = [points[point] for point in route]
    folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(m)

    # Add markers
    for point in route:
        lat, lon = points[point]
        folium.Marker(
            location=[lat, lon],
            tooltip=point,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # Save the route locally
    m.save(map_filename)

    # Upload the file to Google Drive and get the link
    google_drive_url = upload_to_google_drive(map_filename)

    # Generate QR Code with the Google Drive link
    qr_filename = "route_qr.png"
    qr = qrcode.make(google_drive_url)
    qr.save(qr_filename)

    print(f"\n🚀 Route successfully uploaded to Google Drive: {google_drive_url}")
    print(f"📸 QR Code generated: {qr_filename} (links to the route map)")

def debug_graph(G):
    print("\n🚀 Graph Connections:")
    for edge in G.edges:
        print(f"➡️ {edge[0]} → {edge[1]}")
        
# Example usage
generate_route("Bungalow 2")  # Change this to any point from the CSV
