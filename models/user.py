from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, mysql):
        self.mysql = mysql
    
    def create_user(self, username, email, password, role='user'):
        """Create a new user"""
        try:
            cursor = self.mysql.connection.cursor()
            hashed_password = generate_password_hash(password)
            query = """
                INSERT INTO users (username, email, password, role, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, email, hashed_password, role, datetime.now()))
            self.mysql.connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return user_id
        except Exception as e:
            return None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        cursor = self.mysql.connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        cursor = self.mysql.connection.cursor(dictionary=True)
        query = "SELECT id, username, email, role, created_at FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user
    
    def verify_password(self, email, password):
        """Verify user password"""
        user = self.get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    def email_exists(self, email):
        """Check if email already exists"""
        user = self.get_user_by_email(email)
        return user is not None
