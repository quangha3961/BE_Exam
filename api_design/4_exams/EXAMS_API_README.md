# Exams API Documentation

## Overview
This Exams API provides comprehensive management of exams in an educational system. It supports role-based access control where teachers can create, update, and manage exams, while students can view available exams and manage their favorites.

## Features
- Exam Management (Create, Read, Update, Delete)
- Question Management within Exams
- Role-based Access Control
- Search and Filtering
- Pagination Support
- Favorite Exams Management
- Exam Statistics (for teachers)
- Student Access to Available Exams

## Prerequisites
- Django REST Framework
- JWT Authentication (from Auth API)
- MySQL Database
- User accounts with roles (teacher/student)
- Classes and Questions modules

## Installation

### 1. Database Setup
Make sure your MySQL database is running and configured. The Exams API uses the same database as the Auth, Classes, and Questions APIs.

### 2. Run Migrations
```bash
python manage.py makemigrations exams
python manage.py migrate
```

### 3. Start Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Base URL: `http://localhost:8000/exams/`

## Authentication
All endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 1. Exam Management

### 1.1 Get All Exams / Create Exam
**GET/POST** `/exams/`

#### GET - List Exams (Teachers Only)
**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `class_obj`: Filter by class
- `search`: Search by title or description
- `status`: upcoming, ongoing, completed

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "title": "Bai thi giua ky",
                "description": "Bai thi toan giua ky",
                "total_score": 100,
                "minutes": 90,
                "start_time": "2024-01-20T08:00:00Z",
                "end_time": "2024-01-20T10:00:00Z",
                "created_at": "2024-01-15T08:00:00Z",
                "class_obj": {
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
                },
                "created_by": {
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
                "question_count": 5,
                "student_count": 25,
                "session_count": 20,
                "status": "upcoming"
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

#### POST - Create Exam (Teachers Only)
**Request Body:**
```json
{
    "class_obj": 1,
    "title": "Bai thi giua ky",
    "description": "Bai thi toan giua ky",
    "total_score": 100,
    "minutes": 90,
    "start_time": "2024-01-20T08:00:00Z",
    "end_time": "2024-01-20T10:00:00Z",
    "questions": [
        {
            "question_id": 1,
            "order": 1,
            "code": "Q1"
        },
        {
            "question_id": 2,
            "order": 2,
            "code": "Q2"
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
        "title": "Bai thi giua ky",
        "description": "Bai thi toan giua ky",
        "total_score": 100,
        "minutes": 90,
        "start_time": "2024-01-20T08:00:00Z",
        "end_time": "2024-01-20T10:00:00Z",
        "created_at": "2024-01-15T08:00:00Z",
        "class_obj": {
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
        },
        "created_by": {
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
        "exam_questions": [
            {
                "id": 1,
                "question": {
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
                },
                "order": 1,
                "code": "Q1"
            }
        ],
        "sessions": [],
        "favorites_count": 0,
        "is_favorited": false
    },
    "message": "Exam created successfully"
}
```

### 1.2 Get Exam Detail / Update / Delete
**GET/PUT/DELETE** `/exams/{exam_id}/`

#### GET - Get Exam Detail
**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "Bai thi giua ky",
        "description": "Bai thi toan giua ky",
        "total_score": 100,
        "minutes": 90,
        "start_time": "2024-01-20T08:00:00Z",
        "end_time": "2024-01-20T10:00:00Z",
        "created_at": "2024-01-15T08:00:00Z",
        "class_obj": {
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
        },
        "created_by": {
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
        "exam_questions": [
            {
                "id": 1,
                "question": {
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
                },
                "order": 1,
                "code": "Q1"
            }
        ],
        "sessions": [],
        "favorites_count": 15,
        "is_favorited": false
    }
}
```

#### PUT - Update Exam (Teachers Only)
**Note:** All fields are optional for partial updates. Only provided fields will be updated.

**Request Body:**
```json
{
    "title": "Bai thi giua ky - Updated",
    "description": "Bai thi toan giua ky - Updated",
    "total_score": 120,
    "minutes": 100
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "title": "Bai thi giua ky - Updated",
        "description": "Bai thi toan giua ky - Updated",
        "total_score": 120,
        "minutes": 100,
        "start_time": "2024-01-21T08:00:00Z",
        "end_time": "2024-01-21T10:00:00Z",
        "created_at": "2024-01-15T08:00:00Z",
        "class_obj": {
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
        },
        "created_by": {
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
        "exam_questions": [],
        "sessions": [],
        "favorites_count": 15,
        "is_favorited": false
    },
    "message": "Exam updated successfully"
}
```

#### DELETE - Delete Exam (Teachers Only)
**Response (200 OK):**
```json
{
    "success": true,
    "message": "Exam deleted successfully"
}
```

### 1.3 Get Available Exams (Students)
**GET** `/exams/available/`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `class_obj`: Filter by class
- `status`: upcoming, ongoing

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "title": "Bai thi giua ky",
                "description": "Bai thi toan giua ky",
                "total_score": 100,
                "minutes": 90,
                "start_time": "2024-01-20T08:00:00Z",
                "end_time": "2024-01-20T10:00:00Z",
                "class_obj": {
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
                },
                "created_by": {
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
                "question_count": 5,
                "status": "upcoming",
                "can_start": true,
                "time_remaining": "2 days, 5 hours",
                "is_favorited": false,
                "has_session": false
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

## 2. Question Management within Exams

### 2.1 Add Question to Exam
**POST** `/exams/{exam_id}/questions/`

**Request Body:**
```json
{
    "question_id": 3,
    "order": 3,
    "code": "Q3"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 3,
        "question": {
            "id": 3,
            "question_text": "What is 4+4?",
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
                    "id": 5,
                    "text": "7",
                    "is_correct": false,
                    "created_at": "2024-01-15T08:00:00Z",
                    "updated_at": "2024-01-15T08:00:00Z"
                },
                {
                    "id": 6,
                    "text": "8",
                    "is_correct": true,
                    "created_at": "2024-01-15T08:00:00Z",
                    "updated_at": "2024-01-15T08:00:00Z"
                }
            ],
            "usage_count": 5
        },
        "order": 3,
        "code": "Q3"
    },
    "message": "Question added to exam successfully"
}
```

### 2.2 Remove Question from Exam
**DELETE** `/exams/{exam_id}/questions/{exam_question_id}/delete/`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Question removed from exam successfully"
}
```

