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


