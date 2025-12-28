"""
Database Migration Script
This script helps migrate from the old booking_db to the new ticket_system database
and adds the role column to the users table.
"""

import mysql.connector
from mysql.connector import Error

def migrate_database():
    """Migrate database from booking_db to ticket_system"""
    
    # Database connection parameters
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': ''  # Empty password as specified
    }
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("Connected to MySQL server successfully!")
        
        # Create new database
        print("\n1. Creating ticket_system database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS ticket_system")
        print("✓ Database ticket_system created/verified")
        
        # Use the new database
        cursor.execute("USE ticket_system")
        
        # Check if users table exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'ticket_system'
            AND table_name = 'users'
        """)
        
        users_table_exists = cursor.fetchone()[0] > 0
        
        if users_table_exists:
            print("\n2. Checking if role column exists...")
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_schema = 'ticket_system'
                AND table_name = 'users'
                AND column_name = 'role'
            """)
            
            role_column_exists = cursor.fetchone()[0] > 0
            
            if not role_column_exists:
                print("Adding role column to users table...")
                cursor.execute("""
                    ALTER TABLE users
                    ADD COLUMN role ENUM('admin', 'user') DEFAULT 'user'
                    AFTER password
                """)
                connection.commit()
                print("✓ Role column added successfully")
            else:
                print("✓ Role column already exists")
        else:
            print("\n2. Creating users table...")
            cursor.execute("""
                CREATE TABLE users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    email VARCHAR(150) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role ENUM('admin', 'user') DEFAULT 'user',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            connection.commit()
            print("✓ Users table created successfully")
        
        # Check if bookings table exists
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = 'ticket_system'
            AND table_name = 'bookings'
        """)
        
        bookings_table_exists = cursor.fetchone()[0] > 0
        
        if not bookings_table_exists:
            print("\n3. Creating bookings table...")
            cursor.execute("""
                CREATE TABLE bookings (
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
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            connection.commit()
            print("✓ Bookings table created successfully")
        else:
            print("\n3. Bookings table already exists")
        
        # Optional: Migrate data from old database
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.schemata
            WHERE schema_name = 'booking_db'
        """)
        
        old_db_exists = cursor.fetchone()[0] > 0
        
        if old_db_exists:
            print("\n4. Found old booking_db database")
            migrate_choice = input("Do you want to migrate data from booking_db? (y/n): ")
            
            if migrate_choice.lower() == 'y':
                print("Migrating users...")
                cursor.execute("""
                    INSERT INTO ticket_system.users (id, username, email, password, created_at, role)
                    SELECT id, username, email, password, created_at, 'user'
                    FROM booking_db.users
                    WHERE email NOT IN (SELECT email FROM ticket_system.users)
                """)
                users_migrated = cursor.rowcount
                connection.commit()
                print(f"✓ Migrated {users_migrated} users")
                
                print("Migrating bookings...")
                cursor.execute("""
                    INSERT INTO ticket_system.bookings
                    SELECT *
                    FROM booking_db.bookings
                    WHERE id NOT IN (SELECT id FROM ticket_system.bookings)
                """)
                bookings_migrated = cursor.rowcount
                connection.commit()
                print(f"✓ Migrated {bookings_migrated} bookings")
        
        print("\n" + "="*50)
        print("✓ Migration completed successfully!")
        print("="*50)
        print("\nDatabase: ticket_system")
        print("Admin Email: admin@gmail.com")
        print("Admin Password: Admin@123")
        print("\nYou can now run your application with: python app.py")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"\n✗ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("="*50)
    print("Database Migration Script")
    print("="*50)
    print("\nThis script will:")
    print("1. Create ticket_system database")
    print("2. Create/update users table with role column")
    print("3. Create bookings table if not exists")
    print("4. Optionally migrate data from booking_db")
    print("\n" + "="*50)
    
    proceed = input("\nDo you want to proceed? (y/n): ")
    
    if proceed.lower() == 'y':
        migrate_database()
    else:
        print("Migration cancelled.")
