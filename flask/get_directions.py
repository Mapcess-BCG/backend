import requests
import polyline
from map_utils import is_location_on_polyline

GOOGLE_DIRECTIONS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"
GOOGLE_API_KEY = "AIzaSyAWEPohy9CdHpz6j8-_zLDRsSWoDI9b2YU"

def fetch_directions(origin, destination):
    params = {
        'origin': origin,
        'destination': destination,
        'key': GOOGLE_API_KEY,
        'mode': 'walking'
    }

    api_response = requests.get(GOOGLE_DIRECTIONS_API_URL, params=params)
    
    if api_response.status_code == 200:
        # Extract polylines
        steps_list = api_response.json()['routes'][0]['legs'][0]['steps']
        polylines = [steps_list[i]["polyline"]["points"] for i in range(0, len(steps_list))]
        return polylines
    else:
        return {'error': 'Failed to fetch directions'}, 500