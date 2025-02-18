import gmaps
import gmaps.datasets
import qrcode
import googlemaps
import folium

# Configurar la API Key de Google Maps (debes proporcionar tu clave API aquí)
API_KEY = "AIzaSyB4c_cLBtUP7VEVt2PAtK5KXY3yAbLo01A"
gmaps.configure(api_key=API_KEY)
gmaps_client = googlemaps.Client(key=API_KEY)

# Coordenadas para el Camping Treumal
entrada = (41.8358468, 3.0867555)
bungalow = (41.835212, 3.087379)

# Obtener la ruta más corta en coche desde la entrada hasta el bungalow
route = gmaps_client.directions(
    origin=entrada,
    destination=bungalow,
    mode="driving",
    alternatives=False
)

# Crear el mapa con folium
m = folium.Map(location=entrada, zoom_start=18, tiles="cartodbpositron")

# Extraer la ruta y dibujarla en el mapa
if route:
    polyline = route[0]["overview_polyline"]["points"]
    decoded_polyline = googlemaps.convert.decode_polyline(polyline)
    route_coords = [(point["lat"], point["lng"]) for point in decoded_polyline]
    folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(m)
else:
    print("No route was generated.")

# Guardar el mapa
m.save("ruta_camping.html")

# Generar el QR con el enlace al mapa
data = "ruta_camping.html"
qr = qrcode.make(data)
qr.save("ruta_qr.png")

print("Mapa generado como 'ruta_camping.html' y QR guardado como 'ruta_qr.png'")
