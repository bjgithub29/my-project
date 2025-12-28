from flask import Flask, render_template, redirect, url_for, session
from config.config import Config
from utils.db import init_mysql
from routes.auth_routes import auth_bp
from routes.booking_routes import booking_bp
from routes.admin_routes import admin_bp
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MySQL
mysql = init_mysql(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    """Home page"""
    if 'user_id' not in session:
        return render_template('index.html')
    return redirect(url_for('booking.my_bookings_page'))

@app.route('/dashboard')
def dashboard():
    """Dashboard page - requires login"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    return redirect(url_for('booking.my_bookings_page'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
