# Staircase assesment project
# Notes
- The architecture diagram for part 1 is available in this repo as `arch-part-1.svg`
- For part 2, I tried to follow the given architecture as closely as possible. However, I ran into problems trying to connect API Gateway directly to Dynamo.
  - I understand it is supposed to be implemented using API Gateway Service Proxies.
  - I attempted to use the plugin: `serverless-apigateway-service-proxy`, its `serverlessyaml` configuration is commented out in `custom.apiGatewayServiceProxies`. 
  - The issue was in trying to get the plugin to deploy properly. Due to personal time constraints, I could not dedicate alot of time to getting it to work
  - To implement the `GET /blobs/{blob_id}` endpoint, I have instead created a Lambda trigger similar to `POST /blobs/`

# Endpoints
## **`POST`** /blobs
Creates of new blob in db and returns URL for file upload
### Request Body (OPTIONAL)
```json
"body": {
  "callback_url": "<URL STRING>"
}
```
### Response Body
```json
"body": {
  "blob_id": "<STRING>",
  "signedURL": "<STRING URL>"
}
```
---
## **`PUT`** `signedURL`
- Uploads file into S3.
- Supported filetypes: `.png`, `.jpeg`
- Returns HTTP Status code
---
## **`GET`** /blobs/{blob_id}
- Fetches blobInfo for blob with id: `blob_id`
#### Response Body
```json
"body": {
    "blob_id": "<STRING>",
    "result": "<JSON OBJECT>",
    "callbackURL": "<STRING URL>"
}
```
- `result` populates only if image was successfully processed by Rekognition
- `callbackURL` populates only if provided for the blob
---
## **`POST`** /test_callback
- Not a part of the assesment
- Used to test the API's
### Request Body
```json
"body": {
    "blob_id": "<STRING>",
    "result": "<JSON OBJECT>",
}
```
# Callbacks
## On successful label detection by AWS Rekognition
#### Body
```json
"body": {
    "blob_id": "<STRING>",
    "result": "<JSON OBJECT>"
}
```
---