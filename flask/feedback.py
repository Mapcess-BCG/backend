import boto3
from boto3.dynamodb.conditions import Attr

# get feedback along the route
def getFeedbackAlongTheRoute(polylines):
    db = boto3.resource('dynamodb', region_name='eu-central-1')
    feedback_table = db.Table('Feedback')

    
    feedback_along_route = feedback_table.scan()['Items']
    return feedback_along_route