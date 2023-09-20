
# Degree Verification API Documentation

## Introduction

The Degree Verification API allows you to verify academic degrees from images. The API accepts a POST request with an image file and returns a JSON response with the "verified" keyword indicating whether the degree is valid or not.

- **Base URL:** http://127.0.0.1:5000 (Localhost currently)

## Verify Degree

### Endpoint

- **URL:** `/verify`

### Request

- **Method:** POST
- **Headers:** `Content-Type: multipart/form-data`

#### Request Body

- The request body should include a file field with the image of the degree to be verified. The key for the file field should be "file".

#### Example Request

```http
POST http://127.0.0.1:5000/verify
Headers:
    Content-Type: multipart/form-data
Body:
    - file: <Image File>
```

### Response

- **HTTP Status Code:** 200 OK on success.

#### Response Body

- The response body is a JSON object with the "verified" keyword and a string value of "True" or "False" indicating whether the degree is verified.

```json
{
    "verified": "True"
}
```

#### Example Response

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
    "verified": "True"
}
```

- If the degree is verified successfully, the response will have `"verified": "True"`.
- If the degree is not verified, the response will have `"verified": "False"`.

## Error Handling

- In case of errors, the API will return the appropriate HTTP status code .

## Notes

- Make sure to provide a valid image file for verification.
- The API responds with a JSON object containing the "verified" keyword indicating the verification status.
- The API expects the request headers to have `Content-Type: multipart/form-data`.

This API documentation provides an overview of the endpoints, request and response formats, error handling, and important notes for using the Degree Verification API. Make sure to replace the base URL with the actual URL where your API is hosted.