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

# Use the correct JSON credentials file
CREDENTIALS_FILE = "treumaldesobre.json"

# Google Drive Folder ID (Use the folder you shared publicly)
GOOGLE_DRIVE_FOLDER_ID = "17I_oJRD-01s5icfCO_MmggjNRh6nRx-4"

# Authenticate Google Drive API
def authenticate_google_drive():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build("drive", "v3", credentials=creds)

# Upload file to Google Drive and get a direct public link
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

# Generate the route between reception and a chosen location
def generate_route(destination):
    camping_center = (41.8355, 3.0870)
    m = folium.Map(location=camping_center, zoom_start=17)

    # Save the route locally
    m.save(map_filename)

    # Upload to Google Drive and get the direct link
    google_drive_link = upload_to_google_drive(map_filename)

    # Generate QR Code with direct link to the uploaded file
    qr_filename = "route_qr.png"
    qr = qrcode.make(google_drive_link)
    qr.save(qr_filename)

    print(f"\n🚀 Route saved and uploaded to Google Drive: {google_drive_link}")
    print(f"📸 QR Code generated: {qr_filename} (links to the route map)")

# Example usage
generate_route("Bungalow 2")
