import json
import os
import boto3
from botocore.config import Config
import requests

dbClient = boto3.client('dynamodb')
s3Client = boto3.client('s3', config=Config(signature_version='s3v4'))

blobsTableName = os.environ['BLOBS_TABLE']
s3BucketName = os.environ['BLOBS_BUCKET']

def handler(event, context):
    try:
        if(event['Records'][0]['eventName']=='MODIFY'):
            print(event)
            blobData = event['Records'][0]['dynamodb']['NewImage']
            if('callbackURL' in blobData):
                blobData['rekognitionResult'] = blobData['rekognitionResult']
                print('POSTING')
                print(blobData)
                requests.post(
                    blobData['callbackURL']['S'],
                    json = {
                        'blob_id': blobData['blob_id']['S'],
                        'result': json.loads(blobData['rekognitionResult']['S'])
                    }
                )
        return json.dumps({"statusCode": 200})
    except:
        return json.dumps({"statusCode": 500, "body": {'error': 'Unexpected error handling request'}})
