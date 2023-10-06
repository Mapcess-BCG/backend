import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal
from polylines import get_polylines

db = boto3.resource('dynamodb', region_name='eu-central-1')
feedback_table = db.Table('Feedback')

# get feedback along the route
def getFeedbackAlongTheRoute(polyline):
    filter_expression = getFilterExpression(polyline[0])
    for index, coordinate in enumerate(polyline):
        if index % 3 == 0:
            filter_expression = filter_expression | getFilterExpression(coordinate)


    feedback_on_path = feedback_table.scan(
        FilterExpression=filter_expression
    )['Items']

    return feedback_on_path
    '''feedback_on_route = []
    # for test purposes:
    default_origin = "BCG Düsseldorf"
    default_destination = "Curry, Hammer Str. 2, 40219 Düsseldorf"

    polylines = get_polylines(default_origin, default_destination)
    print(polylines)
    
    #iterating through polylines
    for polyline in polylines:

        filter_expression = getFilterExpression(polyline)
        #print(filter_expression)
        for index, coordinate in polyline:
            if index % 3 == 0:
                filter_expression = filter_expression | getFilterExpression(coordinate)
        
        filter_table = feedback_table.scan(
            FilterExpression=filter_expression
        )['Items']

        if(filter_table):
            feedback_on_route.append(filter_table)

    #print(feedback_on_route)

    return feedback_on_route
'''

def getFilterExpression(coordinate):
    #print(coordinate.split(':'))
    #print(Decimal(coordinate.split(':')[1]))
    #print(coordinate[1])
    return Attr("feed_coordinate_long").between(Decimal(coordinate[1]) - Decimal('0.00002'), Decimal(coordinate[1]) + Decimal('0.00002')) \
           & Attr("feed_coordinate_lat").between(Decimal(coordinate[0]) - Decimal('0.00002'), Decimal(coordinate[0]) + Decimal('0.00002'))
