# Post service

---

### GET `/post/get_post/?{post_id: int}`

Gets the post object corresponding to the unique post id provided.  

Authorization is required if the post is **private**.  

Params:
```py
post_id: int # Required
req_creation_date: bool = False # If true, returns post creation date
req_user: bool = False # If true, returns full user object instead of just username
```

Required headers:
```py
"Authorization: YOUR_JWT_HERE" # Required if post is private
```
<br/>

Responses:  
`RESPONSE 200 - OK`

```json
{
    "message": "Post found",
    "post": {
        "id": 1,
        "title": "Example Title",
        "body": "Example Body",
        "status": "PUBLIC"
    },
    "user": "exampleuser"
}
```

If `req_user=true`:

```json
{
    "message": "Post found",
    "post": {
        "id": 1,
        "title": "Example Title",
        "body": "Example Body",
        "status": "PUBLIC"
    },
    "user": {
        "id": 123,
        "username": "exampleuser",
        "name": "John"
    }
}
```
<br/>

`RESPONSE 400 - Bad Request`

```json
{
    "message": "`post_id` parameter is necessary"
}
```
<br/>

`RESPONSE 401 - Unauthorized`

```json
{
    "message": "You are not authorized to view this post"
}
```
<br/>

`RESPONSE 404 - Not Found`

```json
{
    "message": "Post not found"
}
```
<br/>

`RESPONSE 500 - Internal Server Error`

```json
{
    "message": "Error while getting post: {error}"
}
```

---

### POST `/post/create_post/`

Endpoint responsible for creating a new post.  

Required body:
```json
{
    "title": "Example Title",
    "body": "Example Body",
    "status": "PUBLIC"
}
```

Required headers:
```py
"Authorization: YOUR_JWT_HERE"
```
<br/>

Responses:  
`RESPONSE 201 - Created`

```json
{
    "message": "Successfully created post",
    "post": {
        "id": 123,
        "title": "Example Title",
        "body": "Example Body",
        "status": "PUBLIC"
    }
}
```
<br/>

`RESPONSE 401 - Unauthorized`

```json
{
    "message": "You are not authorized to create posts"
}
```
<br/>

`RESPONSE 500 - Internal Server Error`

```json
{
    "message": "Error while creating post: {e}"
}
```

---

### PUT `/post/edit_post/`

Endpoint responsible for editing an existing post.  
User can only edit their own posts.

Required body:
```json
{
    "id": 123,
    "title": "Updated Title",
    "body": "Updated Body",
    "status": "PRIVATE"
}
```

Required headers:
```py
"Authorization: YOUR_JWT_HERE"
```
<br/>

Responses:  
`RESPONSE 200 - OK`

```json
{
    "message": "Successfully edited post",
    "post": {
        "id": 123,
        "title": "Updated Title",
        "body": "Updated Body",
        "status": "PRIVATE"
    }
}
```
<br/>

`RESPONSE 401 - Unauthorized`

```json
{
    "message": "You are not authorized to edit this post"
}
```
<br/>

`RESPONSE 404 - Not Found`

```json
{
    "message": "Post not found"
}
```
<br/>

`RESPONSE 500 - Internal Server Error`

```json
{
    "message": "Error while editing post: {e}"
}
```

---

### DELETE `/post/delete_post/?{post_id: int}`

Deletes an existing post.  
User can only delete their own posts.  

Params:
```py
post_id: int # Required
```

Required headers:
```py
"Authorization: YOUR_JWT_HERE"
```
<br/>

Responses:  
`RESPONSE 200 - OK`

```json
{
    "message": "Successfully deleted post"
}
```
<br/>

`RESPONSE 401 - Unauthorized`

```json
{
    "message": "You are not authorized to delete this post"
}
```
<br/>

`RESPONSE 404 - Not Found`

```json
{
    "message": "Post not found"
}
```
<br/>

`RESPONSE 500 - Internal Server Error`

```json
{
    "message": "Error while deleting post: {e}"
}
```
