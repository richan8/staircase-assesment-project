from asyncio import constants
import json
import os
import boto3
import uuid
from botocore.config import Config

dbClient = boto3.client('dynamodb')
s3Client = boto3.client('s3', config=Config(signature_version='s3v4'))

blobsTableName = os.environ['BLOBS_TABLE']
s3BucketName = os.environ['BLOBS_BUCKET']

def handler(event, context):
    #try:
    print(event)

    blobId = event['pathParameters']['blob_id']

    dbRes = dbClient.get_item(
        TableName=blobsTableName,
        Key={
            "blob_id": {
                "S": blobId
            }
        }
    )

    if('Item' in dbRes):
        dbRes = dbRes['Item']

        blobData = {
            'blob_id': dbRes['blob_id']['S']
        }

        if('rekognitionResult' in dbRes):
            blobData['result'] = json.loads(dbRes['rekognitionResult']['S'])

        if('callbackURL' in dbRes):
            blobData['callbackURL'] = dbRes['callbackURL']['S']

        return json.dumps({
            "statusCode": 200, 
            "body": blobData
        })
    else:
        return json.dumps({"statusCode": 404, "body": {'error': f'No blob found with id {blobId}'}})
        
    #except:
    #    return json.dumps({"statusCode": 500, "body": {'error': 'Unexpected error handling request'}})
