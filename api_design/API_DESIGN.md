# API Design for Exam System

## Base URL
```
http://localhost:8000/api/v1/
```

## Authentication
- **Method**: JWT Token
- **Header**: `Authorization: Bearer <token>`
- **Token Expiry**: 24 hours
- **Refresh Token**: 7 days

---

## 1. AUTHENTICATION API (`/auth/`)

### 1.1 User Registration
```
POST /auth/register/
```
**Request Body:**
```json
{
    "email": "student@example.com",
    "password": "password123",
    "fullName": "Nguyen Van A",
    "role": "student"  // "student" | "teacher" | "admin"
}
```
**Response:**
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

### 1.2 User Login
```
POST /auth/login/
```
**Request Body:**
```json
{
    "email": "student@example.com",
    "password": "password123"
}
```
**Response:**
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

### 1.3 Refresh Token
```
POST /auth/refresh/
```
**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "message": "Token refreshed successfully"
}
```

### 1.4 Logout
```
POST /auth/logout/
```
**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```
**Response:**
```json
{
    "success": true,
    "message": "Logout successful"
}
```

### 1.5 Get Current User Profile
```
GET /auth/profile/
```
**Response:**
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

### 1.6 Update Profile
```
PUT /auth/profile/
```
**Request Body:**
```json
{
    "fullName": "Nguyen Van B",
    "email": "newemail@example.com"
}
```
**Response:**
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

---

## 2. CLASSES API (`/classes/`)

### 2.1 Get All Classes (Teacher)
```
GET /classes/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `search`: Search by class name

**Response:**
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
                    "fullName": "Nguyen Thi B",
                    "email": "teacher@example.com"
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

### 2.2 Create Class (Teacher)
```
POST /classes/
```
**Request Body:**
```json
{
    "className": "Lop 12A1"
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "className": "Lop 12A1",
        "teacher": {
            "id": 2,
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
        },
        "created_at": "2024-01-15T08:00:00Z",
        "student_count": 0,
        "exam_count": 0
    },
    "message": "Class created successfully"
}
```

### 2.3 Get Class Detail
```
GET /classes/{class_id}/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "className": "Lop 12A1",
        "teacher": {
            "id": 2,
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
        },
        "created_at": "2024-01-15T08:00:00Z",
        "students": [
            {
                "id": 1,
                "student": {
                    "id": 3,
                    "fullName": "Nguyen Van C",
                    "email": "student1@example.com"
                },
                "joined_at": "2024-01-15T09:00:00Z"
            }
        ],
        "exams": [
            {
                "id": 1,
                "title": "Bai thi giua ky",
                "start_time": "2024-01-20T08:00:00Z",
                "end_time": "2024-01-20T10:00:00Z",
                "total_score": 100,
                "minutes": 120
            }
        ]
    }
}
```

### 2.4 Update Class (Teacher)
```
PUT /classes/{class_id}/
```
**Request Body:**
```json
{
    "className": "Lop 12A1 - Updated"
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "className": "Lop 12A1 - Updated",
        "teacher": {
            "id": 2,
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
        },
        "created_at": "2024-01-15T08:00:00Z"
    },
    "message": "Class updated successfully"
}
```

### 2.5 Delete Class (Teacher)
```
DELETE /classes/{class_id}/
```
**Response:**
```json
{
    "success": true,
    "message": "Class deleted successfully"
}
```

### 2.6 Add Student to Class (Teacher)
```
POST /classes/{class_id}/students/
```
**Request Body:**
```json
{
    "student_email": "student@example.com"
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "class_obj": {
            "id": 1,
            "className": "Lop 12A1"
        },
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "joined_at": "2024-01-15T09:00:00Z"
    },
    "message": "Student added to class successfully"
}
```

### 2.7 Remove Student from Class (Teacher)
```
DELETE /classes/{class_id}/students/{student_id}/
```
**Response:**
```json
{
    "success": true,
    "message": "Student removed from class successfully"
}
```

### 2.8 Get Class Students
```
GET /classes/{class_id}/students/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "student": {
                    "id": 3,
                    "fullName": "Nguyen Van C",
                    "email": "student1@example.com",
                    "role": "student"
                },
                "joined_at": "2024-01-15T09:00:00Z"
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 2.9 Get My Classes (Student)
```
GET /classes/my-classes/
```
**Response:**
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
                    "fullName": "Nguyen Thi B",
                    "email": "teacher@example.com"
                },
                "joined_at": "2024-01-15T09:00:00Z",
                "exam_count": 3,
                "available_exams": 1
            }
        ],
        "count": 1
    }
}
```

---

## 3. QUESTIONS API (`/questions/`)

### 3.1 Get All Questions (Teacher)
```
GET /questions/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `type`: multiple_choice, true_false, fill_blank, essay
- `difficulty`: easy, medium, hard
- `search`: search in question text
- `teacher_id`: Filter by teacher

