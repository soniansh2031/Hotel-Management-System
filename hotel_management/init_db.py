import os
import sqlite3
from werkzeug.security import generate_password_hash

# Database configuration
DATABASE = os.path.join('database', 'hotel.db')

def init_db():
    """Initialize the database with required tables"""
    # Create database directory if it doesn't exist
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # Create rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            price_per_night REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Available'
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in DATE NOT NULL,
            check_out DATE NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (room_id) REFERENCES rooms (room_id)
        )
    ''')
    
    # Insert default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_password = generate_password_hash('admin123', method='pbkdf2:sha256')
        cursor.execute('''
            INSERT INTO users (username, password, role) 
            VALUES (?, ?, ?)
        ''', ('admin', hashed_password, 'admin'))
        print("Default admin user created (username: admin, password: admin123)")
    else:
        print("Admin user already exists")
    
    # Insert some sample rooms if none exist
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        sample_rooms = [
            ('101', 'Single', 100.00),
            ('102', 'Single', 100.00),
            ('201', 'Double', 150.00),
            ('202', 'Double', 150.00),
            ('301', 'Suite', 250.00)
        ]
        
        for room_number, room_type, price in sample_rooms:
            cursor.execute('''
                INSERT INTO rooms (room_number, room_type, price_per_night, status)
                VALUES (?, ?, ?, ?)
            ''', (room_number, room_type, price, 'Available'))
        
        print("Sample rooms added")
    else:
        print("Rooms already exist in database")
    
    conn.commit()
    conn.close()
    print("Database initialization complete")

if __name__ == '__main__':
    init_db()