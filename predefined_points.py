# Define bungalows (road_direction is not meaningful)
bungalows = [
    {"name": "Bungalow 75", "latitude": 41.835968, "longitude": 3.087096, "image": "Bungalow_75.jpeg"}
]

# Define intersections (road_direction is required)
intersections = [
    {"name": "Intersection 1", "latitude": 41.836325, "longitude": 3.087039 , "road_direction": "one-way"},
    {"name": "Intersection 2", "latitude": 41.835480, "longitude": 3.087084 , "road_direction": "one-way"}
]

# Define roads (as line segments)
roads = [
    {"name": "Road 1", "points": [(41.836729, 3.087111), (41.836600, 3.087050), (41.836346, 3.087046)], "road_direction": "two-way"},
    {"name": "Road 2", "points": [(41.836325, 3.087039), (41.835480, 3.087084)], "road_direction": "one-way"},
]

# Define special locations (road_direction is not meaningful)
special = [
    {"name": "Reception", "latitude": 41.8366780, "longitude": 3.0871180, "image": "Reception.jpeg"}
]

# Add the "source" field
for location in bungalows:
    location["source"] = "bungalow"
    location["road_direction"] = None  # Not needed

for location in intersections:
    location["source"] = "intersection"

for location in roads:
    location["source"] = "road"

for location in special:
    location["source"] = "special"
    location["road_direction"] = None  # Not needed

# Combine all locations into a single list
predefined_locations = bungalows + intersections + special
