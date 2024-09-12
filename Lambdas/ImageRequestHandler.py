import json

import boto3

dynamodb_client = boto3.resource("dynamodb")

def get_image_name(event):
    if "imageName" in event["queryStringParameters"]:
        return event["queryStringParameters"]["imageName"]
    return None

def lambda_handler(event, context):
    
    image_name = get_image_name(event)
    
    if not image_name:
        return {
        'statusCode': 400,
        'body': 'bad request'
    }
    
    validation_table = dynamodb_client.Table("ValidationRequests")
    
    get_response = validation_table.get_item(Key={"FileName": image_name})
    item = None
    if "Item" in get_response:
        item = get_response["Item"]
    
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }