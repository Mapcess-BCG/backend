import requests
import numpy as np
from geopy.distance import geodesic
from constants import *
from feedback import getFeedbackAlongTheRoute

def get_elevations(points):
    locations_str = "%7C".join([f"{lat},{lon}" for lat, lon in points])
    # print(f"Location str: {locations_str}")
    endpoint = f"https://maps.googleapis.com/maps/api/elevation/json?locations={locations_str}&key={GOOGLE_API_KEY}"
    response = requests.get(endpoint)
    # print(f"Response str: {response.json()}")
    if response.status_code == 200:
        results = response.json().get('results', [])
        return [r['elevation'] for r in results]
    return []

def calculate_slope(point1, point2, elev1, elev2):
    delta_y = elev2 - elev1
    delta_x = geodesic((point1[0], point1[1]), (point2[0], point2[1])).meters

    # Slope calculation
    return (delta_y / delta_x)*100

def calculate_elevation_score(segment_polyline):
    print(segment_polyline)
    elevations = get_elevations(segment_polyline)
    max_slope = 0

    for i in range(len(segment_polyline) - 1):
        slope = calculate_slope(segment_polyline[i], segment_polyline[i+1], elevations[i], elevations[i+1])
        max_slope = max(max_slope, abs(slope))

    elevation_score = 5

    if max_slope > 20:
        elevation_score = 1
    elif max_slope > 15:
        elevation_score = 2
    elif max_slope > 10:
        elevation_score = 3
    elif max_slope > 6:
        elevation_score = 4
    else:
        elevation_score = 5

    return elevation_score

def calculate_feedback_score(segment_polyline):
    scores = []
    result = getFeedbackAlongTheRoute(segment_polyline)
    for res in result:
        print(f"Feedback res: {res}")
        if res["feed_score"] != None:
            scores.append(int(res["feed_score"]))

    if len(scores)>0:
        return scores
    else:
        return None

def calculate_score(polyline):

    elevation_scores = []
    feedback_scores = []

    for segment_polyline in polyline:
        elevation_scores.append(calculate_elevation_score(segment_polyline))
        feedback_res = calculate_feedback_score(segment_polyline)
        if feedback_res != None:
            feedback_scores.extend(feedback_res)

    if len(feedback_scores) > 0:
        mean_elevation = np.mean(elevation_scores)
        mean_feedback = np.mean(feedback_scores)
        accessibility_score = (mean_elevation + mean_feedback) / 2
    else:
        accessibility_score = np.mean(elevation_scores)

    return accessibility_score

