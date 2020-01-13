import boto3
import os
import json

from scope_check import scope_check

dynamodb = boto3.client('dynamodb')

def handler(event, context):
    scope_check(event, required_scopes='write:votes')
    song_name = json.loads(event['body'])['songName']
    result = dynamodb.update_item(
        TableName=os.environ['DYNAMODB_TABLE'],
        Key={
            'songName':{'S': song_name}
        },
        UpdateExpression='ADD votes :inc',
        ExpressionAttributeValues={
            ':inc': {'N': '1'}
        },
        ReturnValues="UPDATED_NEW"
    )
    response = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"votes": result["Attributes"]["votes"]["N"]})
    }
    return response
