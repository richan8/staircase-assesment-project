import json

def handler(event, context):
    body = {
        "error": "Please try the correct endpoints as per documentation"
    }
    response = {"statusCode": 400, "body": json.dumps(body)}
    return response