### 2.3 Update Exam Question Order
**PUT** `/exams/{exam_id}/questions/{exam_question_id}/`

**Request Body:**
```json
{
    "order": 2,
    "code": "Q2-Updated"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "question": {
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
        },
        "order": 2,
        "code": "Q2-Updated"
    },
    "message": "Exam question updated successfully"
}
```

## 3. Favorite Exams Management

### 3.1 Add to Favorites (Students)
**POST** `/exams/{exam_id}/favorite/`

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "user": {
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
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky",
            "description": "Bai thi toan giua ky",
            "total_score": 100,
            "minutes": 90,
            "start_time": "2024-01-20T08:00:00Z",
            "end_time": "2024-01-20T10:00:00Z",
            "created_at": "2024-01-15T08:00:00Z",
            "class_obj": {
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
            },
            "created_by": {
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
            "question_count": 5,
            "student_count": 25,
            "session_count": 20,
            "status": "upcoming"
        },
        "created_at": "2024-01-15T10:00:00Z"
    },
    "message": "Exam added to favorites successfully"
}
```

### 3.2 Remove from Favorites (Students)
**DELETE** `/exams/{exam_id}/favorite/remove/`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Exam removed from favorites successfully"
}
```

### 3.3 Get Favorite Exams (Students)
**GET** `/exams/favorites/`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "exam": {
                    "id": 1,
                    "title": "Bai thi giua ky",
                    "description": "Bai thi toan giua ky",
                    "total_score": 100,
                    "minutes": 90,
                    "start_time": "2024-01-20T08:00:00Z",
                    "end_time": "2024-01-20T10:00:00Z",
                    "created_at": "2024-01-15T08:00:00Z",
                    "class_obj": {
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
                    },
                    "created_by": {
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
                    "question_count": 5,
                    "student_count": 25,
                    "session_count": 20,
                    "status": "upcoming"
                },
                "created_at": "2024-01-15T10:00:00Z"
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

## 4. Exam Statistics

### 4.1 Get Exam Statistics (Teachers)
**GET** `/exams/{exam_id}/statistics/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky",
            "total_score": 100,
            "minutes": 90
        },
        "statistics": {
            "total_students": 25,
            "completed_sessions": 0,
            "in_progress_sessions": 0,
            "abandoned_sessions": 0,
            "timeout_sessions": 0,
            "average_score": 0.0,
            "highest_score": 0.0,
            "lowest_score": 0.0,
            "completion_rate": 0.0
        },
        "score_distribution": {
            "0-20": 0,
            "21-40": 0,
            "41-60": 0,
            "61-80": 0,
            "81-100": 0
        }
    }
}
```

## Permissions and Access Control

### Role-based Access

#### Teachers
- Can create, read, update, and delete their own exams
- Can add and remove questions from their exams
- Can view exam statistics for their exams
- Can only manage exams for classes they teach

#### Students
- Can view available exams in their enrolled classes
- Can add and remove exams from their favorites
- Cannot create, update, or delete exams
- Cannot manage exam questions

#### Admins
- Have full access to all operations
- Can manage any exam and exam questions

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
- `"Only teachers can view all exams"`
- `"You can only create exams for your own classes"`
- `"You can only update your own exams"`
- `"You can only delete your own exams"`
- `"You can only add questions to your own exams"`
- `"Question is already in this exam"`
- `"Exam is already in your favorites"`
- `"question_id is required"`
- `"Question does not exist"`

## Testing

### Using curl

#### Create an Exam (Teacher)
```bash
curl -X POST http://localhost:8000/exams/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN" \
  -d '{
    "class_obj": 1,
    "title": "Test Exam",
    "description": "A test exam",
    "total_score": 100,
    "minutes": 90,
    "start_time": "2024-01-20T08:00:00Z",
    "end_time": "2024-01-20T10:00:00Z",
    "questions": [
      {
        "question_id": 1,
        "order": 1,
        "code": "Q1"
      }
    ]
  }'
```

#### Get All Exams
```bash
curl -X GET http://localhost:8000/exams/ \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN"
```

#### Get Available Exams (Student)
```bash
curl -X GET http://localhost:8000/exams/available/ \
  -H "Authorization: Bearer STUDENT_ACCESS_TOKEN"
```

#### Add Question to Exam
```bash
curl -X POST http://localhost:8000/exams/1/questions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN" \
  -d '{
    "question_id": 2,
    "order": 2,
    "code": "Q2"
  }'
```

#### Add to Favorites (Student)
```bash
curl -X POST http://localhost:8000/exams/1/favorite/ \
  -H "Authorization: Bearer STUDENT_ACCESS_TOKEN"
```

#### Get Exam Statistics
```bash
curl -X GET http://localhost:8000/exams/1/statistics/ \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN"
```

## Database Schema

### Exam Model
- `id`: Primary key
- `class_obj`: Foreign key to Class model
- `title`: Exam title (CharField, max_length=255)
- `description`: Exam description (TextField, nullable)
- `total_score`: Total possible score (PositiveIntegerField, default=100)
- `minutes`: Exam duration in minutes (PositiveIntegerField)
- `start_time`: Exam start time (DateTimeField)
- `end_time`: Exam end time (DateTimeField)
- `created_by`: Foreign key to User model (teacher who created the exam)
- `created_at`: Creation timestamp (auto_now_add=True)

### ExamQuestion Model
- `id`: Primary key
- `exam`: Foreign key to Exam model
- `question`: Foreign key to Question model
- `order`: Question order in exam (PositiveIntegerField)
- `code`: Question code (CharField, max_length=50, nullable)
- `unique_together`: ['exam', 'question'] (prevents duplicate questions)

### ExamFavorite Model
- `id`: Primary key
- `user`: Foreign key to User model
- `exam`: Foreign key to Exam model
- `created_at`: Creation timestamp (auto_now_add=True)
- `unique_together`: ['user', 'exam'] (prevents duplicate favorites)

## Integration Notes

### With Auth API
- Uses the same User model from accounts app
- Requires JWT authentication for all endpoints
- Role-based permissions based on user.role field

### With Classes API
- Exams are associated with classes
- Teachers can only create exams for classes they teach
- Students can only see exams in classes they are enrolled in

### With Questions API
- Exams can contain multiple questions
- Questions can be used in multiple exams
- Usage tracking for questions

### With Future Modules
- **Exam Sessions Module**: Will integrate with session_count and statistics
- **Results Module**: Will provide exam results and scoring
- **Notifications Module**: Exam-related notifications for students and teachers

## Configuration

### Pagination Settings
- Default page size: 20 items
- Maximum page size: 100 items
- Configurable via `page_size` query parameter

### Search and Filtering
- Case-insensitive search by title and description
- Filter by class, status, and date ranges
- Uses `icontains` lookup for partial matches

## Security Features
- JWT token authentication required
- Role-based access control
- Object-level permissions (teachers can only manage their own exams)
- Input validation and sanitization
- SQL injection protection via Django ORM
- Time validation for exam scheduling
