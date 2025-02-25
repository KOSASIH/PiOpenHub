# API Documentation

## Overview

The PiOpenHub API provides a set of endpoints for interacting with the PiOpenHub application. This API allows users to manage accounts, perform transactions, and access blockchain-related functionalities.

## Base URL

```
https://api.piopenhub.com/v1
```

## Authentication

All API requests require authentication via a JSON Web Token (JWT). To obtain a token, users must log in with their credentials.

### Login Endpoint

- **URL**: `/auth/login`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
- **Response**:
    - **200 OK**:
        ```json
        {
            "token": "your_jwt_token"
        }
        ```
    - **401 Unauthorized**:
        ```json
        {
            "message": "Invalid credentials"
        }
        ```

## Endpoints

### User Management

#### Create User

- **URL**: `/users`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "secure_password"
    }
    ```
- **Response**:
    - **201 Created**:
        ```json
        {
            "id": 1,
            "username": "new_user",
            "email": "new_user@example.com"
        }
        ```
    - **400 Bad Request**:
        ```json
        {
            "message": "Validation error"
        }
        ```

#### Get User

- **URL**: `/users/{id}`
- **Method**: `GET`
- **Headers**:
    - `Authorization: Bearer your_jwt_token`
- **Response**:
    - **200 OK**:
        ```json
        {
            "id": 1,
            "username": "new_user",
            "email": "new_user@example.com"
        }
        ```
    - **404 Not Found**:
        ```json
        {
            "message": "User not found"
        }
        ```

### Transaction Management

#### Create Transaction

- **URL**: `/transactions`
- **Method**: `POST`
- **Headers**:
    - `Authorization: Bearer your_jwt_token`
- **Request Body**:
    ```json
    {
        "to": "recipient_address",
        "amount": 0.01,
        "currency": "XLM"
    }
    ```
- **Response**:
    - **201 Created**:
        ```json
        {
            "transaction_id": "txn_123456",
            "status": "pending"
        }
        ```
    - **400 Bad Request**:
        ```json
        {
            "message": "Insufficient funds"
        }
        ```

#### Get Transaction

- **URL**: `/transactions/{id}`
- **Method**: `GET`
- **Headers**:
    - `Authorization: Bearer your_jwt_token`
- **Response**:
    - **200 OK**:
        ```json
        {
            "transaction_id": "txn_123456",
            "from": "sender_address",
            "to": "recipient_address",
            "amount": 0.01,
            "currency": "XLM",
            "status": "completed"
        }
        ```
    - **404 Not Found**:
        ```json
        {
            "message": "Transaction not found"
        }
        ```

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of a request. The response body will contain a JSON object with a `message` field describing the error.

### Common Error Responses

- **400 Bad Request**: The request was invalid or cannot be served.
- **401 Unauthorized**: Authentication failed or user does not have permissions for the requested operation.
- **404 Not Found**: The requested resource could not be found.
- **500 Internal Server Error**: An unexpected error occurred on the server.

## Rate Limiting

To ensure fair usage of the API, rate limiting is enforced. Each user is allowed a maximum of 100 requests per minute. Exceeding this limit will result in a `429 Too Many Requests` response.

## Conclusion

This API documentation provides a comprehensive overview of the available endpoints and their usage. For further assistance, please contact the support team at support@piopenhub.com.
