# Exam Sessions API Documentation

## Overview
This Exam Sessions API provides comprehensive management of exam sessions, student answers, and exam results in an educational system. It supports role-based access control where students can take exams, submit answers, and view their results, while teachers can monitor sessions and view detailed analytics.

## Features
- Exam Session Management (Start, Monitor, Complete)
- Student Answer Management (Submit, Update, Track)
- Exam Results and Analytics
- Session Logging and Monitoring
- Role-based Access Control (Student, Teacher, Admin)
- Real-time Session Tracking
- Comprehensive Statistics

## Prerequisites
- Django REST Framework
- JWT Authentication (from Auth API)
- MySQL Database
- User accounts with roles (student/teacher)
- Classes, Questions, and Exams modules

## Installation

### 1. Database Setup
Make sure your MySQL database is running and configured. The Exam Sessions API uses the same database as the Auth, Classes, Questions, and Exams APIs.

### 2. Run Migrations
```bash
python manage.py makemigrations exam_sessions
python manage.py migrate
```

### 3. Start Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Base URL: `http://localhost:8000/sessions/`

## Authentication
All endpoints require JWT authentication. Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 1. Session Management

### 1.1 Start Exam Session
**POST** `/sessions/start/`

**Request Body:**
```json
{
    "exam_id": 1
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Midterm Exam",
            "description": "Mathematics Midterm",
            "total_score": 100,
            "minutes": 60,
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2025-12-31T23:59:59Z",
            "class_obj": {
                "id": 1,
                "className": "Test Class 2024",
                "teacher": {
                    "id": 2,
                    "email": "teacher@example.com",
                    "fullName": "Test Teacher",
                    "role": "teacher",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "created_at": "2024-01-15T08:00:00Z"
            },
            "created_by": {
                "id": 2,
                "email": "teacher@example.com",
                "fullName": "Test Teacher",
                "role": "teacher",
                "created_at": "2024-01-15T08:00:00Z",
                "last_login": "2024-01-15T10:30:00Z",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false
            }
        },
        "student": {
            "id": 3,
            "email": "student@example.com",
            "fullName": "Test Student",
            "role": "student",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "code": "EXAM_20251022_FF6C829E",
        "start_time": "2025-10-22T06:44:12.587436Z",
        "end_time": null,
        "total_score": "0.00",
        "status": "in_progress",
        "submitted_at": null,
        "time_remaining": 3599,
        "answers": [
            {
                "id": 9,
                "exam_question": {
                    "id": 27,
                    "order": 1,
                    "code": "Q1",
                    "question": {
                        "id": 41,
                        "question_text": "What is 2 + 2?",
                        "type": "multiple_choice",
                        "difficulty": "easy",
                        "image_url": null,
                        "answers": [
                            {
                                "id": 120,
                                "text": "3",
                                "is_correct": false
                            },
                            {
                                "id": 121,
                                "text": "4",
                                "is_correct": true
                            },
                            {
                                "id": 122,
                                "text": "5",
                                "is_correct": false
                            }
                        ]
                    }
                },
                "selected_answer": null,
                "answer_text": null,
                "score": "0.00",
                "answered_at": "2025-10-22T06:44:12.589201Z",
                "is_correct": false
            }
        ],
        "questions": [
            {
                "id": 27,
                "exam_question": {
                    "id": 27,
                    "order": 1,
                    "code": "Q1",
                    "question": {
                        "id": 41,
                        "question_text": "What is 2 + 2?",
                        "type": "multiple_choice",
                        "difficulty": "easy",
                        "image_url": null,
                        "answers": [
                            {
                                "id": 120,
                                "text": "3",
                                "is_correct": false
                            },
                            {
                                "id": 121,
                                "text": "4",
                                "is_correct": true
                            },
                            {
                                "id": 122,
                                "text": "5",
                                "is_correct": false
                            }
                        ]
                    }
                },
                "selected_answer": null,
                "answer_text": null,
                "score": 0.0,
                "answered_at": null,
                "is_correct": false
            }
        ]
    },
    "message": "Exam session started successfully"
}
```

### 1.2 Get Active Session
**GET** `/sessions/active/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Midterm Exam",
            "minutes": 60
        },
        "code": "EXAM_20251022_FF6C829E",
        "start_time": "2025-10-22T06:44:12.587436Z",
        "status": "in_progress",
        "time_remaining": 3599,
        "answered_count": 0,
        "total_questions": 1,
        "progress_percentage": 0.0
    }
}
```

