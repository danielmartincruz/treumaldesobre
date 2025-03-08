# Define special points
special_points = [
    {"name": "Reception", "latitude": 41.8366780, "longitude": 3.0872467, "image": "Reception.jpeg", "road_direction": None}
]

# Define bungalows
bungalows = [
    {"name": "Bungalow 75", "latitude": 41.835968, "longitude": 3.087096, "image": "Bungalow_75.jpeg", "road_direction": None},
    {"name": "Bungalow 76", "latitude": 41.836968, "longitude": 3.087096, "image": "Bungalow_75.jpeg", "road_direction": None}

]

# Define roads (beginning and end points only)
roads = [
    {"name": "Road 1", "start": (41.8367279, 3.0871287), "end": (41.836358, 3.087034), "road_direction": "two-way"},
    {"name": "Road 2", "start": (41.836358, 3.087034), "end": (41.8362543, 3.0870697), "road_direction": "one-way"},
    {"name": "Road 3", "start": (41.8362543, 3.0870697), "end": (41.8357347, 3.0869409), "road_direction": "one-way"}
]

# Combine data
predefined_data = {"special_points": special_points, "bungalows": bungalows, "roads": roads}
    