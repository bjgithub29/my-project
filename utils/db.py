import os
import mysql.connector
from flask import g
from dotenv import load_dotenv

load_dotenv()

class MySQL:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
        app.teardown_appcontext(self.teardown)
    
    def connect(self):
        return mysql.connector.connect(
            host=self.app.config['MYSQL_HOST'],
            user=self.app.config['MYSQL_USER'],
            password=self.app.config['MYSQL_PASSWORD'],
            database=self.app.config['MYSQL_DATABASE']
        )
    
    @property
    def connection(self):
        if 'db' not in g:
            g.db = self.connect()
        return g.db
    
    def teardown(self, exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

mysql = None

def init_mysql(app):
    """Initialize MySQL connection"""
    global mysql
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DB', 'booking_db')
    mysql = MySQL(app)
    return mysql

def get_mysql():
    """Get the global MySQL instance"""
    return mysql
