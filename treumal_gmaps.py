API_KEY = "AIzaSyB4c_cLBtUP7VEVt2PAtK5KXY3yAbLo01A"

import csv
import qrcode
import os
import webbrowser

# Define paths
DATA_PATH = "data"
DB_NAME = "camping_data.csv"
DB_FILENAME = os.path.join(DATA_PATH, DB_NAME)

# Load points from CSV
def load_camping_data():
    points = {}
    with open(DB_FILENAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["source"] != "road":  # Only gather points, no roads
                points[row["name"]] = {
                    "coords": (float(row["latitude"]), float(row["longitude"])),
                    "image": row["image"] if row["image"] else None
                }
    return points

# Generate Google Maps link
def generate_google_maps_link(start_coords, end_coords):
    link = f"https://www.google.com/maps/dir/{start_coords[0]},{start_coords[1]}/{end_coords[0]},{end_coords[1]}"
    return link

# Generate QR Code for the Google Maps Link
def generate_qr_code(link):
    qr = qrcode.make(link)
    qr.save("ruta_qr.png")
    print("✅ QR Code generated as 'ruta_qr.png'")

def main():
    points = load_camping_data()
    start_location = "Reception"
    end_location = "Bungalow 75"

    if start_location in points and end_location in points:
        start_coords = points[start_location]["coords"]
        end_coords = points[end_location]["coords"]

        google_maps_link = generate_google_maps_link(start_coords, end_coords)
        print(f"✅ Google Maps Link: {google_maps_link}")

        # Generate QR Code
        generate_qr_code(google_maps_link)

        # Open link in browser (optional)
        webbrowser.open(google_maps_link)
    else:
        print("❌ Error: Start or End location not found in CSV data.")

if __name__ == "__main__":
    main()
