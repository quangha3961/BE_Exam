# Classes API Documentation

## Overview
This Classes API provides comprehensive management of classes and student enrollment in an educational system. It supports role-based access control where teachers can create and manage classes, while students can view their enrolled classes.

## Features
- Class Management (Create, Read, Update, Delete)
- Student Enrollment Management
- Role-based Access Control
- Search and Pagination
- Teacher and Student Views

## Prerequisites
- Django REST Framework
- JWT Authentication (from Auth API)
- MySQL Database
- User accounts with roles (teacher/student)

## Installation

### 1. Database Setup
Make sure your MySQL database is running and configured. The Classes API uses the same database as the Auth API.

### 2. Run Migrations
```bash
python manage.py makemigrations classes
python manage.py migrate
```

### 3. Start Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Base URL: `http://localhost:8000/classes/`

## Authentication
All endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 1. Class Management

### 1.1 Get All Classes / Create Class
**GET/POST** `/classes/`

#### GET - List Classes
**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `search`: Search by class name

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "className": "Lop 12A1",
                "teacher": {
                    "id": 2,
                    "email": "teacher@example.com",
                    "fullName": "Nguyen Thi B",
                    "role": "teacher",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "created_at": "2024-01-15T08:00:00Z",
                "student_count": 25,
                "exam_count": 3
            }
        ],
        "count": 1,
        "next": null,
        "previous": null,
        "page": 1,
        "total_pages": 1
    }
}
```

#### POST - Create Class (Teachers Only)
**Request Body:**
```json
{
    "className": "Lop 12A1"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "className": "Lop 12A1",
        "teacher": {
            "id": 2,
            "email": "teacher@example.com",
            "fullName": "Nguyen Thi B",
            "role": "teacher",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "created_at": "2024-01-15T08:00:00Z",
        "student_count": 0,
        "exam_count": 0
    },
    "message": "Class created successfully"
}
```

### 1.2 Get Class Detail / Update / Delete
**GET/PUT/DELETE** `/classes/{class_id}/`

#### GET - Get Class Detail
**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "className": "Lop 12A1",
        "teacher": {
            "id": 2,
            "email": "teacher@example.com",
            "fullName": "Nguyen Thi B",
            "role": "teacher",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "created_at": "2024-01-15T08:00:00Z",
        "students": [
            {
                "id": 1,
                "student": {
                    "id": 3,
                    "email": "student1@example.com",
                    "fullName": "Nguyen Van C",
                    "role": "student",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "joined_at": "2024-01-15T09:00:00Z"
            }
        ],
        "exams": []
    }
}
```

#### PUT - Update Class (Teachers Only)
**Request Body:**
```json
{
    "className": "Lop 12A1 - Updated"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "className": "Lop 12A1 - Updated",
        "teacher": {
            "id": 2,
            "email": "teacher@example.com",
            "fullName": "Nguyen Thi B",
            "role": "teacher",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "created_at": "2024-01-15T08:00:00Z",
        "students": [],
        "exams": []
    },
    "message": "Class updated successfully"
}
```

#### DELETE - Delete Class (Teachers Only)
**Response (200 OK):**
```json
{
    "success": true,
    "message": "Class deleted successfully"
}
```

### 1.3 Get My Classes
**GET** `/classes/my-classes/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "className": "Lop 12A1",
                "teacher": {
                    "id": 2,
                    "email": "teacher@example.com",
                    "fullName": "Nguyen Thi B",
                    "role": "teacher",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "joined_at": "2024-01-15T09:00:00Z",
                "exam_count": 3,
                "available_exams": 1
            }
        ],
        "count": 1,
        "next": null,
        "previous": null,
        "page": 1,
        "total_pages": 1
    }
}
```

## 2. Student Management

### 2.1 Get Class Students
**GET** `/classes/{class_id}/students/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "student": {
                    "id": 3,
                    "email": "student1@example.com",
                    "fullName": "Nguyen Van C",
                    "role": "student",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "joined_at": "2024-01-15T09:00:00Z"
            }
        ],
        "count": 1,
        "next": null,
        "previous": null,
        "page": 1,
        "total_pages": 1
    }
}
```

### 2.2 Add Student to Class
**POST** `/classes/{class_id}/students/add/`

**Request Body:**
```json
{
    "student_email": "student@example.com"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "student": {
            "id": 3,
            "email": "student@example.com",
            "fullName": "Nguyen Van C",
            "role": "student",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "joined_at": "2024-01-15T09:00:00Z"
    },
    "message": "Student added to class successfully"
}
```

### 2.3 Remove Student from Class
**DELETE** `/classes/{class_id}/students/{student_id}/`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Student removed from class successfully"
}
```

## Permissions and Access Control

### Role-based Access

#### Teachers
- Can create, read, update, and delete their own classes
- Can add and remove students from their classes
- Can view all students in their classes
- Can only manage classes they own

#### Students
- Can view classes they are enrolled in
- Can view other students in the same class
- Cannot create, update, or delete classes
- Cannot add or remove students

#### Admins
- Have full access to all operations
- Can manage any class and student relationships

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

### Common Error Messages
- `"You can only add students to your own classes"`
- `"Student with this email does not exist"`
- `"Student is already in this class"`
- `"You are not enrolled in this class"`
- `"You can only view students in your own classes"`

## Testing

### Using curl

#### Create a Class (Teacher)
```bash
curl -X POST http://localhost:8000/classes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN" \
  -d '{
    "className": "Test Class"
  }'
```

#### Get All Classes
```bash
curl -X GET http://localhost:8000/classes/ \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

#### Add Student to Class
```bash
curl -X POST http://localhost:8000/classes/1/students/add/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN" \
  -d '{
    "student_email": "student@example.com"
  }'
```

#### Get My Classes (Student)
```bash
curl -X GET http://localhost:8000/classes/my-classes/ \
  -H "Authorization: Bearer STUDENT_ACCESS_TOKEN"
```

## Database Schema

### Class Model
- `id`: Primary key
- `className`: Class name (CharField, max_length=255)
- `teacher`: Foreign key to User model
- `created_at`: Creation timestamp (auto_now_add=True)

### ClassStudent Model
- `id`: Primary key
- `class_obj`: Foreign key to Class model
- `student`: Foreign key to User model
- `joined_at`: Enrollment timestamp (auto_now_add=True)
- `unique_together`: ['class_obj', 'student'] (prevents duplicate enrollments)

## Integration Notes

### With Auth API
- Uses the same User model from accounts app
- Requires JWT authentication for all endpoints
- Role-based permissions based on user.role field

### With Future Modules
- **Exams Module**: Will integrate with exam_count and available_exams fields
- **Questions Module**: Classes may have associated question banks
- **Notifications Module**: Class-related notifications for students and teachers

## Configuration

### Pagination Settings
- Default page size: 20 items
- Maximum page size: 100 items
- Configurable via `page_size` query parameter

### Search Functionality
- Case-insensitive search by class name
- Uses `icontains` lookup for partial matches

## Security Features
- JWT token authentication required
- Role-based access control
- Object-level permissions
- Input validation and sanitization
- SQL injection protection via Django ORM