**Response:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "question_text": "What is 2+2?",
                "type": "multiple_choice",
                "difficulty": "easy",
                "image_url": "https://example.com/image.jpg",
                "teacher": {
                    "id": 2,
                    "fullName": "Nguyen Thi B",
                    "email": "teacher@example.com"
                },
                "created_at": "2024-01-15T08:00:00Z",
                "answers": [
                    {
                        "id": 1,
                        "text": "3",
                        "is_correct": false,
                        "created_at": "2024-01-15T08:00:00Z"
                    },
                    {
                        "id": 2,
                        "text": "4",
                        "is_correct": true,
                        "created_at": "2024-01-15T08:00:00Z"
                    }
                ],
                "usage_count": 5
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 3.2 Create Question (Teacher)
```
POST /questions/
```
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
**Response:**
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
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
        },
        "created_at": "2024-01-15T08:00:00Z",
        "answers": [
            {
                "id": 1,
                "text": "3",
                "is_correct": false,
                "created_at": "2024-01-15T08:00:00Z"
            },
            {
                "id": 2,
                "text": "4",
                "is_correct": true,
                "created_at": "2024-01-15T08:00:00Z"
            },
            {
                "id": 3,
                "text": "5",
                "is_correct": false,
                "created_at": "2024-01-15T08:00:00Z"
            }
        ]
    },
    "message": "Question created successfully"
}
```

### 3.3 Get Question Detail
```
GET /questions/{question_id}/
```
**Response:**
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
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
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

### 3.4 Update Question (Teacher)
```
PUT /questions/{question_id}/
```
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
**Response:**
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
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
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

### 3.5 Delete Question (Teacher)
```
DELETE /questions/{question_id}/
```
**Response:**
```json
{
    "success": true,
    "message": "Question deleted successfully"
}
```

### 3.6 Get My Questions (Teacher)
```
GET /questions/my-questions/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `type`: multiple_choice, true_false, fill_blank, essay
- `difficulty`: easy, medium, hard
- `search`: search in question text

**Response:**
```json
{
    "success": true,
    "data": {
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
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 3.7 Add Answer to Question (Teacher)
```
POST /questions/{question_id}/answers/
```
**Request Body:**
```json
{
    "text": "New answer option",
    "is_correct": false
}
```
**Response:**
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

### 3.8 Update Answer (Teacher)
```
PUT /questions/{question_id}/answers/{answer_id}/
```
**Request Body:**
```json
{
    "text": "Updated answer text",
    "is_correct": true
}
```
**Response:**
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

### 3.9 Delete Answer (Teacher)
```
DELETE /questions/{question_id}/answers/{answer_id}/
```
**Response:**
```json
{
    "success": true,
    "message": "Answer deleted successfully"
}
```

---

## 4. EXAMS API (`/exams/`)

### 4.1 Get All Exams (Teacher)
```
GET /exams/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `class_id`: Filter by class
- `search`: Search by title or description
- `status`: upcoming, ongoing, completed

**Response:**
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
                    "className": "Lop 12A1"
                },
                "created_by": {
                    "id": 2,
                    "fullName": "Nguyen Thi B",
                    "email": "teacher@example.com"
                },
                "question_count": 5,
                "student_count": 25,
                "session_count": 20,
                "status": "upcoming"
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 4.2 Create Exam (Teacher)
```
POST /exams/
```
**Request Body:**
```json
{
    "class_id": 1,
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
**Response:**
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
            "className": "Lop 12A1"
        },
        "created_by": {
            "id": 2,
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
        },
        "exam_questions": [
            {
                "id": 1,
                "question": {
                    "id": 1,
                    "question_text": "What is 2+2?",
                    "type": "multiple_choice",
                    "difficulty": "easy"
                },
                "order": 1,
                "code": "Q1"
            },
            {
                "id": 2,
                "question": {
                    "id": 2,
                    "question_text": "What is 3+3?",
                    "type": "multiple_choice",
                    "difficulty": "easy"
                },
                "order": 2,
                "code": "Q2"
            }
        ]
    },
    "message": "Exam created successfully"
}
```

