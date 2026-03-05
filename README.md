Mini SaaS Backend API

About the Project

This project is a backend API built using FastAPI.
It allows users to register, log in, create projects, and manage jobs under those projects.

The goal of this project was to implement a clean backend structure with authentication, database integration, and a service layer for handling business logic.

The application uses PostgreSQL/SQLite for database operations and Redis for caching related functionality.

Technologies Used

FastAPI
SQLAlchemy
PostgreSQL
SQLite
Redis
JWT Authentication
Pydantic
Uvicorn

Project Structure

The project is organized into different folders to keep the code clean and easy to maintain.

app/

core

auth.py – Handles authentication logic
security.py – Password hashing and JWT token utilities

models

user.py – User database model
project.py – Project database model
job.py – Job database model

routes

auth_routes.py – APIs related to user authentication
project_routes.py – APIs for managing projects
job_routes.py – APIs for managing jobs
analytics_routes.py – APIs for analytics

schemas

user_schema.py – User request and response schemas
project_schema.py – Project schemas
job_schema.py – Job schemas

services

user_service.py – Business logic related to users
project_service.py – Business logic for projects
job_service.py – Business logic for jobs
analytics_service.py – Analytics related logic
redis_service.py – Redis related functionality

Other important files

database.py – Database connection configuration
dependencies.py – Shared dependencies used across routes
main.py – Entry point of the FastAPI application

Installation Steps

1. Clone the repository
git clone <repository-url>

2. Create a virtual environment
python -m venv venv

3. Activate the environment
Windows
venv\Scripts\activate

Mac/Linux
source venv/bin/activate

4. Install dependencies
pip install -r requirements.txt

5. Run the server
uvicorn app.main:app --reload

The server will start at:
http://127.0.0.1:8000

API Documentation
FastAPI automatically provides API documentation.

Swagger UI
http://127.0.0.1:8000/docs

Main Features

User registration and login
JWT based authentication
Project creation and management
Job creation and management
Redis integration
Organized layered architecture

Dependencies

| Package         | Purpose                              |
| --------------- | ------------------------------------ |
| fastapi         | Framework used to build the API      |
| uvicorn         | Server used to run FastAPI           |
| sqlalchemy      | ORM used for database operations     |
| pydantic        | Data validation for request/response |
| python-jose     | Used for JWT authentication          |
| passlib[bcrypt] | Used for password hashing            |
| psycopg2-binary | PostgreSQL database driver           |
| redis           | Used for caching functionality       |
| python-dotenv   | Used to load environment variables   |

Note: SQLite is built into Python, so it does not require a separate dependency.

Author
Simran Kamboj