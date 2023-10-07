from calculate_segment_score import calculate_score
from obstacles import getObstaclesForPolyline
from polylines import get_polylines
from feedback import getFeedbackAlongTheRoute
from flask import Flask, request, jsonify
import polyline


def getAllRoutes(origin, destination):

    routes = get_polylines(origin, destination)

    result = []

    for route in routes:
        routeObject = {}

        steps_list = route['legs'][0]['steps']
        route_polylines = [polyline.decode(steps_list[i]["polyline"]["points"]) for i in range(0, len(steps_list))]
        route_score = calculate_score(route_polylines)
        obstacles = []
        feedback = []

        for line in route_polylines:
            obstacles.extend(getObstaclesForPolyline(line))
            feedback.extend(getFeedbackAlongTheRoute(line))
            print("Found obstacles:")

        result.append({
            'polyline': route_polylines,
            'obstacles': obstacles,
            'score': route_score,
            'feedback': feedback,
        })

    return result




