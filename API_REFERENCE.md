# API Endpoints Reference

## Authentication Endpoints

### Register User
- **URL**: `/auth/api/register`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response**: `201 CREATED`
  ```json
  {
    "message": "User registered successfully",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "user"
    }
  }
  ```

### Login
- **URL**: `/auth/api/login`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response (Admin)**: `200 OK`
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": "admin",
      "username": "Admin",
      "email": "admin@gmail.com",
      "role": "admin"
    },
    "redirect": "/admin/dashboard"
  }
  ```
- **Success Response (User)**: `200 OK`
  ```json
  {
    "message": "Login successful",
    "user": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "user"
    },
    "redirect": "/my-bookings"
  }
  ```

### Logout
- **URL**: `/auth/api/logout`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

## Admin Endpoints

### Get Dashboard Statistics
- **URL**: `/admin/api/dashboard-stats`
- **Method**: `GET`
- **Auth Required**: Yes (Admin only)
- **Success Response**: `200 OK`
  ```json
  {
    "totalUsers": 10,
    "totalBookings": 25,
    "pendingBookings": 5,
    "recentBookings": [...],
    "allUsers": [...]
  }
  ```

### Update Booking Status
- **URL**: `/admin/api/bookings/:booking_id/status`
- **Method**: `PUT`
- **Auth Required**: Yes (Admin only)
- **URL Parameters**: `booking_id` (integer)
- **Body**:
  ```json
  {
    "status": "pending|confirmed|cancelled|completed"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Booking status updated successfully"
  }
  ```

### Get All Users
- **URL**: `/admin/api/users`
- **Method**: `GET`
- **Auth Required**: Yes (Admin only)
- **Success Response**: `200 OK`
  ```json
  {
    "users": [
      {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com",
        "role": "user",
        "created_at": "2025-01-01T10:00:00"
      }
    ]
  }
  ```

### Get All Bookings
- **URL**: `/admin/api/bookings`
- **Method**: `GET`
- **Auth Required**: Yes (Admin only)
- **Success Response**: `200 OK`
  ```json
  {
    "bookings": [
      {
        "id": 1,
        "user_id": 1,
        "service_name": "Consultation",
        "booking_date": "2025-12-30",
        "booking_time": "14:00:00",
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "customer_phone": "+1234567890",
        "notes": "First consultation",
        "status": "pending",
        "created_at": "2025-12-28T10:00:00",
        "updated_at": "2025-12-28T10:00:00",
        "username": "john_doe"
      }
    ]
  }
  ```

## Page Routes

### Public Pages
- `/` - Home page
- `/auth/login` - Login page
- `/auth/register` - Registration page

### User Pages (Login Required)
- `/my-bookings` - User's bookings page
- `/booking` - Create new booking page

### Admin Pages (Admin Login Required)
- `/admin/dashboard` - Admin dashboard with statistics and management tools

## Error Responses

### 400 Bad Request
```json
{
  "error": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "error": "Admin access required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 409 Conflict
```json
{
  "error": "Email already registered"
}
```

### 500 Internal Server Error
```json
{
  "error": "Server error message"
}
```

## Role-Based Access Control

### Admin Access
- Can access all `/admin/*` routes
- Can view all users and bookings
- Can update booking statuses
- Cannot access regular user booking management pages

### User Access
- Can access their own booking pages
- Cannot access admin dashboard or API endpoints
- Can create, view, and manage their own bookings

### Public Access
- Home page
- Login page
- Registration page
