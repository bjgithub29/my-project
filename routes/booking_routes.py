from flask import Blueprint, request, jsonify, render_template, session
from models.booking import Booking
from utils.db import get_mysql
from middleware.auth_middleware import login_required
from datetime import datetime

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/', methods=['GET'])
@login_required
def booking_page():
    """Render booking page"""
    return render_template('booking.html')

@booking_bp.route('/my-bookings', methods=['GET'])
@login_required
def my_bookings_page():
    """Render user's bookings page"""
    return render_template('my_bookings.html')

@booking_bp.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    """API endpoint to create a new booking"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    service_name = data.get('service_name')
    booking_date = data.get('booking_date')
    booking_time = data.get('booking_time')
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    customer_phone = data.get('customer_phone')
    notes = data.get('notes', '')
    
    if not all([service_name, booking_date, booking_time, customer_name, customer_email, customer_phone]):
        return jsonify({'error': 'All required fields must be filled'}), 400
    
    # Validate date format
    try:
        datetime.strptime(booking_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    mysql = get_mysql()
    booking_model = Booking(mysql)
    
    booking_id = booking_model.create_booking(
        user_id=session['user_id'],
        service_name=service_name,
        booking_date=booking_date,
        booking_time=booking_time,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        notes=notes
    )
    
    if booking_id:
        return jsonify({
            'message': 'Booking created successfully',
            'booking_id': booking_id
        }), 201
    else:
        return jsonify({'error': 'Failed to create booking'}), 500

@booking_bp.route('/api/bookings', methods=['GET'])
@login_required
def get_user_bookings():
    """API endpoint to get all bookings for the logged-in user"""
    mysql = get_mysql()
    booking_model = Booking(mysql)
    
    bookings = booking_model.get_user_bookings(session['user_id'])
    
    # Convert datetime objects to strings for JSON serialization
    for booking in bookings:
        if booking.get('booking_date'):
            booking['booking_date'] = str(booking['booking_date'])
        if booking.get('created_at'):
            booking['created_at'] = str(booking['created_at'])
    
    return jsonify({'bookings': bookings}), 200

@booking_bp.route('/api/bookings/<int:booking_id>', methods=['GET'])
@login_required
def get_booking(booking_id):
    """API endpoint to get a specific booking"""
    mysql = get_mysql()
    booking_model = Booking(mysql)
    
    booking = booking_model.get_booking_by_id(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    # Verify that the booking belongs to the current user
    if booking['user_id'] != session['user_id']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Convert datetime objects to strings
    if booking.get('booking_date'):
        booking['booking_date'] = str(booking['booking_date'])
    if booking.get('created_at'):
        booking['created_at'] = str(booking['created_at'])
    
    return jsonify({'booking': booking}), 200

@booking_bp.route('/api/bookings/<int:booking_id>/status', methods=['PATCH'])
@login_required
def update_booking_status(booking_id):
    """API endpoint to update booking status"""
    data = request.get_json()
    
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    status = data.get('status')
    valid_statuses = ['pending', 'confirmed', 'cancelled', 'completed']
    
    if status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
    
    mysql = get_mysql()
    booking_model = Booking(mysql)
    
    # Verify booking exists and belongs to user
    booking = booking_model.get_booking_by_id(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking['user_id'] != session['user_id']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    success = booking_model.update_booking_status(booking_id, status)
    
    if success:
        return jsonify({'message': 'Booking status updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update booking status'}), 500

@booking_bp.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def delete_booking(booking_id):
    """API endpoint to delete a booking"""
    mysql = get_mysql()
    booking_model = Booking(mysql)
    
    # Verify booking exists and belongs to user
    booking = booking_model.get_booking_by_id(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    if booking['user_id'] != session['user_id']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    success = booking_model.delete_booking(booking_id)
    
    if success:
        return jsonify({'message': 'Booking deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete booking'}), 500