### 4.3 Get Exam Detail
```
GET /exams/{exam_id}/
```
**Response:**
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
                "fullName": "Nguyen Thi B",
                "email": "teacher@example.com"
            }
        },
        "created_by": {
            "id": 2,
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
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
                        }
                    ]
                },
                "order": 1,
                "code": "Q1"
            }
        ],
        "sessions": [
            {
                "id": 1,
                "student": {
                    "id": 3,
                    "fullName": "Nguyen Van C",
                    "email": "student@example.com"
                },
                "status": "completed",
                "start_time": "2024-01-20T08:00:00Z",
                "end_time": "2024-01-20T09:30:00Z",
                "total_score": 85.5
            }
        ],
        "favorites_count": 15,
        "is_favorited": false
    }
}
```

### 4.4 Update Exam (Teacher)
```
PUT /exams/{exam_id}/
```
**Request Body:**
```json
{
    "title": "Bai thi giua ky - Updated",
    "description": "Bai thi toan giua ky - Updated",
    "total_score": 120,
    "minutes": 100,
    "start_time": "2024-01-21T08:00:00Z",
    "end_time": "2024-01-21T10:00:00Z"
}
```
**Response:**
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
            "className": "Lop 12A1"
        },
        "created_by": {
            "id": 2,
            "fullName": "Nguyen Thi B",
            "email": "teacher@example.com"
        }
    },
    "message": "Exam updated successfully"
}
```

### 4.5 Delete Exam (Teacher)
```
DELETE /exams/{exam_id}/
```
**Response:**
```json
{
    "success": true,
    "message": "Exam deleted successfully"
}
```

### 4.6 Get Available Exams (Student)
```
GET /exams/available/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `class_id`: Filter by class
- `status`: upcoming, ongoing

**Response:**
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
                    "className": "Lop 12A1"
                },
                "created_by": {
                    "id": 2,
                    "fullName": "Nguyen Thi B",
                    "email": "teacher@example.com"
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
        "page": 1,
        "total_pages": 1
    }
}
```

### 4.7 Add Question to Exam (Teacher)
```
POST /exams/{exam_id}/questions/
```
**Request Body:**
```json
{
    "question_id": 3,
    "order": 3,
    "code": "Q3"
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 3,
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky"
        },
        "question": {
            "id": 3,
            "question_text": "What is 4+4?",
            "type": "multiple_choice",
            "difficulty": "easy"
        },
        "order": 3,
        "code": "Q3"
    },
    "message": "Question added to exam successfully"
}
```

### 4.8 Remove Question from Exam (Teacher)
```
DELETE /exams/{exam_id}/questions/{exam_question_id}/
```
**Response:**
```json
{
    "success": true,
    "message": "Question removed from exam successfully"
}
```

### 4.9 Update Exam Question Order (Teacher)
```
PUT /exams/{exam_id}/questions/{exam_question_id}/
```
**Request Body:**
```json
{
    "order": 2,
    "code": "Q2-Updated"
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky"
        },
        "question": {
            "id": 1,
            "question_text": "What is 2+2?"
        },
        "order": 2,
        "code": "Q2-Updated"
    },
    "message": "Exam question updated successfully"
}
```

### 4.10 Add to Favorites (Student)
```
POST /exams/{exam_id}/favorite/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "user": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky"
        },
        "created_at": "2024-01-15T10:00:00Z"
    },
    "message": "Exam added to favorites successfully"
}
```

### 4.11 Remove from Favorites (Student)
```
DELETE /exams/{exam_id}/favorite/
```
**Response:**
```json
{
    "success": true,
    "message": "Exam removed from favorites successfully"
}
```

### 4.12 Get Favorite Exams (Student)
```
GET /exams/favorites/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Response:**
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
                    "class_obj": {
                        "id": 1,
                        "className": "Lop 12A1"
                    },
                    "created_by": {
                        "id": 2,
                        "fullName": "Nguyen Thi B",
                        "email": "teacher@example.com"
                    },
                    "status": "upcoming"
                },
                "created_at": "2024-01-15T10:00:00Z"
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 4.13 Get Exam Statistics (Teacher)
```
GET /exams/{exam_id}/statistics/
```
**Response:**
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
            "completed_sessions": 20,
            "in_progress_sessions": 2,
            "abandoned_sessions": 1,
            "timeout_sessions": 2,
            "average_score": 78.5,
            "highest_score": 95.0,
            "lowest_score": 45.0,
            "completion_rate": 80.0
        },
        "score_distribution": {
            "0-20": 1,
            "21-40": 2,
            "41-60": 5,
            "61-80": 8,
            "81-100": 4
        }
    }
}
```

---

## 5. EXAM SESSIONS API (`/sessions/`)

