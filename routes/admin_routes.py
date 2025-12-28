from flask import Blueprint, render_template, jsonify, request, session
from middleware.auth_middleware import admin_required
from utils.db import get_mysql

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard page"""
    return render_template('admin_dashboard.html')

@admin_bp.route('/api/dashboard-stats')
@admin_required
def dashboard_stats():
    """API endpoint to get dashboard statistics"""
    try:
        mysql = get_mysql()
        cursor = mysql.connection.cursor(dictionary=True)
        
        # Get total users count
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()['count']
        
        # Get total bookings count
        cursor.execute("SELECT COUNT(*) as count FROM bookings")
        total_bookings = cursor.fetchone()['count']
        
        # Get pending bookings count
        cursor.execute("SELECT COUNT(*) as count FROM bookings WHERE status = 'pending'")
        pending_bookings = cursor.fetchone()['count']
        
        # Get recent bookings (last 10)
        cursor.execute("""
            SELECT b.*, u.username 
            FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            ORDER BY b.created_at DESC
            LIMIT 10
        """)
        recent_bookings = cursor.fetchall()
        
        # Get all users
        cursor.execute("""
            SELECT id, username, email, role, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        all_users = cursor.fetchall()
        
        cursor.close()
        
        return jsonify({
            'totalUsers': total_users,
            'totalBookings': total_bookings,
            'pendingBookings': pending_bookings,
            'recentBookings': recent_bookings,
            'allUsers': all_users
        }), 200
        
    except Exception as e:
        print(f"Error fetching dashboard stats: {e}")
        return jsonify({'error': 'Failed to fetch dashboard statistics'}), 500

@admin_bp.route('/api/bookings/<int:booking_id>/status', methods=['PUT'])
@admin_required
def update_booking_status(booking_id):
    """API endpoint to update booking status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        if new_status not in ['pending', 'confirmed', 'cancelled', 'completed']:
            return jsonify({'error': 'Invalid status'}), 400
        
        mysql = get_mysql()
        cursor = mysql.connection.cursor()
        
        query = "UPDATE bookings SET status = %s WHERE id = %s"
        cursor.execute(query, (new_status, booking_id))
        mysql.connection.commit()
        
        if cursor.rowcount > 0:
            cursor.close()
            return jsonify({'message': 'Booking status updated successfully'}), 200
        else:
            cursor.close()
            return jsonify({'error': 'Booking not found'}), 404
            
    except Exception as e:
        print(f"Error updating booking status: {e}")
        return jsonify({'error': 'Failed to update booking status'}), 500

@admin_bp.route('/api/users')
@admin_required
def get_all_users():
    """API endpoint to get all users"""
    try:
        mysql = get_mysql()
        cursor = mysql.connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT id, username, email, role, created_at
            FROM users
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()
        cursor.close()
        
        return jsonify({'users': users}), 200
        
    except Exception as e:
        print(f"Error fetching users: {e}")
        return jsonify({'error': 'Failed to fetch users'}), 500

@admin_bp.route('/api/bookings')
@admin_required
def get_all_bookings():
    """API endpoint to get all bookings"""
    try:
        mysql = get_mysql()
        cursor = mysql.connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT b.*, u.username 
            FROM bookings b
            LEFT JOIN users u ON b.user_id = u.id
            ORDER BY b.created_at DESC
        """)
        bookings = cursor.fetchall()
        cursor.close()
        
        return jsonify({'bookings': bookings}), 200
        
    except Exception as e:
        print(f"Error fetching bookings: {e}")
        return jsonify({'error': 'Failed to fetch bookings'}), 500
