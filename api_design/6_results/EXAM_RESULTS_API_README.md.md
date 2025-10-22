## 6. RESULTS API (`/results/`)

### Overview
Results API cung cấp các endpoint để truy xuất kết quả bài thi (`ExamResult`) theo nhiều ngữ cảnh (của tôi, theo lớp, theo bài thi, theo học sinh), xem chi tiết, và chấm điểm/ghi phản hồi. Các endpoint sử dụng model `ExamResult` thuộc app `exam_sessions`.

### Base URL
`http://localhost:8000/results/`

### Authentication
- Tất cả endpoint yêu cầu JWT: `Authorization: Bearer <access_token>`
- Quyền truy cập:
  - Students: chỉ truy vấn được kết quả của chính mình (my-results, result detail nếu là owner)
  - Teachers: xem kết quả/ thống kê lớp mình dạy, bài thi do mình phụ trách; chấm điểm kết quả thuộc lớp mình
  - Admins: truy cập tất cả

---

### 6.1 Get My Results (Student)
```
GET /results/my-results/
```
Query params:
- `page` (mặc định: 1)
- `page_size` (mặc định: 20, tối đa: 100)
- `exam_id`: lọc theo bài thi
- `class_id`: lọc theo lớp
- `status`: pending | graded | reviewed

Response (200 OK) - dạng phân trang DRF chuẩn:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 13,
      "session": { "id": 15, "code": "EXAM_20251022_XXXX", "status": "completed" },
      "student": { "id": 123, "email": "student@example.com", "fullName": "Test Student", "role": "student", "created_at": "...", "last_login": "...", "is_active": true, "is_staff": false, "is_superuser": false },
      "exam": { "id": 38, "title": "Midterm Exam", "description": "Mathematics Midterm", "total_score": 100, "minutes": 60, "start_time": "...", "end_time": "...", "class_obj": { "id": 63, "className": "Test Class 2024", "teacher": { "id": 2, "email": "teacher@example.com", "fullName": "Test Teacher", "role": "teacher", "created_at": "...", "last_login": "...", "is_active": true, "is_staff": false, "is_superuser": false } }, "created_by": { "id": 2, "email": "teacher@example.com", "fullName": "Test Teacher", "role": "teacher", "created_at": "...", "last_login": "...", "is_active": true, "is_staff": false, "is_superuser": false } },
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
  ]
}
```

---

### 6.2 Get Class Results (Teacher/Admin)
```
GET /results/class/{class_id}/
```
Query params:
- `page`, `page_size`
- `exam_id`
- `status`: pending | graded | reviewed

Response (200 OK):
```json
{
  "success": true,
  "data": {
    "class": { "id": 63 },
    "results": {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 13,
          "session": { "id": 15, "code": "EXAM_20251022_XXXX", "status": "completed" },
          "student": { "id": 123, "email": "student@example.com", "fullName": "Test Student", "role": "student", "created_at": "...", "last_login": "...", "is_active": true, "is_staff": false, "is_superuser": false },
          "exam": { "id": 38, "title": "Midterm Exam", "total_score": 100, "minutes": 60 },
          "total_score": "100.00",
          "correct_count": 1,
          "wrong_count": 0,
          "submitted_at": "2025-10-22T06:44:12.628878Z",
          "status": "graded",
          "percentage": "100.00",
          "grade": "A",
          "time_taken": 0
        }
      ]
    },
    "statistics": {
      "total_students": 1,
      "completed_exams": 1,
      "average_score": 100.0,
      "highest_score": 100.0,
      "lowest_score": 100.0,
      "grade_distribution": { "A": 1, "B": 0, "C": 0, "D": 0, "F": 0 }
    }
  }
}
```

---

### 6.3 Get Exam Results (Teacher/Admin)
```
GET /results/exam/{exam_id}/
```
Query params:
- `page`, `page_size`
- `status`: pending | graded | reviewed

Response (200 OK):
```json
{
  "success": true,
  "data": {
    "exam": { "id": 38, "title": "Midterm Exam", "total_score": 100, "minutes": 60 },
    "results": {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 13,
          "session": { "id": 15, "code": "EXAM_20251022_XXXX", "status": "completed" },
          "student": { "id": 123, "email": "student@example.com", "fullName": "Test Student", "role": "student", "created_at": "...", "last_login": "...", "is_active": true, "is_staff": false, "is_superuser": false },
          "total_score": "100.00",
          "correct_count": 1,
          "wrong_count": 0,
          "submitted_at": "2025-10-22T06:44:12.628878Z",
          "status": "graded",
          "feedback": null,
          "percentage": "100.00",
          "grade": "A",
          "time_taken": 0
        }
      ]
    },
    "statistics": {
      "total_sessions": 1,
      "completed_sessions": 1,
      "average_score": 100.0,
      "highest_score": 100.0,
      "lowest_score": 100.0,
      "completion_rate": 100.0,
      "score_distribution": { "0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 1 }
    }
  }
}
```

---

### 6.4 Get Student Results (Teacher/Admin)
```
GET /results/student/{student_id}/
```
Query params:
- `page`, `page_size`
- `class_id`: lọc theo lớp (teacher phải là giáo viên của lớp đó)
- `exam_id`: lọc theo bài thi

Response (200 OK):
```json
{
  "success": true,
  "data": {
    "student": { "id": 123, "fullName": "Test Student", "email": "student@example.com", "role": "student" },
    "results": {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 13,
          "session": { "id": 15, "code": "EXAM_20251022_XXXX" },
          "exam": { "id": 38, "title": "Midterm Exam", "class_obj": { "id": 63, "className": "Test Class 2024" }, "total_score": 100 },
          "total_score": "100.00",
          "correct_count": 1,
          "wrong_count": 0,
          "submitted_at": "2025-10-22T06:44:12.628878Z",
          "status": "graded",
          "feedback": null,
          "percentage": "100.00",
          "grade": "A",
          "time_taken": 0
        }
      ]
    },
    "statistics": {
      "total_exams": 1,
      "completed_exams": 1,
      "average_score": 100.0,
      "highest_score": 100.0,
      "lowest_score": 100.0,
      "improvement_trend": "unknown"
    }
  }
}
```

---

### 6.5 Grade Result (Teacher/Admin)
```
POST /results/{result_id}/grade/
```
Body:
```json
{
  "feedback": "Good work!",
  "status": "graded"
}
```

Response (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 13,
    "session": { "id": 15, "code": "EXAM_20251022_XXXX", "status": "completed" },
    "student": { "id": 123, "email": "student@example.com", "fullName": "Test Student", "role": "student", "created_at": "...", "last_login": "...", "is_active": true, "is_staff": false, "is_superuser": false },
    "exam": { "id": 38, "title": "Midterm Exam" },
    "total_score": "100.00",
    "correct_count": 1,
    "wrong_count": 0,
    "submitted_at": "2025-10-22T06:44:12.628878Z",
    "status": "graded",
    "feedback": "Good work!",
    "percentage": "100.00",
    "grade": "A",
    "time_taken": 0,
    "answers_summary": [
      { "question_order": 1, "question_text": "What is 2 + 2?", "is_correct": true, "score": 100.0, "selected_answer": "4", "correct_answer": "4" }
    ]
  },
  "message": "Exam graded successfully"
}
```

