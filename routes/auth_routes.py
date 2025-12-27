from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from models.user import User
from utils.db import get_mysql

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """Render registration page"""
    if 'user_id' in session:
        return redirect(url_for('booking.my_bookings_page'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """Render login page"""
    if 'user_id' in session:
        return redirect(url_for('booking.my_bookings_page'))
    return render_template('login.html')

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """API endpoint for user registration"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not all([username, email, password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    mysql = get_mysql()
    user_model = User(mysql)
    
    if user_model.email_exists(email):
        return jsonify({'error': 'Email already registered'}), 409
    
    user_id = user_model.create_user(username, email, password)
    
    if user_id:
        session['user_id'] = user_id
        session['username'] = username
        session['email'] = email
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        }), 201
    else:
        return jsonify({'error': 'Failed to register user'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """API endpoint for user login"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not all([email, password]):
        return jsonify({'error': 'Email and password are required'}), 400
    
    mysql = get_mysql()
    user_model = User(mysql)
    
    user = user_model.verify_password(email, password)
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['email'] = user['email']
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """API endpoint for user logout"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/api/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({
        'user': {
            'id': session['user_id'],
            'username': session['username'],
            'email': session['email']
        }
    }), 200
