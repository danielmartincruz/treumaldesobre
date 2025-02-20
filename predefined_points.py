# predefined_points.py

# Define bungalows (road_direction is not meaningful)
bungalows = [
    {"name": "Bungalow 1", "latitude": 41.835212, "longitude": 3.087379},
    {"name": "Bungalow 2", "latitude": 41.835, "longitude": 3.0875},
    {"name": "Bungalow 3", "latitude": 41.8348, "longitude": 3.0876},
    {"name": "Bungalow 4", "latitude": 41.8346, "longitude": 3.0872},
    {"name": "Bungalow 5", "latitude": 41.8344, "longitude": 3.0869},
]

# Define intersections (road_direction is required)
intersections = [
    {"name": "Intersection 1", "latitude": 41.8355, "longitude": 3.087, "road_direction": "one-way"},
    {"name": "Intersection 2", "latitude": 41.8352, "longitude": 3.0872, "road_direction": "two-way"},
    {"name": "Intersection 3", "latitude": 41.8349, "longitude": 3.0874, "road_direction": "one-way"},
    {"name": "Intersection 4", "latitude": 41.8346, "longitude": 3.0871, "road_direction": "two-way"},
]

# Define roads (road_direction is required)
roads = [
    {"name": "Road 1", "latitude": 41.8356, "longitude": 3.0871, "road_direction": "one-way"},
    {"name": "Road 2", "latitude": 41.8353, "longitude": 3.0873, "road_direction": "two-way"},
    {"name": "Road 3", "latitude": 41.835, "longitude": 3.0875, "road_direction": "one-way"},
    {"name": "Road 4", "latitude": 41.8347, "longitude": 3.0873, "road_direction": "two-way"},
]

# Define special locations (road_direction is not meaningful)
special = [
    {"name": "Reception", "latitude": 41.8358468, "longitude": 3.0867555},
    {"name": "Pool", "latitude": 41.8349, "longitude": 3.0866},
]

# Add the "source" field to each category and ensure "road_direction" where needed
for location in bungalows:
    location["source"] = "bungalow"
    location["road_direction"] = None  # Explicitly setting it for clarity

for location in intersections:
    location["source"] = "intersection"

for location in roads:
    location["source"] = "road"

for location in special:
    location["source"] = "special"
    location["road_direction"] = None  # Explicitly setting it for clarity

# Combine all locations into a single list
predefined_locations = bungalows + intersections + roads + special