### 5.1 Start Exam Session (Student)
```
POST /sessions/start/
```
**Request Body:**
```json
{
    "exam_id": 1
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky",
            "description": "Bai thi toan giua ky",
            "total_score": 100,
            "minutes": 90,
            "start_time": "2024-01-20T08:00:00Z",
            "end_time": "2024-01-20T10:00:00Z"
        },
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "code": "EXAM_20240120_001",
        "start_time": "2024-01-20T08:00:00Z",
        "end_time": null,
        "total_score": 0.0,
        "status": "in_progress",
        "submitted_at": null,
        "time_remaining": 5400,
        "questions": [
            {
                "id": 1,
                "exam_question": {
                    "id": 1,
                    "order": 1,
                    "code": "Q1",
                    "question": {
                        "id": 1,
                        "question_text": "What is 2+2?",
                        "type": "multiple_choice",
                        "difficulty": "easy",
                        "image_url": "https://example.com/image.jpg",
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

### 5.2 Get Active Session (Student)
```
GET /sessions/active/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky",
            "minutes": 90
        },
        "code": "EXAM_20240120_001",
        "start_time": "2024-01-20T08:00:00Z",
        "status": "in_progress",
        "time_remaining": 3600,
        "answered_count": 2,
        "total_questions": 5,
        "progress_percentage": 40.0
    }
}
```

### 5.3 Submit Answer (Student)
```
POST /sessions/{session_id}/answers/
```
**Request Body:**
```json
{
    "exam_question_id": 1,
    "selected_answer_id": 2,  // for multiple choice
    "answer_text": "My answer"  // for essay/fill blank
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "session": {
            "id": 1,
            "code": "EXAM_20240120_001"
        },
        "exam_question": {
            "id": 1,
            "order": 1,
            "code": "Q1",
            "question": {
                "id": 1,
                "question_text": "What is 2+2?",
                "type": "multiple_choice"
            }
        },
        "selected_answer": {
            "id": 2,
            "text": "4",
            "is_correct": true
        },
        "answer_text": null,
        "score": 20.0,
        "answered_at": "2024-01-20T08:15:00Z",
        "is_correct": true
    },
    "message": "Answer submitted successfully"
}
```

### 5.4 Update Answer (Student)
```
PUT /sessions/{session_id}/answers/{answer_id}/
```
**Request Body:**
```json
{
    "selected_answer_id": 1,  // change answer
    "answer_text": "Updated answer"
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "session": {
            "id": 1,
            "code": "EXAM_20240120_001"
        },
        "exam_question": {
            "id": 1,
            "order": 1,
            "code": "Q1"
        },
        "selected_answer": {
            "id": 1,
            "text": "3",
            "is_correct": false
        },
        "answer_text": "Updated answer",
        "score": 0.0,
        "answered_at": "2024-01-20T08:15:00Z",
        "is_correct": false
    },
    "message": "Answer updated successfully"
}
```

### 5.5 Submit Exam (Student)
```
POST /sessions/{session_id}/submit/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky"
        },
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C"
        },
        "total_score": 75.0,
        "correct_count": 3,
        "wrong_count": 2,
        "submitted_at": "2024-01-20T09:30:00Z",
        "status": "graded",
        "percentage": 75.0,
        "feedback": null,
        "session": {
            "id": 1,
            "code": "EXAM_20240120_001",
            "status": "completed",
            "end_time": "2024-01-20T09:30:00Z"
        }
    },
    "message": "Exam submitted successfully"
}
```

### 5.6 Get Session Detail (Student/Teacher)
```
GET /sessions/{session_id}/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky",
            "description": "Bai thi toan giua ky",
            "total_score": 100,
            "minutes": 90,
            "start_time": "2024-01-20T08:00:00Z",
            "end_time": "2024-01-20T10:00:00Z"
        },
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "code": "EXAM_20240120_001",
        "start_time": "2024-01-20T08:00:00Z",
        "end_time": "2024-01-20T09:30:00Z",
        "total_score": 75.0,
        "status": "completed",
        "submitted_at": "2024-01-20T09:30:00Z",
        "answers": [
            {
                "id": 1,
                "exam_question": {
                    "id": 1,
                    "order": 1,
                    "code": "Q1",
                    "question": {
                        "id": 1,
                        "question_text": "What is 2+2?",
                        "type": "multiple_choice",
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
                            }
                        ]
                    }
                },
                "selected_answer": {
                    "id": 2,
                    "text": "4",
                    "is_correct": true
                },
                "answer_text": null,
                "score": 20.0,
                "answered_at": "2024-01-20T08:15:00Z",
                "is_correct": true
            }
        ],
        "logs": [
            {
                "id": 1,
                "actions": "exam_started",
                "timestamp": "2024-01-20T08:00:00Z",
                "detail": "Student started the exam"
            },
            {
                "id": 2,
                "actions": "answer_submitted",
                "timestamp": "2024-01-20T08:15:00Z",
                "detail": "Answered question Q1"
            }
        ]
    }
}
```

### 5.7 Get Session Results (Student)
```
GET /sessions/{session_id}/result/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "session": {
            "id": 1,
            "code": "EXAM_20240120_001",
            "status": "completed"
        },
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky",
            "total_score": 100,
            "minutes": 90
        },
        "total_score": 75.0,
        "correct_count": 3,
        "wrong_count": 2,
        "submitted_at": "2024-01-20T09:30:00Z",
        "status": "graded",
        "feedback": "Good work! You did well on the basic concepts.",
        "percentage": 75.0,
        "grade": "B",
        "time_taken": 90,
        "answers_summary": [
            {
                "question_order": 1,
                "question_text": "What is 2+2?",
                "is_correct": true,
                "score": 20.0,
                "selected_answer": "4",
                "correct_answer": "4"
            },
            {
                "question_order": 2,
                "question_text": "What is 3+3?",
                "is_correct": false,
                "score": 0.0,
                "selected_answer": "5",
                "correct_answer": "6"
            }
        ]
    }
}
```

### 5.8 Get My Sessions (Student)
```
GET /sessions/my-sessions/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `status`: in_progress, completed, abandoned, timeout
- `exam_id`: Filter by exam

