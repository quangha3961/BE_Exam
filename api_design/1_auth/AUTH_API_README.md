# Authentication API Documentation

## Overview
This authentication system is built with Django REST Framework and JWT (JSON Web Tokens) for secure user authentication and authorization.

## Features
- User Registration
- User Login with JWT tokens
- Token Refresh
- User Logout
- Profile Management
- Password Change
- Role-based access control (Student, Teacher, Admin)

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
Make sure your MySQL database is running and configured in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'exam_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Base URL: `http://localhost:8000/auth/`

### 1. User Registration
**POST** `/auth/register/`

**Request Body:**
```json
{
    "email": "student@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "fullName": "Nguyen Van A",
    "role": "student"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "email": "student@example.com",
        "fullName": "Nguyen Van A",
        "role": "student",
        "created_at": "2024-01-15T08:00:00Z",
        "last_login": null
    },
    "message": "User registered successfully"
}
```

### 2. User Login
**POST** `/auth/login/`

**Request Body:**
```json
{
    "email": "student@example.com",
    "password": "password123"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "user": {
            "id": 1,
            "email": "student@example.com",
            "fullName": "Nguyen Van A",
            "role": "student",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z"
        }
    },
    "message": "Login successful"
}
```

### 3. Refresh Token
**POST** `/auth/refresh/`

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "message": "Token refreshed successfully"
}
```

### 4. User Logout
**POST** `/auth/logout/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Logout successful"
}
```

### 5. Get Current User Profile
**GET** `/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "email": "student@example.com",
        "fullName": "Nguyen Van A",
        "role": "student",
        "created_at": "2024-01-15T08:00:00Z",
        "last_login": "2024-01-15T10:30:00Z",
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    }
}
```

### 6. Update Profile
**PUT** `/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "fullName": "Nguyen Van B",
    "email": "newemail@example.com"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "email": "newemail@example.com",
        "fullName": "Nguyen Van B",
        "role": "student",
        "created_at": "2024-01-15T08:00:00Z",
        "last_login": "2024-01-15T10:30:00Z"
    },
    "message": "Profile updated successfully"
}
```

### 7. Change Password
**POST** `/auth/change-password/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "old_password": "password123",
    "new_password": "newpassword123",
    "new_password_confirm": "newpassword123"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Password changed successfully"
}
```

## Authentication

### JWT Token Usage
1. After login, you'll receive an `access` token and a `refresh` token
2. Include the `access` token in the Authorization header for protected endpoints:
   ```
   Authorization: Bearer <access_token>
   ```
3. When the access token expires, use the refresh token to get a new access token
4. The access token expires in 1 hour, refresh token expires in 7 days

### User Roles
- **student**: Regular student user
- **teacher**: Teacher with additional permissions
- **admin**: Administrator with full access

## Error Responses

All error responses follow this format:
```json
{
    "success": false,
    "errors": {
        "field_name": ["Error message"]
    },
    "message": "Error description"
}
```

### Common HTTP Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error



### Using curl
```bash
# Register
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "password_confirm": "testpassword123",
    "fullName": "Test User",
    "role": "student"
  }'

# Login
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'

# Get Profile (replace ACCESS_TOKEN with actual token)
curl -X GET http://localhost:8000/auth/profile/ \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## Security Features
- Password validation using Django's built-in validators
- JWT tokens with configurable expiration
- Token blacklisting on logout
- CORS protection
- Email uniqueness validation
- Secure password hashing

## Configuration

### JWT Settings (in settings.py)
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}
```

### CORS Settings
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

## Database Schema

### User Model
- `id`: Primary key
- `email`: Unique email address (used for login)
- `username`: Username (auto-generated from email)
- `fullName`: User's full name
- `role`: User role (student/teacher/admin)
- `password`: Hashed password
- `created_at`: Account creation timestamp
- `last_login`: Last login timestamp
- `is_active`: Account status
- `is_staff`: Staff status
- `is_superuser`: Superuser status
