# Define bungalows (road_direction is not meaningful)
bungalows = [
    {"name": "Bungalow 75", "latitude": 41.835968, "longitude": 3.087096, "image": "Bungalow_75.jpeg"}
]

# Define intersections (road_direction is required)
intersections = [
    {"name": "Intersection 1", "latitude": 41.8363582, "longitude": 3.0870348 , "road_direction": "one-way"},
    {"name": "Intersection 2", "latitude": 41.835480, "longitude": 3.087084 , "road_direction": "one-way"}
]

# Define roads (as line segments)
roads = [
    {"name": "Road 1", "points": [(41.8367399, 3.0871341), (41.8365941, 3.0870992), (41.8363582, 3.0870348)], "road_direction": "two-way"},
    {"name": "Road 2", "points": [(41.8363582, 3.0870348), (41.8362543, 3.0870697)], "road_direction": "one-way"},
    {"name": "Road 3", "points": [(41.8362543, 3.0870697), (41.8361304, 3.0870402), (41.8359606, 3.0870080)], "road_direction": "one-way"},
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