### 1.3 Get Session Detail
**GET** `/sessions/{session_id}/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Midterm Exam",
            "description": "Mathematics Midterm",
            "total_score": 100,
            "minutes": 60,
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2025-12-31T23:59:59Z",
            "class_obj": {
                "id": 1,
                "className": "Test Class 2024",
                "teacher": {
                    "id": 2,
                    "email": "teacher@example.com",
                    "fullName": "Test Teacher",
                    "role": "teacher",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "created_at": "2024-01-15T08:00:00Z"
            },
            "created_by": {
                "id": 2,
                "email": "teacher@example.com",
                "fullName": "Test Teacher",
                "role": "teacher",
                "created_at": "2024-01-15T08:00:00Z",
                "last_login": "2024-01-15T10:30:00Z",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false
            }
        },
        "student": {
            "id": 3,
            "email": "student@example.com",
            "fullName": "Test Student",
            "role": "student",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
                "is_superuser": false
        },
        "code": "EXAM_20251022_FF6C829E",
        "start_time": "2025-10-22T06:44:12.587436Z",
        "end_time": null,
        "total_score": "0.00",
        "status": "in_progress",
        "submitted_at": null,
        "answers": [
            {
                "id": 9,
                "exam_question": {
                    "id": 27,
                    "order": 1,
                    "code": "Q1",
                    "question": {
                        "id": 41,
                        "question_text": "What is 2 + 2?",
                        "type": "multiple_choice",
                        "difficulty": "easy",
                        "image_url": null,
                        "answers": [
                            {
                                "id": 120,
                                "text": "3",
                                "is_correct": false
                            },
                            {
                                "id": 121,
                                "text": "4",
                                "is_correct": true
                            },
                            {
                                "id": 122,
                                "text": "5",
                                "is_correct": false
                            }
                        ]
                    }
                },
                "selected_answer": null,
                "answer_text": null,
                "score": "0.00",
                "answered_at": "2025-10-22T06:44:12.589201Z",
                "is_correct": false
            }
        ],
        "logs": [
            {
                "id": 1,
                "actions": "exam_started",
                "timestamp": "2025-10-22T06:44:12.587436Z",
                "detail": "Student started the exam"
            }
        ]
    }
}
```

### 1.4 Submit Exam
**POST** `/sessions/{session_id}/submit/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "session": {
            "id": 1,
            "code": "EXAM_20251022_FF6C829E",
            "status": "completed"
        },
        "student": {
            "id": 3,
            "email": "student@example.com",
            "fullName": "Test Student",
            "role": "student",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "exam": {
            "id": 1,
            "title": "Midterm Exam",
            "description": "Mathematics Midterm",
            "total_score": 100,
            "minutes": 60,
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2025-12-31T23:59:59Z",
            "class_obj": {
                "id": 1,
                "className": "Test Class 2024",
                "teacher": {
                    "id": 2,
                    "email": "teacher@example.com",
                    "fullName": "Test Teacher",
                    "role": "teacher",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "created_at": "2024-01-15T08:00:00Z"
            },
            "created_by": {
                "id": 2,
                "email": "teacher@example.com",
                "fullName": "Test Teacher",
                "role": "teacher",
                "created_at": "2024-01-15T08:00:00Z",
                "last_login": "2024-01-15T10:30:00Z",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false
            }
        },
        "total_score": "100.00",
        "correct_count": 1,
        "wrong_count": 0,
        "submitted_at": "2025-10-22T06:44:12.628878Z",
        "status": "graded",
        "feedback": null,
        "percentage": "100.00",
        "grade": "A",
        "time_taken": 0,
        "answers_summary": [
            {
                "question_order": 1,
                "question_text": "What is 2 + 2?",
                "is_correct": true,
                "score": 100.0,
                "selected_answer": "4",
                "correct_answer": "4"
            }
        ]
    },
    "message": "Exam submitted successfully"
}
```

## 2. Answer Management

### 2.1 Submit Answer
**POST** `/sessions/{session_id}/answers/`

