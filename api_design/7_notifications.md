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


