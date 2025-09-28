# User service

---

### GET `/api/get_user/{user_id: int}`

Gets the user object corresponding to the unique user id provided

Params:
```py
user_id: int # Required
req_name: bool = False # If true, returns name of user
req_creation_date: bool = False # If true, returns creation date of account
```
<br/>

Responses:
`RESPONSE 200 - OK`

```json
{
    "message": "User found",
    "user": {
        "id": 1,
        "username": "exampleuser"
    }
}
```
<br/>

`RESPONSE 400 - Bad Request`
This is issued when the user_id parameter is not passed

```json
{
    "message": "`user_id` parameter is necessary"
}
```
<br/>

`RESPONSE 404 - Not Found`
This request happens when a user with the provided user_id doesn't exist

```json
{
    "message": "User not found"
}
```
<br/>

`RESPONSE 500 - Internal server error`
This request can be caused by a number of issues

```json
{
    "message": "An error occured: {error}"
}
```

---

### POST `/api/register_user/`
Endpoint responsible for registering a user

Request body:
```json
{
    "username": "exampleuser",
    "password": "sEcurePaSSword123"
}
```
<br />

Responses:
`RESPONSE 201 - Successfully created`
```json
{
    "message": "User created and logged in",
    "user": {
        "id": 123,
        "username": "exampleuser"
    },
    "token": "JWT TOKEN HERE"
}
```
Note: `token` field is a JWT token used for authenticating the user
<br />

`RESPONSE 400 - Bad Request`
Can be cause by 2 cases:
1. One of the needed parameters wasn't provded
2. User with such username already exists
```json
{
    "message": "Username and password required"
}
```
OR
```json
{
    "message": "User with such username already exists"
}
```
<br/>

`RESPONSE 500 - Internal server error`
This request can be caused by a number of issues

```json
{
    "message": "An error occured: {error}"
}
```

---

### POST `/api/login/`
Endpoint responsible for logging in a user

Request body:
```json
{
    "username": "exampleuser",
    "password": "sEcurePaSSword123"
}
```
<br />

`RESPONSE 200 - OK`

```json
{
    "message": "User logged in",
    "user": {
        "id": 123,
        "username": "exampleuser"
    },
    "token": "JWT TOKEN HERE"
}
```

Note: `token` field is a JWT token used for authenticating the user
<br />

`RESPONSE 400 - Bad Request`
Can be cause by 2 cases:
1. One of the needed parameters wasn't provded
2. Credentials don't match any user

```json
{
    "message": "Username and password required"
}
```
OR
```json
{
    "message": "Incorrect credentials"
}
```
<br/>

`RESPONSE 500 - Internal server error`
This request can be caused by a number of issues

```json
{
    "message": "An error occured: {error}"
}
```