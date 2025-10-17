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