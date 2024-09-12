import datetime
import json

import boto3
from botocore.exceptions import ClientError

rekognition_client = boto3.client("rekognition")
dynamodb_client = boto3.resource("dynamodb")

BUCKET_NAME = "recognition-service-images"

min_confidence_threshhold = 90

criteria = {
    "Smile": [False, min_confidence_threshhold],
    "Sunglasses": [False, min_confidence_threshhold],
    "EyesOpen": [True, min_confidence_threshhold],
    "MouthOpen": [False, min_confidence_threshhold]
}

def parse_file_name(event):
    return event["Records"][0]["s3"]["object"]["key"]
    
def evaluate_rekognition_response(image_values):
    
    failure_reasons = []
    
    for attribute, threshholds in criteria.items():
        if image_values[attribute]["Value"] != threshholds[0] or image_values[attribute]["Confidence"] < threshholds[1]:
            failure_reasons.append(attribute)
        
    return failure_reasons
    
def store_result(file_name, result, face_details):
    
    item = {
        "FileName": file_name,
        "ValidationResult": result["Result"],
        "FailureResons": result["FailureReasons"],
        "Timestamp": datetime.datetime.now().replace(microsecond=0).isoformat(),
        "FileLocation": BUCKET_NAME + "/" + file_name,
        "FaceDetails": json.dumps(face_details)
    }
    
    validation_table = dynamodb_client.Table("ValidationRequests")
    
    try:
        validation_table.put_item(Item=item)
    except ClientError as err:
        print(err)

def lambda_handler(event, context):

    file_name = parse_file_name(event)
    
    response = rekognition_client.detect_faces(
        Image={
            "S3Object": {
                "Bucket": BUCKET_NAME,
                "Name": file_name
            }
        },
        Attributes=['ALL']
    )
    
    face_details = response["FaceDetails"][0]
    
    important_face_details = {}
    
    for attribute in criteria.keys():
        important_face_details[attribute] = face_details[attribute]
    
    failure_reasons = evaluate_rekognition_response(important_face_details)
    
    result = {
        "Result": "Pass" if len(failure_reasons) == 0 else "Fail",
        "FailureReasons": failure_reasons
    }
    
    store_result(file_name, result, important_face_details)