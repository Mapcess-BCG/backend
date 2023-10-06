import os

import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# TODO: optimize -> move to the server file and make it global
db = boto3.resource('dynamodb',
                    region_name='eu-central-1',
                    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
obstacles_table = db.Table('Obstacles')


def getObstaclesForPolyline(polyline):
    # TODO: optimize
    result = []
    filter_expression = getFilterExpression(polyline[0])

    chunk_size = 50

    # Split the original array into multiple partitions
    partitions = list(split_array(polyline, chunk_size))

    for partition in partitions:
        for index, coordinate in enumerate(partition):
            filter_expression = filter_expression | getFilterExpression(coordinate)

        result.extend(obstacles_table.scan(
            FilterExpression=filter_expression
        )['Items'])

        filter_expression = getFilterExpression(polyline[0])

    return result


def getAllObstacles():
    db = boto3.resource('dynamodb',
                        region_name='eu-central-1',
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    tTable = db.Table('Obstacles')
    print(tTable.scan()['Items'])


def postObstacle(obstacle):
    transformed_data = {
        "id": {"S": obstacle["id"]},
        "obs_comment": {"S": obstacle["obs_comment"]},
        "obs_coordinate_lat": {"N": obstacle["obs_coordinate_lat"]},
        "obs_coordinate_long": {"N": obstacle["obs_coordinate_long"]},
        "obs_created": {"S": obstacle["obs_created"]},
        "obs_resolved": {"S": obstacle["obs_resolved"]},
        "obs_type": {"S": obstacle["obs_type"]}
    }
    
    db = boto3.client('dynamodb',
                        region_name='eu-central-1',
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    item = db.put_item(
        TableName='Obstacles',
        Item=transformed_data
    )

    return item


def getFilterExpression(coordinate):
    return Attr("obs_coordinate_long").between(Decimal(coordinate[1]) - Decimal('0.00002'),
                                               Decimal(coordinate[1]) + Decimal('0.00002')) \
           & Attr("obs_coordinate_lat").between(Decimal(coordinate[0]) - Decimal('0.00002'),
                                                Decimal(coordinate[0]) + Decimal('0.00002'))


def split_array(arr, chunk_size):
    for i in range(0, len(arr), chunk_size):
        yield arr[i:i + chunk_size]