---

### 6.6 Get Result Detail (Owner/Teacher/Admin)
```
GET /results/{result_id}/
```
Response (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 13,
    "session": { "id": 15, "code": "EXAM_20251022_XXXX", "status": "completed", "start_time": "...", "end_time": "..." },
    "student": { "id": 123, "fullName": "Test Student", "email": "student@example.com" },
    "exam": { "id": 38, "title": "Midterm Exam", "description": "Mathematics Midterm", "total_score": 100, "minutes": 60, "class_obj": { "id": 63, "className": "Test Class 2024" } },
    "total_score": "100.00",
    "correct_count": 1,
    "wrong_count": 0,
    "submitted_at": "2025-10-22T06:44:12.628878Z",
    "status": "graded",
    "feedback": "Good work!",
    "percentage": "100.00",
    "grade": "A",
    "time_taken": 0,
    "answers_summary": [
      { "question_order": 1, "question_text": "What is 2 + 2?", "is_correct": true, "score": 100.0, "selected_answer": "4", "correct_answer": "4" }
    ]
  }
}
```

---

### Error Responses
Format chung:
```json
{
  "success": false,
  "errors": { "field_name": ["Error message"] },
  "message": "Error description"
}
```

Các lỗi phổ biến:
- `401 Unauthorized`: Thiếu/invalid token
- `403 Forbidden`: Không đủ quyền (ví dụ teacher xem lớp không phải của mình)
- `404 Not Found`: Exam/Class/Result không tồn tại
- `400 Bad Request`: Tham số/giá trị không hợp lệ (vd: `status` sai)

---

### Notes
- `my-results` trả về dạng phân trang DRF mặc định.
- Các endpoint còn lại trả JSON có `success: true` và `data` bao bọc kết quả và thống kê.

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


