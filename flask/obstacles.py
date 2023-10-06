import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# TODO: optimize -> move to the server file and make it global
db = boto3.resource('dynamodb', region_name='eu-central-1')
obstacles_table = db.Table('Obstacles')


def getObstaclesForPolyline(polyline):
    # TODO: optimize
    print('our polyline:')
    print(polyline)
    filter_expression = getFilterExpression(polyline[0])
    for coordinate in polyline:
        filter_expression = filter_expression | getFilterExpression(coordinate)

    obstacles_on_the_way = obstacles_table.scan(
        FilterExpression=filter_expression
    )['Items']

    print(obstacles_on_the_way)

    return obstacles_on_the_way


# DO we integrate Google map in the back or front?
def getAllObstaclesOnTheWay(start, end):
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    obstacles_table = db.Table('Obstacles')
    obstacles_on_the_way = obstacles_table.scan(
        FilterExpression=(
                             Attr("obs_coordinate_long").gte(Decimal(start.split(':')[1]) + Decimal('0.00002'))
                         & Attr("obs_coordinate_long").lte(Decimal(start.split(':')[1]) + Decimal('0.00002'))
        )
    )['Items']

    return obstacles_on_the_way


def getAllObstacles():
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    tTable = db.Table('Obstacles')
    print(tTable.scan()['Items'])

# TODO: to implement
def postObstacle():
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    tTable = db.Table('Obstacles')



def getFilterExpression(coordinate):
    print(coordinate.split(':'))
    print(Decimal(coordinate.split(':')[1]))
    
    return Attr("obs_coordinate_long").gte(Decimal(coordinate.split(':')[1]) + Decimal('0.00002')) \
           & Attr("obs_coordinate_long").lte(Decimal(coordinate.split(':')[1]) + Decimal('0.00002')) \
           & Attr("obs_coordinate_lat").gte(Decimal(coordinate.split(':')[0]) + Decimal('0.00002')) \
           & Attr("obs_coordinate_lat").lte(Decimal(coordinate.split(':')[0]) + Decimal('0.00002'))
