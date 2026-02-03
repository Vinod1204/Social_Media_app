# FastAPI Social Media App

A social media API built with FastAPI, SQLAlchemy, and PostgreSQL. This application allows users to create accounts, authenticate, and manage posts.

## Features

- User registration and authentication using OAuth2
- CRUD operations for posts
- PostgreSQL database integration
- Password hashing with bcrypt
- JWT token-based authentication
- Pydantic schemas for data validation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Vinod1204/Social_Media_app.git
   
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL database:
   - Create a database named `fastapi`
   - Update the database connection details in `app/main.py` if necessary

5. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## Usage

### API Endpoints

#### Authentication
- `POST /login` - User login (returns access token)

#### Posts
- `GET /posts` - Get all posts
- `POST /posts` - Create a new post (requires authentication)
- `GET /posts/{id}` - Get a specific post
- `PUT /posts/{id}` - Update a post (requires authentication)
- `DELETE /posts/{id}` - Delete a post (requires authentication)

#### Users
- User-related endpoints are handled through authentication

### Example Requests

#### Create a Post
```bash
curl -X POST "http://localhost:8000/posts" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your-token>" \
     -d '{"title": "My Post", "content": "This is my post content", "published": true}'
```

#### Login
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@example.com&password=password"
```

## Database Models

### Post
- id: Integer (Primary Key)
- title: String
- content: String
- published: Boolean
- created_at: Timestamp

### User
- id: Integer (Primary Key)
- email: String (Unique)
- password: String (Hashed)
- created_at: Timestamp

## Authentication

The application uses OAuth2 with JWT tokens for authentication. After logging in, include the access token in the Authorization header as `Bearer <token>` for protected endpoints.

## Dependencies

Key dependencies include:
- FastAPI
- SQLAlchemy
- psycopg2
- Pydantic
- bcrypt
- python-jose

See `requirements.txt` for the full list.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
