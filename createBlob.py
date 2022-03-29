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
    try:
        blobId = str(uuid.uuid4())

        newBlobData = {
            "blob_id": {
                "S": blobId
            }
        }

        try:
            if('body' in event):
                reqBody = json.loads(event['body'])
                if('callback_url' in reqBody):
                    newBlobData['callbackURL'] = {
                        "S": str(reqBody['callback_url'])
                    }
        except:
            return json.dumps({"statusCode": 400, "body": {'error': 'Request body could not be parsed'}})

        dbClient.put_item(
            TableName = blobsTableName,
            Item = newBlobData
        )

        signedURL = s3Client.generate_presigned_url(
                ClientMethod='put_object', 
                Params={
                    "Bucket" : s3BucketName,
                    "Key" : blobId
                },
                ExpiresIn = 3600,
                HttpMethod = 'PUT'
            )

        return(
            json.dumps({
                "statusCode": 200, 
                "body": {
                    'blob_id': blobId,
                    'signedURL': signedURL
                }
            })
        )
        
    except:
        return json.dumps({"statusCode": 500, "body": {'error': 'Unexpected error handling request'}})
