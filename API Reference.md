## Casting Agency API
The Casting Agency API provides an interface for managing
actor and movie information. The API supports creating,
viewing, searching, and deleting actors and movies.

### Getting Started
- Base URL
    - When run locally, the API can be accessed at 
      `http://localhost:5000`.
    - A hosted application can be accessed at
      `https://fsnd-casting-api.herokuapp.com/`
- Authentication
    - The API uses Bearer token authentication
      that is provided through the `Authorization` header
      with the format `Bearer {token_value}`
- Media Types
    - The API only support JSON and expects the `Content-Type`
      header to contain `application/json`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": false,
    "description": "A description of the error."
}
```

Validation errors contain an additional `invalid_params` key
with an array of objects in the following format:
```
{
    "success": false,
    "message": "The request parameters are not valid.",
    "invalid_params": [
        {
            "name": "birthdate",
            "reason": "Unknown field."
        }
    ]
}
``` 

Each validation error provides an attribute name and the reason
the attribute is invalid.

The API can respond to requests with the following HTTP status codes:
- 400: Bad Request
- 404: Not Found
- 405: Method Not Allowed
- 500 Internal Server Error

### Endpoints
Upon a succesful request, the JSON body will contain a `success` key
with a boolean value of `true`. Any request with an error will hold a value of `false`
in the `success` key.

### GET /actors
- Fetches a list of actors.
- Request Arguments:
    - None
- Example:
    - Request Path
        - `http://localhost:5000/actors`
    - Response Body
        ```
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "name": "Tom Hanks",
                    "age": 64,
                    "gender": "male",
                    "movies": [
                        {
                            "id": 1,
                            "title": "Forrest Gump",
                            "release_date": "1994-07-06T00:00:00"
                        }
                    ]
                }
            ]
        }
        ```

### GET /movies
- Fetches a list of movies.
- Request Arguments:
    - None
- Example:
    - Request Path
        - `http://localhost:5000/movies`
    - Response Body
        ```
        {
            "success": true,
            "data": [
                {
                    "id": 1,
                    "title": "Forrest Gump",
                    "release_date": "1994-07-06T00:00:00",
                    "actors": [
                        {
                            "id": 1,
                            "name": "Tom Hanks",
                            "age": 64,
                            "gender": "male"
                        }
                    ]
                }
            ]
        }
        ```

### POST /actors
- Creates an actor resource.
- Request Body Parameters:
    - name
        - The name of the actor.
    - age
        - The age of the actor.
    - gender
        - The gender of the actor.
    - movies (optional)
        - A list of movie ids the actor 
          will be added to.
- Example:
    - Request Path
        - `http://localhost:5000/actors`
    - Request Body
        ```
        {
            "name": "Diane Keaton",
            "age": 74,
            "gender": "female",
        }
        ```
    - Response Body
        ```
        {
            "success": true,
            "data": [
                {
                    "id": 4,
                    "name": "Diane Keaton",
                    "age": 74,
                    "gender": "female",
                    "movies": []
                }
            ]
        }
        ```

### POST /movies
- Creates a movie resource.
- Request Body Parameters:
    - title
        - The name of the movie.
    - release_date
        - A timestamp of the date and time
          the movie was or will be released
          shown in theaters. 
        - If there is no
          specific time for the release,
          then the hour, minutes, and seconds
          can be left as zeros.
    - actors (optional)
        - A list of actor ids that will be
          added to the movie cast.
- Example:
    - Request Path
        - `http://localhost:5000/movies`
    - Request Body
        ```
        {
            "title": "The Godfather: Part II",
            "release_date": "1974-12-18T00:00:00"
        }
        ```
    - Response Body
        ```
        {
            "success": true,
            "data": [
                {
                    "id": 3,
                    "title": "The Godfather: Part II",
                    "release_date": "1974-12-18T00:00:00",
                    "actors": []
                }
            ]
        }
        ```

### PATCH /actors/{actor_id}
- Updates specific attributes on an actor resource.
- Request Body Parameters:
    - name (optional)
        - The name of the actor.
    - age (optional)
        - The age of the actor.
    - gender (optional)
        - The gender of the actor.
    - movies (optional)
        - A list of movie ids the actor 
          will be added to.
- Example:
    - Request Path
        - `http://localhost:5000/actors/4`
    - Request Body
        ```
        {
            "age": 75
        }
        ```
    - Response Body
        ```
        {
            "success": true,
            "data": [
                {
                    "id": 4,
                    "name": "Diane Keaton",
                    "age": 75,
                    "gender": "female",
                    "movies": []
                }
            ]
        }
        ```

### PATCH /movies/{movie_id}
- Updates specific attributes on a movie resource.
- Request Body Parameters:
    - title (optional)
        - The name of the movie.
    - release_date (optional)
        - A timestamp of the date and time
          the movie was or will be released
          shown in theaters.
    - actors (optional)
        - A list of actor ids that will be
          added to the movie cast.
- Example:
    - Request Path
        - `http://localhost:5000/movies/3`
    - Request Body
        ```
        {
            "title": "The Godfather: Part 2"
        }
        ```
    - Response Body
        ```
        {
            "success": true,
            "data": [
                {
                    "id": 3,
                    "title": "The Godfather: Part 2",
                    "release_date": "1974-12-18T00:00:00",
                    "actors": []
                }
            ]
        }
        ```

### DELETE /actors/{actor_id}
- Removes an actor with the provided id.
- Path Parameters:
    - actor_id
- Example
    - Request Path
        - `http://localhost:5000/actors/4`
    - Response Body
        ```
        {
            "success": true,
            "id": 4
        }
        ```

### DELETE /movies/{movie_id}
- Removes a movie with the provided id.
- Path Parameters
    - movie_id
- Example
    - Request Path
        - `http://localhost:5000/movies/3`
    - Response Body
        ```
        {
            "success": true,
            "id": 3
        }
        ```