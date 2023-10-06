from calculate_segment_score import calculate_score
from obstacles import getObstaclesForPolyline
from polylines import get_polylines
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

        for line in route_polylines:
            obstacles.extend(getObstaclesForPolyline(line))
            print("Found obstacles:")
            print(obstacles)

        result.append({
            'polyline': route_polylines,
            'obstacles': obstacles,
            'score': route_score,
            'feedback': [],
        })

    return result




