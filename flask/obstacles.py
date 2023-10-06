import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal


# DO we integrate Google map in the back or front?
def getAllObstaclesOnTheWay(start, end):
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    obstacles_table = db.Table('Obstacles')
    obstacles_on_the_way = obstacles_table.scan(
        FilterExpression=Attr("obs_coordinate_long").gte(Decimal('6.1')) & Attr("obs_coordinate_long").lte(Decimal('6.8'))
    )['Items']

    return obstacles_on_the_way


def getAllObstacles():
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    tTable = db.Table('Obstacles')
    print(tTable.scan()['Items'])

def postObstacle():
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    tTable = db.Table('Obstacles')


# def getFeedbackForRoute(start, end):
#     db = boto3.resource('dynamodb', region_name='eu-central-1')
#     tTable = db.Table('Obstacles')
#     print(tTable.scan()['Items'])
#
# def getFeedbackForRoute(start, end):
#     db = boto3.resource('dynamodb', region_name='eu-central-1')
#     tTable = db.Table('Obstacles')
#     print(tTable.scan()['Items'])

def is_point_inside_line_segment(start, end, point):
    # Calculate the equation of the line passing through start and end points
    line_equation = lambda x: (end[1] - start[1]) * (x - start[0]) / (end[0] - start[0]) + start[1]

    # Check if the point lies within the bounding box of the line segment
    if (start[0] <= point[0] <= end[0] or start[0] >= point[0] >= end[0]) and \
            (start[1] <= point[1] <= end[1] or start[1] >= point[1] >= end[1]):
        # Check if the point lies on or below the line
        if point[1] <= line_equation(point[0]):
            return True
    return False