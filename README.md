# Endpoint manager

This is a simple tool to manage endpoints in a RESTful API.
you can signup and login to get a token to access the API.
also you can create, update, delete and list endpoints.

## Installation

```bash
docker-compose up -d
```

## Usage

### Signup

Method: POST

URL: /auth/register

Body:

```json
{
  "name": "name",
  "username": "username",
  "password": "password"
}
```

### Login

Method: POST

URL: /auth/login

Body:

```json
{
  "username": "username",
  "password": "password"
}
```

### Create endpoint

Method: POST

URL: /create/

Body:

```json
{
  "address": "address",
  "fail_limit": 1,
}
```

### User endpoints

Method: GET

URL: /user_endpoints/

### Endpoint status

Method: GET

URL: /endpoint_stats/<int:pk>/

pk : endpoint id


### Endpoint warning

Method: GET

URL: /warnings/<int:pk>/

pk : endpoint id

### Call endpoint

Method: GET

URL: /<str:endpoint>/

endpoint : endpoint address

## Documentation

### Tables

#### User

| Field | Type | Description |
| --- | --- | --- |
| id | int | user id |
| name | varchar | user name |
| username | varchar | user username |
| password | varchar | user password |
| failed_count | int | user failed count |
| created_at | datetime | user created at |
| updated_at | datetime | user updated at |

#### Endpoint

| Field | Type | Description |

| --- | --- | --- |
| id | int | endpoint id |
| address | varchar | endpoint address |
| fail_limit | int | endpoint fail limit |
| created_at | datetime | endpoint created at |
| updated_at | datetime | endpoint updated at |
| user | fk | endpoint user id |
| success_count | int | endpoint success count |
| failed_count | int | endpoint failed count |

#### Request

| Field | Type | Description |
| --- | --- | --- |
| id | int | request id |
| endpoint | fk | request endpoint id |
| created_at | datetime | request created at |
| updated_at | datetime | request updated at |
| status_code | int | request status |