**Response:**
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
                    "class_obj": {
                        "id": 1,
                        "className": "Lop 12A1"
                    }
                },
                "code": "EXAM_20240120_001",
                "start_time": "2024-01-20T08:00:00Z",
                "end_time": "2024-01-20T09:30:00Z",
                "total_score": 75.0,
                "status": "completed",
                "submitted_at": "2024-01-20T09:30:00Z",
                "time_taken": 90,
                "percentage": 75.0
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 5.9 Get Class Sessions (Teacher)
```
GET /sessions/class/{class_id}/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `status`: in_progress, completed, abandoned, timeout
- `exam_id`: Filter by exam

**Response:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "exam": {
                    "id": 1,
                    "title": "Bai thi giua ky"
                },
                "student": {
                    "id": 3,
                    "fullName": "Nguyen Van C",
                    "email": "student@example.com"
                },
                "code": "EXAM_20240120_001",
                "start_time": "2024-01-20T08:00:00Z",
                "end_time": "2024-01-20T09:30:00Z",
                "total_score": 75.0,
                "status": "completed",
                "submitted_at": "2024-01-20T09:30:00Z",
                "time_taken": 90,
                "percentage": 75.0
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 5.10 Get Exam Sessions (Teacher)
```
GET /sessions/exam/{exam_id}/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `status`: in_progress, completed, abandoned, timeout

**Response:**
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
        "sessions": {
            "results": [
                {
                    "id": 1,
                    "student": {
                        "id": 3,
                        "fullName": "Nguyen Van C",
                        "email": "student@example.com"
                    },
                    "code": "EXAM_20240120_001",
                    "start_time": "2024-01-20T08:00:00Z",
                    "end_time": "2024-01-20T09:30:00Z",
                    "total_score": 75.0,
                    "status": "completed",
                    "submitted_at": "2024-01-20T09:30:00Z",
                    "time_taken": 90,
                    "percentage": 75.0
                }
            ],
            "count": 1,
            "page": 1,
            "total_pages": 1
        },
        "statistics": {
            "total_sessions": 25,
            "completed": 20,
            "in_progress": 2,
            "abandoned": 1,
            "timeout": 2,
            "average_score": 78.5,
            "completion_rate": 80.0
        }
    }
}
```

### 5.11 Get Session Logs (Student/Teacher)
```
GET /sessions/{session_id}/logs/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "session": {
            "id": 1,
            "code": "EXAM_20240120_001",
            "student": {
                "id": 3,
                "fullName": "Nguyen Van C"
            }
        },
        "logs": [
            {
                "id": 1,
                "actions": "exam_started",
                "timestamp": "2024-01-20T08:00:00Z",
                "detail": "Student started the exam"
            },
            {
                "id": 2,
                "actions": "answer_submitted",
                "timestamp": "2024-01-20T08:15:00Z",
                "detail": "Answered question Q1"
            },
            {
                "id": 3,
                "actions": "page_leave",
                "timestamp": "2024-01-20T08:20:00Z",
                "detail": "Student left the exam page"
            },
            {
                "id": 4,
                "actions": "page_return",
                "timestamp": "2024-01-20T08:25:00Z",
                "detail": "Student returned to exam page"
            },
            {
                "id": 5,
                "actions": "exam_submitted",
                "timestamp": "2024-01-20T09:30:00Z",
                "detail": "Student submitted the exam"
            }
        ]
    }
}
```

---

## 6. RESULTS API (`/results/`)

### 6.1 Get My Results (Student)
```
GET /results/my-results/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `exam_id`: Filter by exam
- `class_id`: Filter by class
- `status`: pending, graded, reviewed

