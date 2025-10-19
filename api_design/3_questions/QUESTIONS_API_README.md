# Questions API Documentation

## Overview
This Questions API provides comprehensive management of questions and answers in an educational system. It supports role-based access control where teachers can create, update, and delete questions and their answers, while maintaining proper authentication and authorization.

## Features
- Question Management (Create, Read, Update, Delete)
- Answer Management (Add, Update, Delete)
- Role-based Access Control (Teacher-only operations)
- Search and Filtering
- Pagination Support
- Question Types: Multiple Choice, True/False, Fill in the Blank, Essay

## Prerequisites
- Django REST Framework
- JWT Authentication (from Auth API)
- MySQL Database
- User accounts with teacher role

## Installation

### 1. Database Setup
Make sure your MySQL database is running and configured. The Questions API uses the same database as the Auth and Classes APIs.

### 2. Run Migrations
```bash
python manage.py makemigrations questions
python manage.py migrate
```

### 3. Start Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Base URL: `http://localhost:8000/questions/`

## Authentication
All endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 1. Question Management

### 1.1 Get All Questions / Create Question
**GET/POST** `/questions/`

#### GET - List Questions (Teachers Only)
**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `type`: Filter by question type (multiple_choice, true_false, fill_blank, essay)
- `difficulty`: Filter by difficulty (easy, medium, hard)
- `search`: Search in question text
- `teacher_id`: Filter by teacher ID

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "question_text": "What is 2+2?",
                "type": "multiple_choice",
                "difficulty": "easy",
                "image_url": "https://example.com/image.jpg",
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
                "answers": [
                    {
                        "id": 1,
                        "text": "3",
                        "is_correct": false,
                        "created_at": "2024-01-15T08:00:00Z",
                        "updated_at": "2024-01-15T08:00:00Z"
                    },
                    {
                        "id": 2,
                        "text": "4",
                        "is_correct": true,
                        "created_at": "2024-01-15T08:00:00Z",
                        "updated_at": "2024-01-15T08:00:00Z"
                    }
                ],
                "usage_count": 5
            }
        ]
    }
}
```

#### POST - Create Question (Teachers Only)
**Request Body:**
```json
{
    "question_text": "What is 2+2?",
    "type": "multiple_choice",
    "difficulty": "easy",
    "image_url": "https://example.com/image.jpg",
    "answers": [
        {
            "text": "3",
            "is_correct": false
        },
        {
            "text": "4",
            "is_correct": true
        },
        {
            "text": "5",
            "is_correct": false
        }
    ]
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "question_text": "What is 2+2?",
        "type": "multiple_choice",
        "difficulty": "easy",
        "image_url": "https://example.com/image.jpg",
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
        "answers": [
            {
                "id": 1,
                "text": "3",
                "is_correct": false,
                "created_at": "2024-01-15T08:00:00Z",
                "updated_at": "2024-01-15T08:00:00Z"
            },
            {
                "id": 2,
                "text": "4",
                "is_correct": true,
                "created_at": "2024-01-15T08:00:00Z",
                "updated_at": "2024-01-15T08:00:00Z"
            },
            {
                "id": 3,
                "text": "5",
                "is_correct": false,
                "created_at": "2024-01-15T08:00:00Z",
                "updated_at": "2024-01-15T08:00:00Z"
            }
        ]
    },
    "message": "Question created successfully"
}
```

### 1.2 Get Question Detail / Update / Delete
**GET/PUT/DELETE** `/questions/{question_id}/`

#### GET - Get Question Detail
**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "question_text": "What is 2+2?",
        "type": "multiple_choice",
        "difficulty": "easy",
        "image_url": "https://example.com/image.jpg",
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
        "answers": [
            {
                "id": 1,
                "text": "3",
                "is_correct": false,
                "created_at": "2024-01-15T08:00:00Z",
                "updated_at": "2024-01-15T08:00:00Z"
            },
            {
                "id": 2,
                "text": "4",
                "is_correct": true,
                "created_at": "2024-01-15T08:00:00Z",
                "updated_at": "2024-01-15T08:00:00Z"
            }
        ],
        "usage_count": 5,
        "used_in_exams": [
            {
                "id": 1,
                "title": "Bai thi giua ky",
                "order": 1,
                "code": "Q1"
            }
        ]
    }
}
```

#### PUT - Update Question (Teachers Only)
**Request Body:**
```json
{
    "question_text": "What is 2+2? (Updated)",
    "type": "multiple_choice",
    "difficulty": "medium",
    "image_url": "https://example.com/new-image.jpg",
    "answers": [
        {
            "id": 1,
            "text": "3",
            "is_correct": false
        },
        {
            "id": 2,
            "text": "4",
            "is_correct": true
        },
        {
            "text": "6",
            "is_correct": false
        }
    ]
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "question_text": "What is 2+2? (Updated)",
        "type": "multiple_choice",
        "difficulty": "medium",
        "image_url": "https://example.com/new-image.jpg",
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
        "answers": [
            {
                "id": 1,
                "text": "3",
                "is_correct": false,
                "created_at": "2024-01-15T08:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            },
            {
                "id": 2,
                "text": "4",
                "is_correct": true,
                "created_at": "2024-01-15T08:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            },
            {
                "id": 4,
                "text": "6",
                "is_correct": false,
                "created_at": "2024-01-15T10:00:00Z",
                "updated_at": "2024-01-15T10:00:00Z"
            }
        ]
    },
    "message": "Question updated successfully"
}
```

