-- Booking System Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS booking_db;
USE booking_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Bookings table
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

-- Insert sample data (optional, for testing)
-- Note: The password 'password123' is hashed using werkzeug.security
-- You should create users through the registration form in production

-- Sample user (password: password123)
-- INSERT INTO users (username, email, password) VALUES
-- ('demo_user', 'demo@example.com', 'pbkdf2:sha256:600000$...');

-- Sample booking
-- INSERT INTO bookings (user_id, service_name, booking_date, booking_time, customer_name, customer_email, customer_phone, notes, status)
-- VALUES (1, 'Consultation', '2025-12-30', '14:00:00', 'John Doe', 'john@example.com', '+1234567890', 'First consultation', 'confirmed');