**Response:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "session": {
                    "id": 1,
                    "code": "EXAM_20240120_001",
                    "status": "completed"
                },
                "student": {
                    "id": 3,
                    "fullName": "Nguyen Van C",
                    "email": "student@example.com"
                },
                "exam": {
                    "id": 1,
                    "title": "Bai thi giua ky",
                    "class_obj": {
                        "id": 1,
                        "className": "Lop 12A1"
                    },
                    "total_score": 100,
                    "minutes": 90
                },
                "total_score": 75.0,
                "correct_count": 3,
                "wrong_count": 2,
                "submitted_at": "2024-01-20T09:30:00Z",
                "status": "graded",
                "feedback": "Good work! You did well on the basic concepts.",
                "percentage": 75.0,
                "grade": "B",
                "time_taken": 90
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 6.2 Get Class Results (Teacher)
```
GET /results/class/{class_id}/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `exam_id`: Filter by exam
- `status`: pending, graded, reviewed

**Response:**
```json
{
    "success": true,
    "data": {
        "class": {
            "id": 1,
            "className": "Lop 12A1"
        },
        "results": {
            "results": [
                {
                    "id": 1,
                    "session": {
                        "id": 1,
                        "code": "EXAM_20240120_001"
                    },
                    "student": {
                        "id": 3,
                        "fullName": "Nguyen Van C",
                        "email": "student@example.com"
                    },
                    "exam": {
                        "id": 1,
                        "title": "Bai thi giua ky",
                        "total_score": 100
                    },
                    "total_score": 75.0,
                    "correct_count": 3,
                    "wrong_count": 2,
                    "submitted_at": "2024-01-20T09:30:00Z",
                    "status": "graded",
                    "percentage": 75.0,
                    "grade": "B"
                }
            ],
            "count": 1,
            "page": 1,
            "total_pages": 1
        },
        "statistics": {
            "total_students": 25,
            "completed_exams": 20,
            "average_score": 78.5,
            "highest_score": 95.0,
            "lowest_score": 45.0,
            "grade_distribution": {
                "A": 5,
                "B": 8,
                "C": 5,
                "D": 2,
                "F": 0
            }
        }
    }
}
```

### 6.3 Get Exam Results (Teacher)
```
GET /results/exam/{exam_id}/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `status`: pending, graded, reviewed

**Response:**
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
        "results": {
            "results": [
                {
                    "id": 1,
                    "session": {
                        "id": 1,
                        "code": "EXAM_20240120_001"
                    },
                    "student": {
                        "id": 3,
                        "fullName": "Nguyen Van C",
                        "email": "student@example.com"
                    },
                    "total_score": 75.0,
                    "correct_count": 3,
                    "wrong_count": 2,
                    "submitted_at": "2024-01-20T09:30:00Z",
                    "status": "graded",
                    "feedback": "Good work!",
                    "percentage": 75.0,
                    "grade": "B",
                    "time_taken": 90
                }
            ],
            "count": 1,
            "page": 1,
            "total_pages": 1
        },
        "statistics": {
            "total_sessions": 25,
            "completed_sessions": 20,
            "average_score": 78.5,
            "highest_score": 95.0,
            "lowest_score": 45.0,
            "completion_rate": 80.0,
            "score_distribution": {
                "0-20": 1,
                "21-40": 2,
                "41-60": 5,
                "61-80": 8,
                "81-100": 4
            }
        }
    }
}
```

### 6.4 Get Student Results (Teacher)
```
GET /results/student/{student_id}/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `class_id`: Filter by class
- `exam_id`: Filter by exam

**Response:**
```json
{
    "success": true,
    "data": {
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com",
            "role": "student"
        },
        "results": {
            "results": [
                {
                    "id": 1,
                    "session": {
                        "id": 1,
                        "code": "EXAM_20240120_001"
                    },
                    "exam": {
                        "id": 1,
                        "title": "Bai thi giua ky",
                        "class_obj": {
                            "id": 1,
                            "className": "Lop 12A1"
                        },
                        "total_score": 100
                    },
                    "total_score": 75.0,
                    "correct_count": 3,
                    "wrong_count": 2,
                    "submitted_at": "2024-01-20T09:30:00Z",
                    "status": "graded",
                    "feedback": "Good work!",
                    "percentage": 75.0,
                    "grade": "B",
                    "time_taken": 90
                }
            ],
            "count": 1,
            "page": 1,
            "total_pages": 1
        },
        "statistics": {
            "total_exams": 5,
            "completed_exams": 4,
            "average_score": 78.5,
            "highest_score": 95.0,
            "lowest_score": 45.0,
            "improvement_trend": "increasing"
        }
    }
}
```

