from obstacles import getObstaclesForPolyline
from polylines import get_polylines


def goEatCurryWurst():
    default_origin = "BCG Düsseldorf"
    default_destination = "Curry, Hammer Str. 2, 40219 Düsseldorf"

    polylines = get_polylines(default_origin, default_destination)

    print(polylines)

    for polyline in polylines:
        obstacles = getObstaclesForPolyline(polyline)
        print("Found obstacles:")
        print(obstacles)


