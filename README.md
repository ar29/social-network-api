# Social Network API

This is a social networking application API built with Django Rest Framework. The API supports user authentication using JSON Web Tokens (JWT) and provides functionalities for user signup, login, user search, friend requests, and managing friend lists.

## Features

- User signup and login using email and password
- JWT authentication
- Search users by email and name (paginated)
- Send, accept, and reject friend requests
- List friends and pending friend requests
- Rate limiting for sending friend requests

## Installation

### Prerequisites

- Python 3.8+
- Docker (for containerized deployment)
- PostgreSQL (if using the provided `docker-compose.yml` setup)

### Steps

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/social-network-api.git
   cd social-network-api
   ```
2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install dependencies:
    
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'social_network',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '',
        }
    }
    ```

5. Run database migrations:
    ```sh
    python manage.py migrate
    ```

6. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```sh
    python manage.py createsuperuser
    ```

### Docker Setup

- To run the project using Docker, you can use the provided Dockerfile and docker-compose.yml.

1. Build and start the containers:
    ```sh
    docker-compose up --build #This will start the Django application and a PostgreSQL database.
    ```

2. Run database migrations inside the web container:
    ```sh
    docker-compose exec web python manage.py migrate
    ```

3. Create a superuser inside the web container:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```

## Usage

### API Endpoints
- Signup: POST /api/signup/
- Login: POST /api/token/
- Token Refresh: POST /api/token/refresh/
- Search Users: GET /api/search/?query=<search_query>
- Send Friend Request: POST /api/friend-request/send/
- Respond to Friend Request: POST /api/friend-request/respond/<request_id>/
- List Friends: GET /api/friends/
- List Pending Friend Requests: GET /api/friend-requests/pending/

### Postman Collection
You can import the provided Postman collection for easy testing of the API endpoints.

#### Note
- Variables: The collection uses variables such as {{base_url}}, {{access_token}}, {{refresh_token}}, etc., to make the requests more dynamic.
- Endpoints: Each endpoint (signup, login, refresh token, search users, send friend request, respond to friend request, list friends, list pending friend requests) is defined with the appropriate method, headers, URL, and body where needed.
- Authorization: Endpoints that require authentication include the Authorization header with the Bearer {{access_token}} token.

#### Importing the Collection into Postman
1. Open Postman.
2. Click on Import in the top left corner.
3. Select the Upload Files tab.
4. Choose the social_network_api.postman_collection.json file.
5. Click Open to import the collection.
6. Using the Collection
7. Set the base_url variable to the URL of your running API (default is http://localhost:8000).
8. Signup and login to get the access_token and refresh_token.
9. Set the access_token variable in Postman using the token received from the login response.
10. Use the other endpoints by setting the appropriate variables (e.g., search_query, to_user_id, request_id, action).
11. By following these steps, you can easily test the API endpoints using Postman.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.