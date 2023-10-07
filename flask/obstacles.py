import os
import base64
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal
from credentials import *

# TODO: optimize -> move to the server file and make it global

db = boto3.resource('dynamodb',
                    region_name='eu-central-1',
                    aws_access_key_id=aws_key,
                    aws_secret_access_key=aws_secret)
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

        obstacles = obstacles_table.scan(
            FilterExpression=filter_expression
        )['Items']

        for obstacle in obstacles:
            img_url = obstacle.get('img', '')  # Get the img_url attribute (assuming it's a relative path)

            # Construct the full path to the image file
            image_path = os.path.join('../static', img_url)

            try:
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()

                encoded_image = base64.b64encode(image_data).decode('utf-8')

                obstacle['img_binary'] = encoded_image

            except FileNotFoundError:
                obstacle['img_binary'] = ''

        result.extend(obstacles)

        filter_expression = getFilterExpression(polyline[0])
    
    # Initialize the S3 client
    s3 = boto3.client('s3')     
    # List objects in a bucket
    objects = s3.list_objects(Bucket='obs-images-bcg')
    # Download an image
    #images = s3.download_file('obs-images-bcg', 'obs_001.jpg', 'downloaded_image.jpg')
    s3_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': 'obs-images-bcg', 'Key': 'obs_001.jpg'},
        ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
    )

    print(f"Image URL: {s3_url}")

    return result



def getAllObstacles():
    db = boto3.resource('dynamodb',
                        region_name='eu-central-1',
                        aws_access_key_id=aws_key,
                        aws_secret_access_key=aws_secret)
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
                        aws_access_key_id=aws_key,
                        aws_secret_access_key=aws_secret)

    item = db.put_item(
        TableName='Obstacles',
        Item=transformed_data
    )
    
    return item

def getObstacleImg():
    # Initialize the S3 client
    s3 = boto3.client('s3')
    # List objects in a bucket
    objects = s3.list_objects(Bucket='your-bucket-name')
    print(objects)
    # Download an image
    img = s3.download_file('your-bucket-name', 'image.jpg', 'local-image.jpg')
    print(img)

    return "hello"


def getFilterExpression(coordinate):
    return Attr("obs_coordinate_long").between(Decimal(coordinate[1]) - Decimal('0.00002'),
                                               Decimal(coordinate[1]) + Decimal('0.00002')) \
           & Attr("obs_coordinate_lat").between(Decimal(coordinate[0]) - Decimal('0.00002'),
                                                Decimal(coordinate[0]) + Decimal('0.00002'))


def split_array(arr, chunk_size):
    for i in range(0, len(arr), chunk_size):
        yield arr[i:i + chunk_size]