**Request Body:**
```json
{
    "exam_question_id": 27,
    "selected_answer_id": 121,
    "answer_text": ""
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "data": {
        "id": 9,
        "exam_question": {
            "id": 27,
            "order": 1,
            "code": "Q1",
            "question": {
                "id": 41,
                "question_text": "What is 2 + 2?",
                "type": "multiple_choice",
                "difficulty": "easy",
                "image_url": null,
                "answers": [
                    {
                        "id": 120,
                        "text": "3",
                        "is_correct": false
                    },
                    {
                        "id": 121,
                        "text": "4",
                        "is_correct": true
                    },
                    {
                        "id": 122,
                        "text": "5",
                        "is_correct": false
                    }
                ]
            }
        },
        "selected_answer": {
            "id": 121,
            "text": "4",
            "is_correct": true
        },
        "answer_text": "",
        "score": "100.00",
        "answered_at": "2025-10-22T06:44:12.628878Z",
        "is_correct": true
    },
    "message": "Answer submitted successfully"
}
```

### 2.2 Update Answer
**PUT** `/sessions/{session_id}/answers/{answer_id}/`

**Request Body:**
```json
{
    "selected_answer_id": 121,
    "answer_text": ""
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 9,
        "exam_question": {
            "id": 27,
            "order": 1,
            "code": "Q1",
            "question": {
                "id": 41,
                "question_text": "What is 2 + 2?",
                "type": "multiple_choice",
                "difficulty": "easy",
                "image_url": null,
                "answers": [
                    {
                        "id": 120,
                        "text": "3",
                        "is_correct": false
                    },
                    {
                        "id": 121,
                        "text": "4",
                        "is_correct": true
                    },
                    {
                        "id": 122,
                        "text": "5",
                        "is_correct": false
                    }
                ]
            }
        },
        "selected_answer": {
            "id": 121,
            "text": "4",
            "is_correct": true
        },
        "answer_text": "",
        "score": "100.00",
        "answered_at": "2025-10-22T06:44:12.628878Z",
        "is_correct": true
    },
    "message": "Answer updated successfully"
}
```

## 3. Session Lists and Analytics

