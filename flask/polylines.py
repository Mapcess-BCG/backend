import requests
import polyline
from flask import Flask, request, jsonify
# from map_utils import is_location_on_polyline

GOOGLE_DIRECTIONS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"
GOOGLE_API_KEY = "AIzaSyAWEPohy9CdHpz6j8-_zLDRsSWoDI9b2YU"

def get_polylines(origin, destination):
    # Default values for origin and destination
    # TODO: REMOVE once frontend input is possible

    if not origin or not destination:
        return jsonify({'error': 'Origin and Destination are required'}), 400

    if not origin:
        origin = "BCG Düsseldorf"
    if not destination:
        destination = "Curry, Hammer Str. 2, 40219 Düsseldorf"

    params = {
        'origin': origin,
        'destination': destination,
        'key': GOOGLE_API_KEY,
        'mode': 'walking',
        "alternatives": 'true'
    }

    api_response = requests.get(GOOGLE_DIRECTIONS_API_URL, params=params)
    
    if api_response.status_code == 200:
        # Extract polylines
        # TODO: Handle alternate routes
        steps_list = api_response.json()['routes'][0]['legs'][0]['steps']
        polylines = [polyline.decode(steps_list[i]["polyline"]["points"]) for i in range(0, len(steps_list))]

        # return len(polylines[0]), get_elevation(steps_list)
        return polylines
    else:
        return {'error': 'Failed to fetch directions'}, 500

def get_elevation(steps_list):
    for step in steps_list:
        # Get start and end coordinates
        start_lat = step["start_location"]["lat"]
        start_lng = step["start_location"]["lng"]
        end_lat = step["end_location"]["lat"]
        end_lng = step["end_location"]["lng"]

        # Get distance in meters
        distance = step["distance"]["value"]
        # api_response = requests.get(GOOGLE_DIRECTIONS_API_URL, params=params)