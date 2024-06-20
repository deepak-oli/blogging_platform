# FastAPI Blogging Platform Backend API

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [API Endpoints](#api-endpoints)
7. [Authentication](#authentication)
8. [Database Migrations](#database-migrations)
9. [Further work](#further-work)

## Introduction
This is a comprehensive backend API for a blogging platform built using FastAPI. It includes features like basic role-based authentication, user management, posts, categories, comments, and like functionalities.

## Features
- Role-based authentication
- User management
- Posts
- Categories
- Comments
- Likes

## Installation
To get started with this project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/deepak-oli/blogging_platform.git
    cd blogging_platform
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
Create a `.env` file in the root directory and add the following environment variables:
```env
SECRET_KEY="your_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL="sqlite:///./blog_platform.db"
ADMIN_PASSWORD="Test"
ADMIN_EMAIL="test@example.com"
```

## Running the Application
To run the application, execute the following command:
```bash
uvicorn app.main:app --reload
```
The application will be accessible at `http://127.0.0.1:8000` and full Swagger documentation will be at `http://127.0.0.1:8000/docs`

## API Endpoints
Here are some of the primary API endpoints available in this application:

### Authentication
- `POST /login`: Login a user and obtain a token.
- `POST /register`: Register a new user.

### Users
- `GET /users/`: Get a list of all users.
- `GET /users/{user_id}`: Get details of a specific user.
- `PUT /users/{user_id}`: Update a specific user.
- `DELETE /users/{user_id}`: Delete a specific user.

### Posts
- `GET /posts/`: Get a list of all posts.
- `POST /posts/`: Create a new post.
- `GET /posts/{post_id}`: Get details of a specific post.
- `PUT /posts/{post_id}`: Update a specific post.
- `DELETE /posts/{post_id}`: Delete a specific post.

### Categories
- `GET /categories/`: Get a list of all categories.
- `POST /categories/`: Create a new category.
- `GET /categories/{category_id}`: Get details of a specific category.
- `PUT /categories/{category_id}`: Update a specific category.
- `DELETE /categories/{category_id}`: Delete a specific category.

### Comments
- `GET /posts/{post_id}/comments/`: Get all comments for a post.
- `POST /posts/{post_id}/comments/`: Add a comment to a post.
- `PUT /comments/{comment_id}`: Update a comment.
- `DELETE /comments/{comment_id}`: Delete a comment.

### Likes
- `POST /like/{post_id}/`: Like a post.
- `POST /unlike/{post_id}/unlike`: Unlike a post.
- `POST /likes/{post_id}/`: Get a post's like count.
- `POST /user-likes/{post_id}/unlike`: Get User Liked posts

## Authentication
The API uses JWT (JSON Web Tokens) for authentication. To access protected routes, include the token in the Authorization header:
```bash
Authorization: Bearer <token>
```

## Database Migrations
This project uses Alembic for database migrations. To run migrations, use:

First, add your db url to sqlalchemy.url in alembic.ini file `sqlalchemy.url = sqlite:///blog_platform.db` then, run

```bash
alembic upgrade head
```
To create a new migration, use:
```bash
alembic revision --autogenerate -m "Migration message"
```
## Further work
- Testing using `pytest`
- Build Frontend using `Next.js`

---
