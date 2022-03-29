import json
import boto3


def handler(event, context):
    try:
        print(event)
        print('Blob ID')
        body = json.loads(event['body'])
        print(body['blob_id'])
        print('RESULT')
        print(body['result'])
        return json.dumps({"statusCode": 200})
    except:
        return json.dumps({"statusCode": 500, "body": {'error': 'Unexpected error handling request'}})
