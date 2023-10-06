import boto3

# DO we integrate Google map in the back or front?

def getAllObstacles():
    dynamodb = boto3.client('dynamodb', region_name='eu-central-1')
    # s3 = boto3.resource('s3',
    #                     aws_access_key_id=ACCESS_ID,
    #                     aws_secret_access_key=ACCESS_KEY)

    # Example: List all tables
    response = dynamodb.list_tables()
    print("Tables in DynamoDB:", response['TableNames'])