#### DELETE - Delete Question (Teachers Only)
**Response (200 OK):**
```json
{
    "success": true,
    "message": "Question deleted successfully"
}
```

### 1.3 Get My Questions
**GET** `/questions/my-questions/`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `type`: Filter by question type (multiple_choice, true_false, fill_blank, essay)
- `difficulty`: Filter by difficulty (easy, medium, hard)
- `search`: Search in question text

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "question_text": "What is 2+2?",
                "type": "multiple_choice",
                "difficulty": "easy",
                "image_url": "https://example.com/image.jpg",
                "created_at": "2024-01-15T08:00:00Z",
                "answers_count": 4,
                "usage_count": 5
            }
        ]
    }
}
```

## 2. Answer Management

### 2.1 Add Answer to Question
**POST** `/questions/{question_id}/answers/`

**Request Body:**
```json
{
    "text": "New answer option",
    "is_correct": false
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 5,
        "question": {
            "id": 1,
            "question_text": "What is 2+2?"
        },
        "text": "New answer option",
        "is_correct": false,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T10:00:00Z"
    },
    "message": "Answer added successfully"
}
```

### 2.2 Update Answer
**PUT** `/questions/{question_id}/answers/{answer_id}/update/`

**Request Body:**
```json
{
    "text": "Updated answer text",
    "is_correct": true
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 5,
        "question": {
            "id": 1,
            "question_text": "What is 2+2?"
        },
        "text": "Updated answer text",
        "is_correct": true,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-15T11:00:00Z"
    },
    "message": "Answer updated successfully"
}
```

### 2.3 Delete Answer
**DELETE** `/questions/{question_id}/answers/{answer_id}/delete/`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Answer deleted successfully"
}
```

## Permissions and Access Control

### Role-based Access

#### Teachers
- Can create, read, update, and delete their own questions
- Can add, update, and delete answers to their own questions
- Can view all questions in the system
- Can filter and search questions

#### Students
- Cannot access question management endpoints
- Will receive 403 Forbidden for all question operations

#### Admins
- Have full access to all operations
- Can manage any question and answer

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
- `"Only teachers can view all questions"`
- `"Only teachers can view their questions"`
- `"You can only update your own questions"`
- `"You can only delete your own questions"`
- `"You can only add answers to your own questions"`
- `"You can only update answers to your own questions"`
- `"You can only delete answers to your own questions"`

## Testing

### Using curl

#### Create a Question (Teacher)
```bash
curl -X POST http://localhost:8000/questions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN" \
  -d '{
    "question_text": "What is 5+3?",
    "type": "multiple_choice",
    "difficulty": "easy",
    "answers": [
      {"text": "7", "is_correct": false},
      {"text": "8", "is_correct": true},
      {"text": "9", "is_correct": false}
    ]
  }'
```

#### Get All Questions
```bash
curl -X GET http://localhost:8000/questions/ \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN"
```

#### Get My Questions
```bash
curl -X GET http://localhost:8000/questions/my-questions/ \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN"
```

#### Add Answer to Question
```bash
curl -X POST http://localhost:8000/questions/1/answers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN" \
  -d '{
    "text": "Another option",
    "is_correct": false
  }'
```

#### Update Answer
```bash
curl -X PUT http://localhost:8000/questions/1/answers/5/update/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN" \
  -d '{
    "text": "Updated option",
    "is_correct": true
  }'
```

#### Delete Answer
```bash
curl -X DELETE http://localhost:8000/questions/1/answers/5/delete/ \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN"
```

#### Delete Question
```bash
curl -X DELETE http://localhost:8000/questions/1/ \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN"
```

## Database Schema

### Question Model
- `id`: Primary key
- `question_text`: Question content (TextField)
- `type`: Question type (CharField, choices: multiple_choice, true_false, fill_blank, essay)
- `difficulty`: Difficulty level (CharField, choices: easy, medium, hard)
- `image_url`: Optional image URL (URLField, nullable)
- `teacher`: Foreign key to User model
- `created_at`: Creation timestamp (auto_now_add=True)

### QuestionAnswer Model
- `id`: Primary key
- `question`: Foreign key to Question model
- `text`: Answer text (TextField)
- `is_correct`: Whether answer is correct (BooleanField)
- `created_at`: Creation timestamp (auto_now_add=True)
- `updated_at`: Last update timestamp (auto_now=True)

## Integration Notes

### With Auth API
- Uses the same User model from accounts app
- Requires JWT authentication for all endpoints
- Role-based permissions based on user.role field

### With Classes API
- Questions can be associated with classes through future exams module
- Teachers can create questions for their classes

### With Future Modules
- **Exams Module**: Will integrate with usage_count and used_in_exams fields
- **Results Module**: Questions will be used in exam results
- **Notifications Module**: Question-related notifications for teachers

## Configuration

### Pagination Settings
- Default page size: 20 items
- Maximum page size: 100 items
- Configurable via `page_size` query parameter

### Search and Filtering
- Case-insensitive search by question text
- Filter by question type and difficulty
- Filter by teacher ID
- Uses `icontains` lookup for partial matches

## Security Features
- JWT token authentication required
- Role-based access control
- Object-level permissions (teachers can only manage their own questions)
- Input validation and sanitization
- SQL injection protection via Django ORM

## Question Types

### Multiple Choice
- Questions with multiple answer options
- One or more correct answers possible
- Most common question type

### True/False
- Simple binary choice questions
- Only two answer options: True/False

### Fill in the Blank
- Questions requiring text input
- Open-ended answers

### Essay
- Long-form written responses
- Subjective grading required
