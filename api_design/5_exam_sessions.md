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

