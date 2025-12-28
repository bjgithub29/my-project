# Role-Based Authentication Setup Instructions

## Overview
This system now implements role-based authentication with two roles:
- **Admin**: Single admin user with fixed credentials
- **User**: All other registered users

## Database Configuration

### Database Details
- **Database Name**: `ticket_system`
- **Database Password**: `` (empty/null)
- **Database User**: `root`
- **Database Host**: `localhost`

## Admin Credentials

The system has one fixed admin account:
- **Email**: `admin@gmail.com`
- **Password**: `Admin@123`

## Setup Steps

### 1. Create the Database
Run the following SQL commands to set up the database:

```bash
mysql -u root -p
```

Then execute the schema file:
```sql
source database/schema.sql
```

Or manually run:
```sql
CREATE DATABASE IF NOT EXISTS ticket_system;
USE ticket_system;

-- Create users table with role column
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    service_name VARCHAR(150) NOT NULL,
    booking_date DATE NOT NULL,
    booking_time TIME NOT NULL,
    customer_name VARCHAR(150) NOT NULL,
    customer_email VARCHAR(150) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    notes TEXT,
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_booking_date (booking_date),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

The application will run on: `http://localhost:8000`

## How It Works

### User Login Flow
1. Users navigate to `/auth/login`
2. Enter credentials
3. System checks if credentials match admin credentials:
   - **If Admin**: User is logged in as admin and redirected to `/admin/dashboard`
   - **If Regular User**: User credentials are verified against database and redirected to `/my-bookings`

### Admin Features
- View dashboard with statistics (total users, total bookings, pending bookings)
- View all bookings from all users
- Update booking status (confirm, cancel, complete)
- View all registered users

### User Features
- Register new account (automatically assigned 'user' role)
- Login and manage their own bookings
- Cannot access admin dashboard

### Access Control
- **Admin-only routes**: `/admin/dashboard` and all `/admin/api/*` endpoints
- **User-only routes**: Regular booking management routes
- **Public routes**: Login, Register, Home page

## Key Files Modified

1. **config/config.py**: Updated database name to `ticket_system` and added admin credentials
2. **database/schema.sql**: Updated database name and added `role` column to users table
3. **models/user.py**: Updated to handle user roles
4. **routes/auth_routes.py**: Added admin authentication logic
5. **middleware/auth_middleware.py**: Added `admin_required` and `user_required` decorators
6. **routes/admin_routes.py**: New file with admin routes and API endpoints
7. **templates/admin_dashboard.html**: New admin dashboard template
8. **app.py**: Registered admin blueprint
9. **templates/login.html**: Updated to handle role-based redirects

## Testing the Implementation

### Test Admin Login
1. Go to `http://localhost:8000/auth/login`
2. Enter:
   - Email: `admin@gmail.com`
   - Password: `Admin@123`
3. You should be redirected to `/admin/dashboard`

### Test User Registration & Login
1. Go to `http://localhost:8000/auth/register`
2. Register a new user
3. Login with the registered credentials
4. You should be redirected to `/my-bookings`
5. Trying to access `/admin/dashboard` will redirect you back to user pages

## Security Features

- Admin credentials are stored in config (not in database)
- Passwords are hashed using werkzeug security
- Session-based authentication
- Role-based access control using decorators
- Automatic redirection based on user role
