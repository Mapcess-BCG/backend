import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# TODO: optimize -> move to the server file and make it global
db = boto3.resource('dynamodb',
                    region_name='eu-central-1',
                    aws_access_key_id='AKIAUOE65TFG6UZKDCWO',
                    aws_secret_access_key='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')
obstacles_table = db.Table('Obstacles')


def getObstaclesForPolyline(polyline):
    # TODO: optimize
    filter_expression = getFilterExpression(polyline[0])
    for index, coordinate in enumerate(polyline):
        if index % 3 == 0:
            filter_expression = filter_expression | getFilterExpression(coordinate)


    obstacles_on_the_way = obstacles_table.scan(
        FilterExpression=filter_expression
    )['Items']

    return obstacles_on_the_way


# DO we integrate Google map in the back or front?
def getAllObstaclesOnTheWay(start, end):
    db = boto3.resource('dynamodb',
                        region_name='eu-central-1',
                        aws_access_key_id='AKIAUOE65TFG6UZKDCWO',
                        aws_secret_access_key='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')
    obstacles_table = db.Table('Obstacles')
    obstacles_on_the_way = obstacles_table.scan(
        FilterExpression=(
                             Attr("obs_coordinate_long").gte(Decimal(start.split(':')[1]) + Decimal('0.00002'))
                         & Attr("obs_coordinate_long").lte(Decimal(start.split(':')[1]) + Decimal('0.00002'))
        )
    )['Items']

    return obstacles_on_the_way


def getAllObstacles():
    db = boto3.resource('dynamodb',
                    region_name='eu-central-1',
                    aws_access_key_id='AKIAUOE65TFG6UZKDCWO',
                    aws_secret_access_key='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')
    tTable = db.Table('Obstacles')
    print(tTable.scan()['Items'])

# TODO: to implement
def postObstacle():
    db = boto3.resource('dynamodb',
                    region_name='eu-central-1',
                    aws_access_key_id='AKIAUOE65TFG6UZKDCWO',
                    aws_secret_access_key='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')
    tTable = db.Table('Obstacles')



def getFilterExpression(coordinate):
    return Attr("obs_coordinate_long").between(Decimal(coordinate[1]) - Decimal('0.00002'), Decimal(coordinate[1]) + Decimal('0.00002')) \
           & Attr("obs_coordinate_lat").between(Decimal(coordinate[0]) - Decimal('0.00002'), Decimal(coordinate[0]) + Decimal('0.00002'))

