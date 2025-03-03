import os
import csv
import folium
import networkx as nx
import qrcode
import shutil
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# Define paths
DATA_PATH = "data"
IMAGE_PATH = "images"
ROUTES_PATH = "routes"
DB_NAME = "camping_data.csv"
CREDENTIALS_FILE = "treumaldesobre.json"  # Service account credentials
GOOGLE_DRIVE_FOLDER_ID = "17I_oJRD-01s5icfCO_MmggjNRh6nRx-4"

def authenticate_google_drive():
    """Authenticate and return a Google Drive service client."""
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build("drive", "v3", credentials=creds)

def upload_to_google_drive(local_file):
    """Upload a file to Google Drive and return a public link."""
    drive_service = authenticate_google_drive()
    mime_type = "image/jpeg" if local_file.endswith(('.jpg', '.jpeg', '.png')) else "text/html"
    file_metadata = {"name": os.path.basename(local_file), "mimeType": mime_type, "parents": [GOOGLE_DRIVE_FOLDER_ID]}
    media = MediaFileUpload(local_file, mimetype=mime_type)
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    file_id = uploaded_file.get("id")
    
    drive_service.permissions().create(fileId=file_id, body={"role": "reader", "type": "anyone"}).execute()
    return f"https://drive.google.com/uc?id={file_id}"

def load_camping_data():
    """Load camping data (points and roads) from CSV."""
    points, roads = {}, []
    
    with open(os.path.join(DATA_PATH, DB_NAME), mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row["source"] == "road":  
                # ✅ Roads are stored using start and end coordinates, not single lat/lon
                if row["start_lat"] and row["start_lon"] and row["end_lat"] and row["end_lon"]:
                    start = (float(row["start_lat"]), float(row["start_lon"]))
                    end = (float(row["end_lat"]), float(row["end_lon"]))
                    roads.append((row["name"], start, end, row["road_direction"]))  # Store as segment
            else:
                # ✅ Single locations (Bungalows, Reception, Intersections)
                if row["latitude"] and row["longitude"]:  # Ensure no empty values
                    points[row["name"]] = (float(row["latitude"]), float(row["longitude"]))
    
    return points, roads


def build_graph(points, roads):
    """Construct a directed graph from the camping data."""
    G = nx.DiGraph()

    # Add nodes for all points (Reception, Intersections, Bungalows)
    for point_name, coords in points.items():
        G.add_node(point_name, pos=coords)

    # ✅ Add edges for roads (using tuple structure: (name, start, end, direction))
    for road in roads:
        road_name, start, end, direction = road  # ✅ Unpack tuple

        # Create unique node names for start and end points
        start_point = f"{road_name}_start"
        end_point = f"{road_name}_end"

        G.add_node(start_point, pos=start)
        G.add_node(end_point, pos=end)

        G.add_edge(start_point, end_point, weight=1)  # Default one-way
        if direction == "two-way":
            G.add_edge(end_point, start_point, weight=1)  # Allow reverse direction

    return G



def get_shortest_path(G, origin, destination):
    """Calculate the shortest path from origin to a given destination."""
    try:
        return nx.shortest_path(G, origin, destination, weight="weight")
    except nx.NetworkXNoPath:
        print("❌ No valid path found.")
        return None

def add_images_to_route(route, points):
    """Add images to route points where available."""
    image_locations = {"Reception": "Reception.jpeg", "Bungalow 2": "bungalow_2.jpeg"}
    os.makedirs(os.path.join(ROUTES_PATH, "images"), exist_ok=True)
    copied_image_locations = {}
    for point, img in image_locations.items():
        src = os.path.join(IMAGE_PATH, img)
        dest = os.path.join(ROUTES_PATH, "images", img)
        shutil.copy(src, dest)
        copied_image_locations[point] = dest
    return copied_image_locations

def save_route(route, points, destination, save_to_drive=False):
    """Save the route locally and optionally upload to Google Drive."""
    m = folium.Map(location=points[route[0]], zoom_start=17)
    folium.PolyLine([points[point] for point in route], color='blue', weight=5, opacity=0.7).add_to(m)
    
    local_map_filename = os.path.join(ROUTES_PATH, f"route_to_{destination.replace(' ', '_')}.html")
    m.save(local_map_filename)
    print(f"📁 Route saved locally: {local_map_filename}")
    
    if save_to_drive:
        google_drive_url = upload_to_google_drive(local_map_filename)
        qr_filename = os.path.join(ROUTES_PATH, f"qr_to_{destination.replace(' ', '_')}.png")
        qr = qrcode.make(google_drive_url)
        qr.save(qr_filename)
        print(f"🚀 Route uploaded: {google_drive_url}")
        print(f"📸 QR Code generated: {qr_filename}")

def generate_route(origin, destination, save_to_drive=False):
    """Generate a route from origin to destination."""
    points, roads = load_camping_data()
    G = build_graph(points, roads)
    route = get_shortest_path(G, origin, destination)
    if route:
        add_images_to_route(route, points)
        save_route(route, points, destination, save_to_drive)

def main():
    """Main execution function."""
    origin = "Reception"  # Default starting point
    destination = "Intersection 1"  # Change as needed
    save_to_drive = True  # Change to False to save locally only
    generate_route(origin, destination, save_to_drive)

if __name__ == "__main__":
    main()