### 3.1 Get My Sessions
**GET** `/sessions/my-sessions/`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `status`: Filter by status (in_progress, completed, abandoned, timeout)
- `exam_id`: Filter by exam ID

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
                    "title": "Midterm Exam",
                    "class_obj": {
                        "id": 1,
                        "className": "Test Class 2024"
                    }
                },
                "student": {
                    "id": 3,
                    "email": "student@example.com",
                    "fullName": "Test Student",
                    "role": "student",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "code": "EXAM_20251022_FF6C829E",
                "start_time": "2025-10-22T06:44:12.587436Z",
                "end_time": "2025-10-22T06:44:12.628878Z",
                "total_score": "100.00",
                "status": "completed",
                "submitted_at": "2025-10-22T06:44:12.628878Z",
                "time_taken": 0,
                "percentage": "100.00"
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

### 3.2 Get Class Sessions
**GET** `/sessions/class/{class_id}/`

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
                    "title": "Midterm Exam",
                    "class_obj": {
                        "id": 1,
                        "className": "Test Class 2024"
                    }
                },
                "student": {
                    "id": 3,
                    "email": "student@example.com",
                    "fullName": "Test Student",
                    "role": "student",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "code": "EXAM_20251022_FF6C829E",
                "start_time": "2025-10-22T06:44:12.587436Z",
                "end_time": "2025-10-22T06:44:12.628878Z",
                "total_score": "100.00",
                "status": "completed",
                "submitted_at": "2025-10-22T06:44:12.628878Z",
                "time_taken": 0,
                "percentage": "100.00"
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

### 3.3 Get Exam Sessions
**GET** `/sessions/exam/{exam_id}/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "exam": {
            "id": 1,
            "title": "Midterm Exam",
            "total_score": 100,
            "minutes": 60
        },
        "sessions": {
            "results": [
                {
                    "id": 1,
                    "exam": {
                        "id": 1,
                        "title": "Midterm Exam",
                        "class_obj": {
                            "id": 1,
                            "className": "Test Class 2024"
                        }
                    },
                    "student": {
                        "id": 3,
                        "email": "student@example.com",
                        "fullName": "Test Student",
                        "role": "student",
                        "created_at": "2024-01-15T08:00:00Z",
                        "last_login": "2024-01-15T10:30:00Z",
                        "is_active": true,
                        "is_staff": false,
                        "is_superuser": false
                    },
                    "code": "EXAM_20251022_FF6C829E",
                    "start_time": "2025-10-22T06:44:12.587436Z",
                    "end_time": "2025-10-22T06:44:12.628878Z",
                    "total_score": "100.00",
                    "status": "completed",
                    "submitted_at": "2025-10-22T06:44:12.628878Z",
                    "time_taken": 0,
                    "percentage": "100.00"
                }
            ],
            "count": 1,
            "next": null,
            "previous": null,
            "page": 1,
            "total_pages": 1
        },
        "statistics": {
            "total_sessions": 1,
            "completed": 1,
            "in_progress": 0,
            "abandoned": 0,
            "timeout": 0,
            "average_score": 100.0,
            "completion_rate": 100.0
        }
    }
}
```

## 4. Session Logging

### 4.1 Get Session Logs
**GET** `/sessions/{session_id}/logs/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "session": {
            "id": 1,
            "code": "EXAM_20251022_FF6C829E",
            "student": {
                "id": 3,
                "fullName": "Test Student"
            }
        },
        "logs": [
            {
                "id": 1,
                "actions": "exam_started",
                "timestamp": "2025-10-22T06:44:12.587436Z",
                "detail": "Student started the exam"
            },
            {
                "id": 2,
                "actions": "answer_submitted",
                "timestamp": "2025-10-22T06:44:12.628878Z",
                "detail": "Answered question Q1"
            },
            {
                "id": 3,
                "actions": "exam_submitted",
                "timestamp": "2025-10-22T06:44:12.628878Z",
                "detail": "Student submitted the exam"
            }
        ]
    }
}
```

### 4.2 Log Page Action
**POST** `/sessions/{session_id}/log-action/`

**Request Body:**
```json
{
    "action": "page_leave"
}
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Action logged successfully"
}
```

## 5. Session Results

### 5.1 Get Session Result
**GET** `/sessions/{session_id}/result/`

**Response (200 OK):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "session": {
            "id": 1,
            "code": "EXAM_20251022_FF6C829E",
            "status": "completed"
        },
        "student": {
            "id": 3,
            "email": "student@example.com",
            "fullName": "Test Student",
            "role": "student",
            "created_at": "2024-01-15T08:00:00Z",
            "last_login": "2024-01-15T10:30:00Z",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false
        },
        "exam": {
            "id": 1,
            "title": "Midterm Exam",
            "description": "Mathematics Midterm",
            "total_score": 100,
            "minutes": 60,
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2025-12-31T23:59:59Z",
            "class_obj": {
                "id": 1,
                "className": "Test Class 2024",
                "teacher": {
                    "id": 2,
                    "email": "teacher@example.com",
                    "fullName": "Test Teacher",
                    "role": "teacher",
                    "created_at": "2024-01-15T08:00:00Z",
                    "last_login": "2024-01-15T10:30:00Z",
                    "is_active": true,
                    "is_staff": false,
                    "is_superuser": false
                },
                "created_at": "2024-01-15T08:00:00Z"
            },
            "created_by": {
                "id": 2,
                "email": "teacher@example.com",
                "fullName": "Test Teacher",
                "role": "teacher",
                "created_at": "2024-01-15T08:00:00Z",
                "last_login": "2024-01-15T10:30:00Z",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false
            }
        },
        "total_score": "100.00",
        "correct_count": 1,
        "wrong_count": 0,
        "submitted_at": "2025-10-22T06:44:12.628878Z",
        "status": "graded",
        "feedback": null,
        "percentage": "100.00",
        "grade": "A",
        "time_taken": 0,
        "answers_summary": [
            {
                "question_order": 1,
                "question_text": "What is 2 + 2?",
                "is_correct": true,
                "score": 100.0,
                "selected_answer": "4",
                "correct_answer": "4"
            }
        ]
    }
}
```

## Permissions and Access Control

### Role-based Access

#### Students
- Can start exam sessions for exams they are enrolled in
- Can submit and update answers during active sessions
- Can view their own session details and results
- Can view their own session logs
- Cannot view other students' sessions

#### Teachers
- Can view all sessions for their classes
- Can view detailed session analytics and statistics
- Can monitor student progress in real-time
- Can view session logs for their students
- Cannot modify student answers

#### Admins
- Have full access to all operations
- Can view all sessions and results
- Can manage any session data

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
- `"You are not enrolled in this class"`
- `"You already have an active session for this exam"`
- `"Session is not active"`
- `"Exam has not started yet"`
- `"Exam has already ended"`
- `"Selected answer does not belong to this question"`
- `"Question not found in this exam"`

## Testing

### Using curl

#### Start Exam Session
```bash
curl -X POST http://localhost:8000/sessions/start/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer STUDENT_ACCESS_TOKEN" \
  -d '{
    "exam_id": 1
  }'
