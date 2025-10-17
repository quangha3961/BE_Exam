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


