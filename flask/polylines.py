import requests
import polyline
from flask import Flask, request, jsonify
from constants import *
from calculate_segment_score import calculate_score

def get_polylines(origin, destination):
    # Default values for origin and destination
    # TODO: REMOVE once frontend input is possible

    # if not origin or not destination:
    #     return jsonify({'error': 'Origin and Destination are required'}), 400

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
        routes = api_response.json()['routes']

        # Create dict {route, accessibility_score}
        # Evaluate main route plus alternatives
        routes_dict = {}
        for route in routes:
            steps_list = route['legs'][0]['steps']
            route_polylines = [polyline.decode(steps_list[i]["polyline"]["points"]) for i in range(0, len(steps_list))]
            route_score = calculate_score(route_polylines)
            routes_dict[str(route)] = route_score
        return routes_dict
    
    else:
        return {'error': 'Failed to fetch directions'}, 500
    