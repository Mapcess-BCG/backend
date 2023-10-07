import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal
from credentials import *
from polylines import get_polylines

db = boto3.resource('dynamodb',
                    region_name='eu-central-1',
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret)
db_client = boto3.client('dynamodb',
                        region_name='eu-central-1',
                        aws_access_key_id=aws_key,
                        aws_secret_access_key=aws_secret)
feedback_table = db.Table('Feedback')

# get feedback along the route
def getFeedbackAlongTheRoute(polyline):
    result = []
    filter_expression = getFilterExpression(polyline[0])

    chunk_size = 50

    # Split the original array into multiple partitions
    partitions = list(split_array(polyline, chunk_size))

    for partition in partitions:
        for index, coordinate in enumerate(partition):
            filter_expression = filter_expression | getFilterExpression(coordinate)

        result.extend(feedback_table.scan(
            FilterExpression=filter_expression
        )['Items'])
        filter_expression = getFilterExpression(polyline[0])

    return result

def postFeedback(data):
    transformed_data = {
        "id": {"S": data['id'] },
        "feed_comment": {"S": data['feed_comment']},
        "feed_coordinate_lat": {"N": data["feed_coordinate_lat"]},
        "feed_coordinate_long": {"N": data["feed_coordinate_long"]},
        "feed_created": {"S": data["feed_created"]},
        "feed_problem": {"S": data["feed_problem"]},
        "feed_score": {"S": data["feed_score"]}
    }

    feedback = db_client.put_item(TableName='Feedback', 
                       Item=transformed_data)
    return feedback

def getFilterExpression(coordinate):
    #print(coordinate.split(':'))
    #print(Decimal(coordinate.split(':')[1]))
    #print(coordinate[1])
    return Attr("feed_coordinate_long").between(Decimal(coordinate[1]) - Decimal('0.00002'), Decimal(coordinate[1]) + Decimal('0.00002')) \
           & Attr("feed_coordinate_lat").between(Decimal(coordinate[0]) - Decimal('0.00002'), Decimal(coordinate[0]) + Decimal('0.00002'))

def split_array(arr, chunk_size):
    for i in range(0, len(arr), chunk_size):
        yield arr[i:i + chunk_size]