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