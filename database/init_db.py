import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_database():
    """Initialize the database with schema"""
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', '')
        )
        
        cursor = connection.cursor()
        
        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = f.read()
        
        # Execute each statement
        for statement in schema.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        print("✓ Database initialized successfully!")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"✗ Error: {err}")
        return False
    
    return True

if __name__ == '__main__':
    print("Initializing database...")
    initialize_database()