### 6.5 Grade Exam (Teacher)
```
POST /results/{result_id}/grade/
```
**Request Body:**
```json
{
    "feedback": "Good work! You did well on the basic concepts.",
    "status": "graded"
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "session": {
            "id": 1,
            "code": "EXAM_20240120_001"
        },
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky"
        },
        "total_score": 75.0,
        "correct_count": 3,
        "wrong_count": 2,
        "submitted_at": "2024-01-20T09:30:00Z",
        "status": "graded",
        "feedback": "Good work! You did well on the basic concepts.",
        "percentage": 75.0
    },
    "message": "Exam graded successfully"
}
```

### 6.6 Get Result Detail (Student/Teacher)
```
GET /results/{result_id}/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "session": {
            "id": 1,
            "code": "EXAM_20240120_001",
            "status": "completed",
            "start_time": "2024-01-20T08:00:00Z",
            "end_time": "2024-01-20T09:30:00Z"
        },
        "student": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "exam": {
            "id": 1,
            "title": "Bai thi giua ky",
            "description": "Bai thi toan giua ky",
            "total_score": 100,
            "minutes": 90,
            "class_obj": {
                "id": 1,
                "className": "Lop 12A1"
            }
        },
        "total_score": 75.0,
        "correct_count": 3,
        "wrong_count": 2,
        "submitted_at": "2024-01-20T09:30:00Z",
        "status": "graded",
        "feedback": "Good work! You did well on the basic concepts.",
        "percentage": 75.0,
        "grade": "B",
        "time_taken": 90,
        "answers_summary": [
            {
                "question_order": 1,
                "question_text": "What is 2+2?",
                "question_type": "multiple_choice",
                "is_correct": true,
                "score": 20.0,
                "selected_answer": "4",
                "correct_answer": "4",
                "answered_at": "2024-01-20T08:15:00Z"
            }
        ]
    }
}
```

---

## 7. NOTIFICATIONS API (`/notifications/`)

### 7.1 Get My Notifications
```
GET /notifications/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `is_read`: Filter by read status (true/false)
- `related_exam_id`: Filter by related exam

**Response:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "user": {
                    "id": 3,
                    "fullName": "Nguyen Van C",
                    "email": "student@example.com"
                },
                "title": "New Exam Available",
                "message": "A new exam 'Bai thi giua ky' is now available for your class 'Lop 12A1'",
                "created_at": "2024-01-20T08:00:00Z",
                "is_read": false,
                "related_exam": {
                    "id": 1,
                    "title": "Bai thi giua ky",
                    "class_obj": {
                        "id": 1,
                        "className": "Lop 12A1"
                    }
                }
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1,
        "unread_count": 1
    }
}
```

### 7.2 Mark as Read
```
PUT /notifications/{notification_id}/read/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "user": {
            "id": 3,
            "fullName": "Nguyen Van C"
        },
        "title": "New Exam Available",
        "message": "A new exam 'Bai thi giua ky' is now available for your class 'Lop 12A1'",
        "created_at": "2024-01-20T08:00:00Z",
        "is_read": true,
        "related_exam": {
            "id": 1,
            "title": "Bai thi giua ky"
        }
    },
    "message": "Notification marked as read"
}
```

### 7.3 Mark All as Read
```
PUT /notifications/mark-all-read/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "updated_count": 5
    },
    "message": "All notifications marked as read"
}
```

### 7.4 Get Unread Count
```
GET /notifications/unread-count/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "unread_count": 3
    }
}
```

### 7.5 Create Notification (System/Teacher)
```
POST /notifications/
```
**Request Body:**
```json
{
    "user_id": 3,
    "title": "Exam Result Ready",
    "message": "Your exam result for 'Bai thi giua ky' is now available",
    "related_exam_id": 1
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 2,
        "user": {
            "id": 3,
            "fullName": "Nguyen Van C",
            "email": "student@example.com"
        },
        "title": "Exam Result Ready",
        "message": "Your exam result for 'Bai thi giua ky' is now available",
        "created_at": "2024-01-20T10:00:00Z",
        "is_read": false,
        "related_exam": {
            "id": 1,
            "title": "Bai thi giua ky"
        }
    },
    "message": "Notification created successfully"
}
```

---

## 8. ADMIN API (`/admin/`)

