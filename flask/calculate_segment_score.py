import requests
from geopy.distance import geodesic
from constants import *

def get_elevations(points):
    locations_str = "%7C".join([f"{lat},{lon}" for lat, lon in points])
    # print(f"Location str: {locations_str}")
    endpoint = f"https://maps.googleapis.com/maps/api/elevation/json?locations={locations_str}&key={GOOGLE_API_KEY}"
    response = requests.get(endpoint)
    print(f"Response str: {response.json()}")
    if response.status_code == 200:
        results = response.json().get('results', [])
        return [r['elevation'] for r in results]
    return []

def calculate_slope(point1, point2, elev1, elev2):
    delta_y = elev2 - elev1
    delta_x = geodesic((point1[0], point1[1]), (point2[0], point2[1])).meters

    # Slope calculation
    return delta_y / delta_x

def calculate_elevations(segment_polyline):
    print(segment_polyline)
    elevations = get_elevations(segment_polyline)
    max_slope = 0

    for i in range(len(segment_polyline) - 1):
        slope = calculate_slope(segment_polyline[i], segment_polyline[i+1], elevations[i], elevations[i+1])
        max_slope = max(max_slope, abs(slope))


def calculate_score(segment_polyline):
    print(len(segment_polyline))
    calculate_elevations(segment_polyline[0])
