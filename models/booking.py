from datetime import datetime

class Booking:
    def __init__(self, mysql):
        self.mysql = mysql
    
    def create_booking(self, user_id, service_name, booking_date, booking_time, customer_name, customer_email, customer_phone, notes=None):
        """Create a new booking"""
        try:
            cursor = self.mysql.connection.cursor()
            query = """
                INSERT INTO bookings (user_id, service_name, booking_date, booking_time, 
                                    customer_name, customer_email, customer_phone, notes, 
                                    status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, service_name, booking_date, booking_time,
                                 customer_name, customer_email, customer_phone, notes,
                                 'pending', datetime.now()))
            self.mysql.connection.commit()
            booking_id = cursor.lastrowid
            cursor.close()
            return booking_id
        except Exception as e:
            print(f"Error creating booking: {e}")
            return None
    
    def get_booking_by_id(self, booking_id):
        """Get booking by ID"""
        cursor = self.mysql.connection.cursor(dictionary=True)
        query = "SELECT * FROM bookings WHERE id = %s"
        cursor.execute(query, (booking_id,))
        booking = cursor.fetchone()
        cursor.close()
        return booking
    
    def get_user_bookings(self, user_id):
        """Get all bookings for a specific user"""
        cursor = self.mysql.connection.cursor(dictionary=True)
        query = """
            SELECT * FROM bookings 
            WHERE user_id = %s 
            ORDER BY booking_date DESC, booking_time DESC
        """
        cursor.execute(query, (user_id,))
        bookings = cursor.fetchall()
        cursor.close()
        return bookings
    
    def get_all_bookings(self):
        """Get all bookings"""
        cursor = self.mysql.connection.cursor(dictionary=True)
        query = "SELECT * FROM bookings ORDER BY booking_date DESC, booking_time DESC"
        cursor.execute(query)
        bookings = cursor.fetchall()
        cursor.close()
        return bookings
    
    def update_booking_status(self, booking_id, status):
        """Update booking status"""
        try:
            cursor = self.mysql.connection.cursor()
            query = "UPDATE bookings SET status = %s WHERE id = %s"
            cursor.execute(query, (status, booking_id))
            self.mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating booking status: {e}")
            return False
    
    def delete_booking(self, booking_id):
        """Delete a booking"""
        try:
            cursor = self.mysql.connection.cursor()
            query = "DELETE FROM bookings WHERE id = %s"
            cursor.execute(query, (booking_id,))
            self.mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error deleting booking: {e}")
            return False
