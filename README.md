# Booking System

A minimal and modern booking system with user authentication and REST APIs built with Flask.

## Features

- 🔐 User Authentication (Register, Login, Logout)
- 📅 Booking Management (Create, Read, Update, Delete)
- 🎨 Minimal and Modern UI
- 🔒 Secure Password Hashing
- 📱 Responsive Design
- 🚀 RESTful API

## Folder Structure

```
ecommerce/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── config/
│   └── config.py          # Application configuration
├── database/
│   ├── schema.sql         # Database schema
│   └── init_db.py         # Database initialization script
├── middleware/
│   └── auth_middleware.py # Authentication middleware
├── models/
│   ├── user.py            # User model
│   └── booking.py         # Booking model
├── routes/
│   ├── auth_routes.py     # Authentication routes
│   └── booking_routes.py  # Booking routes
├── templates/
│   ├── index.html         # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── booking.html       # Create booking page
│   └── my_bookings.html   # User bookings page
├── static/
│   ├── css/
│   ├── images/
│   └── js/
└── utils/
    └── db.py              # Database utilities
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update with your MySQL credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=booking_db
SECRET_KEY=your-secret-key
```

### 3. Initialize Database

Run the database initialization script:

```bash
python database/init_db.py
```

Or manually execute the SQL schema:
```bash
mysql -u root -p < database/schema.sql
```

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- **POST** `/auth/api/register` - Register a new user
  ```json
  {
    "username": "john",
    "email": "john@example.com",
    "password": "password123"
  }
  ```

- **POST** `/auth/api/login` - Login user
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```

- **POST** `/auth/api/logout` - Logout user

- **GET** `/auth/api/me` - Get current user info

### Bookings

- **POST** `/booking/api/bookings` - Create a new booking
  ```json
  {
    "service_name": "Consultation",
    "booking_date": "2025-12-30",
    "booking_time": "14:00",
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "customer_phone": "+1234567890",
    "notes": "Optional notes"
  }
  ```

- **GET** `/booking/api/bookings` - Get all bookings for logged-in user

- **GET** `/booking/api/bookings/<id>` - Get specific booking

- **PATCH** `/booking/api/bookings/<id>/status` - Update booking status
  ```json
  {
    "status": "confirmed"
  }
  ```
  Status options: `pending`, `confirmed`, `cancelled`, `completed`

- **DELETE** `/booking/api/bookings/<id>` - Delete a booking

## Pages

- `/` - Home page (redirects to login if not authenticated)
- `/auth/login` - Login page
- `/auth/register` - Registration page
- `/booking/` - Create new booking
- `/booking/my-bookings` - View all user bookings

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Authentication**: Session-based with password hashing
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Styling**: Custom CSS with gradient design

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- CSRF protection
- SQL injection prevention
- Input validation

## Development

To run in development mode:

```bash
python app.py
```

The application runs with debug mode enabled by default.

## License

MIT License
