from obstacles import getObstaclesForPolyline
from get_directions import fetch_directions


def goEatCurryWurst():
    default_origin = "BCG Düsseldorf"
    default_destination = "Curry, Hammer Str. 2, 40219 Düsseldorf"

    polylines = fetch_directions(default_origin, default_destination)

    print(polylines)

    for polyline in polylines:
        obstacles = getObstaclesForPolyline(polyline)
        print("Found obstacles:")
        print(obstacles)