```

#### Submit Answer
```bash
curl -X POST http://localhost:8000/sessions/1/answers/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer STUDENT_ACCESS_TOKEN" \
  -d '{
    "exam_question_id": 27,
    "selected_answer_id": 121
  }'
```

#### Submit Exam
```bash
curl -X POST http://localhost:8000/sessions/1/submit/ \
  -H "Authorization: Bearer STUDENT_ACCESS_TOKEN"
```

#### Get My Sessions
```bash
curl -X GET http://localhost:8000/sessions/my-sessions/ \
  -H "Authorization: Bearer STUDENT_ACCESS_TOKEN"
```

#### Get Exam Sessions (Teacher)
```bash
curl -X GET http://localhost:8000/sessions/exam/1/ \
  -H "Authorization: Bearer TEACHER_ACCESS_TOKEN"
```

## Database Schema

### ExamSession Model
- `id`: Primary key
- `exam`: Foreign key to Exam model
- `student`: Foreign key to User model
- `code`: Unique session code (CharField, max_length=50)
- `start_time`: Session start time (DateTimeField)
- `end_time`: Session end time (DateTimeField, nullable)
- `total_score`: Total score achieved (DecimalField)
- `status`: Session status (CharField, choices: in_progress, completed, abandoned, timeout)
- `submitted_at`: Submission timestamp (DateTimeField, nullable)

### StudentAnswer Model
- `id`: Primary key
- `session`: Foreign key to ExamSession model
- `exam_question`: Foreign key to ExamQuestion model
- `selected_answer`: Foreign key to QuestionAnswer model (nullable)
- `answer_text`: Text answer (TextField, nullable)
- `score`: Score for this answer (DecimalField)
- `answered_at`: Answer timestamp (DateTimeField)
- `is_correct`: Whether answer is correct (BooleanField)

### ExamResult Model
- `id`: Primary key
- `session`: OneToOneField to ExamSession model
- `student`: Foreign key to User model
- `exam`: Foreign key to Exam model
- `total_score`: Final total score (DecimalField)
- `correct_count`: Number of correct answers (PositiveIntegerField)
- `wrong_count`: Number of wrong answers (PositiveIntegerField)
- `submitted_at`: Submission timestamp (DateTimeField)
- `status`: Result status (CharField, choices: pending, graded, reviewed)
- `feedback`: Teacher feedback (TextField, nullable)
- `percentage`: Percentage score (DecimalField)

### ExamLog Model
- `id`: Primary key
- `session`: Foreign key to ExamSession model
- `student`: Foreign key to User model
- `actions`: Action type (CharField, max_length=100)
- `timestamp`: Action timestamp (DateTimeField)
- `detail`: Action details (TextField, nullable)

## Integration Notes

### With Auth API
- Uses the same User model from accounts app
- Requires JWT authentication for all endpoints
- Role-based permissions based on user.role field

### With Classes API
- Sessions are associated with classes through exams
- Students can only start sessions for exams in their enrolled classes
- Teachers can view sessions for their classes

### With Questions API
- Sessions use questions from the questions module
- Answer validation based on question types
- Score calculation based on question difficulty

### With Exams API
- Sessions are created for specific exams
- Session time limits based on exam duration
- Results are linked to exam statistics

## Configuration

### Pagination Settings
- Default page size: 20 items
- Maximum page size: 100 items
- Configurable via `page_size` query parameter

### Session Timeout
- Sessions automatically timeout based on exam duration
- Real-time time remaining calculation
- Automatic session status updates

### Logging Configuration
- All student actions are logged
- Page leave/return tracking
- Answer submission tracking
- Session completion tracking

## Security Features
- JWT token authentication required
- Role-based access control
- Object-level permissions (students can only access their own sessions)
- Session timeout protection
- Answer validation and sanitization
- SQL injection protection via Django ORM
- Real-time session monitoring

## Performance Considerations
- Efficient session queries with proper indexing
- Pagination for large session lists
- Optimized answer submission with bulk operations
- Real-time statistics calculation
- Cached session data for active sessions
