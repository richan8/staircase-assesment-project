import json
import os
import boto3

dbClient = boto3.client('dynamodb')
rekClient = boto3.client('rekognition')

blobsTableName = os.environ['BLOBS_TABLE']
s3BucketName = os.environ['BLOBS_BUCKET']


def handler(event, context):
    try:
        print(event)
        
        s3Data = event['Records'][0]['s3']
        blobId = s3Data['object']['key']
        
        blobData = dbClient.get_item(
            TableName=blobsTableName,
            Key={
                "blob_id": {
                    "S": blobId
                }
            }
        )

        if('Item' in blobData):
            resBlobData = blobData['Item']
            
            rekRes = rekClient.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': s3BucketName,
                        'Name': blobId,
                    }
                },
                MaxLabels=16
            )
            
            if('Labels' in rekRes):
                resBlobData['rekognitionResult'] = {
                    "S": json.dumps(rekRes)
                }
            else:
                resBlobData['err'] = {
                    "S": 'No Labels generated'
                }
            
            dbClient.put_item(
                TableName = blobsTableName,
                Item = resBlobData
            )

            print({
                's3Data':s3Data, 
                'Labels':rekRes
            })

            return( json.dumps({"statusCode": 200}) )
        else:
            return json.dumps({"statusCode": 500, "body": event})
    except:
        return json.dumps({"statusCode": 500, "body": {'error': 'Unexpected error handling request'}})
