import mysql.connector
from flask import g
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        pass
    
    def connect(self):
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )
    
    @property
    def connection(self):
        if 'db' not in g:
            g.db = self.connect()
        return g.db

# Global database instance
db = Database()

def init_mysql(app):
    """Initialize MySQL with Flask app"""
    return db

def get_mysql():
    """Get the global database instance"""
    return db