### 8.1 Get All Users (Admin)
```
GET /admin/users/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `role`: Filter by role (student, teacher, admin)
- `search`: Search by name or email
- `is_active`: Filter by active status

**Response:**
```json
{
    "success": true,
    "data": {
        "results": [
            {
                "id": 1,
                "email": "student@example.com",
                "fullName": "Nguyen Van A",
                "role": "student",
                "created_at": "2024-01-15T08:00:00Z",
                "last_login": "2024-01-20T10:30:00Z",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false,
                "statistics": {
                    "total_exams": 5,
                    "completed_exams": 4,
                    "average_score": 78.5
                }
            }
        ],
        "count": 1,
        "page": 1,
        "total_pages": 1
    }
}
```

### 8.2 Create User (Admin)
```
POST /admin/users/
```
**Request Body:**
```json
{
    "email": "newstudent@example.com",
    "password": "password123",
    "fullName": "Nguyen Van D",
    "role": "student",
    "is_active": true
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 4,
        "email": "newstudent@example.com",
        "fullName": "Nguyen Van D",
        "role": "student",
        "created_at": "2024-01-20T10:00:00Z",
        "last_login": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    },
    "message": "User created successfully"
}
```

### 8.3 Update User (Admin)
```
PUT /admin/users/{user_id}/
```
**Request Body:**
```json
{
    "fullName": "Nguyen Van D - Updated",
    "role": "teacher",
    "is_active": true
}
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 4,
        "email": "newstudent@example.com",
        "fullName": "Nguyen Van D - Updated",
        "role": "teacher",
        "created_at": "2024-01-20T10:00:00Z",
        "last_login": null,
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    },
    "message": "User updated successfully"
}
```

### 8.4 Delete User (Admin)
```
DELETE /admin/users/{user_id}/
```
**Response:**
```json
{
    "success": true,
    "message": "User deleted successfully"
}
```

### 8.5 Get System Statistics (Admin)
```
GET /admin/statistics/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "users": {
            "total_users": 150,
            "students": 120,
            "teachers": 25,
            "admins": 5,
            "active_users": 140,
            "new_users_this_month": 15
        },
        "classes": {
            "total_classes": 30,
            "active_classes": 28,
            "average_students_per_class": 4.0
        },
        "exams": {
            "total_exams": 200,
            "completed_exams": 150,
            "upcoming_exams": 30,
            "ongoing_exams": 20
        },
        "sessions": {
            "total_sessions": 3000,
            "completed_sessions": 2500,
            "in_progress_sessions": 50,
            "abandoned_sessions": 100,
            "timeout_sessions": 50
        },
        "questions": {
            "total_questions": 500,
            "multiple_choice": 300,
            "true_false": 100,
            "fill_blank": 50,
            "essay": 50
        },
        "notifications": {
            "total_notifications": 1000,
            "unread_notifications": 150
        },
        "performance": {
            "average_exam_score": 75.5,
            "completion_rate": 83.3,
            "system_uptime": "99.9%"
        }
    }
}
```

### 8.6 Get User Detail (Admin)
```
GET /admin/users/{user_id}/
```
**Response:**
```json
{
    "success": true,
    "data": {
        "id": 3,
        "email": "student@example.com",
        "fullName": "Nguyen Van C",
        "role": "student",
        "created_at": "2024-01-15T08:00:00Z",
        "last_login": "2024-01-20T10:30:00Z",
        "is_active": true,
        "is_staff": false,
        "is_superuser": false,
        "enrolled_classes": [
            {
                "id": 1,
                "class_obj": {
                    "id": 1,
                    "className": "Lop 12A1"
                },
                "joined_at": "2024-01-15T09:00:00Z"
            }
        ],
        "exam_sessions": [
            {
                "id": 1,
                "exam": {
                    "id": 1,
                    "title": "Bai thi giua ky"
                },
                "status": "completed",
                "total_score": 75.0,
                "submitted_at": "2024-01-20T09:30:00Z"
            }
        ],
        "statistics": {
            "total_exams": 5,
            "completed_exams": 4,
            "average_score": 78.5,
            "highest_score": 95.0,
            "lowest_score": 45.0
        }
    }
}
```

---

## Response Format

### Success Response
```json
{
    "success": true,
    "data": {
        // response data
    },
    "message": "Success message"
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Error message",
        "details": {}
    }
}
```

### Pagination Response
```json
{
    "success": true,
    "data": {
        "results": [],
        "count": 100,
        "next": "http://api.com/endpoint/?page=2",
        "previous": null,
        "page": 1,
        "total_pages": 10
    }
}
```

---

## HTTP Status Codes

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

---

## Rate Limiting

- **General API**: 1000 requests/hour per user
- **Auth API**: 10 requests/hour per IP
- **Exam Submission**: 1 request/minute per user

---

## WebSocket Events (Real-time)

### Exam Session Events
- `exam_started` - When student starts exam
- `answer_submitted` - When student submits answer
- `time_warning` - 5 minutes before exam ends
- `exam_ended` - When exam time expires

### Notification Events
- `new_notification` - When new notification is created
- `exam_available` - When new exam is available
- `result_ready` - When exam result is ready
