# Define bungalows (road_direction is not meaningful)
bungalows = [
    {"name": "Bungalow 75", "latitude": 41.835968, "longitude": 3.087096}
]

# Define intersections (road_direction is required)
intersections = [
    {"name": "Intersection 1", "latitude": 41.836325, "longitude": 3.087039 , "road_direction": "one-way"},
    {"name": "Intersection 2", "latitude": 41.835480, "longitude": 3.087084 , "road_direction": "one-way"}
]

# Define roads (as line segments)
roads = [
    {"name": "Road 1", "start": (41.836729, 3.087111), "end": (41.836346, 41.836346), "road_direction": "two-way"},
    {"name": "Road 2", "start": (41.836325, 3.087039), "end": (41.835480, 3.087084), "road_direction": "two-way"},
    {"name": "Road 3", "start": (41.835480, 3.087084), "end": (41.835, 3.0875), "road_direction": "one-way"},
    {"name": "Road 4", "start": (41.835, 3.0875), "end": (41.8347, 3.0873), "road_direction": "two-way"},
]

# Define special locations (road_direction is not meaningful)
special = [
    {"name": "Reception", "latitude": 41.8344505, "longitude": 3.0848667}
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
