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
