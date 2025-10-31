import os
import sqlite3
from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database configuration
DATABASE = os.path.join('database', 'hotel.db')

def init_db():
    """Initialize the database with required tables"""
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
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def is_admin():
    """Check if current user is admin"""
    return 'user_role' in session and session['user_role'] == 'admin'

def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        if not username or not password:
            flash('Username and password are required!')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', (username, hashed_password, role))
            conn.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!')
            return redirect(url_for('register'))
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['user_role'] = user['role']
            flash('Login successful!')
            
            if user['role'] == 'admin':
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('book_room'))
        else:
            flash('Invalid username or password!')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in() or not is_admin():
        flash('Access denied!')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get statistics
    total_rooms = conn.execute('SELECT COUNT(*) as count FROM rooms').fetchone()['count']
    available_rooms = conn.execute('SELECT COUNT(*) as count FROM rooms WHERE status = "Available"').fetchone()['count']
    booked_rooms = conn.execute('SELECT COUNT(*) as count FROM rooms WHERE status = "Booked"').fetchone()['count']
    
    # Get total revenue
    total_revenue = conn.execute('SELECT SUM(total_amount) as sum FROM bookings').fetchone()['sum']
    if total_revenue is None:
        total_revenue = 0
    
    # Get all rooms
    rooms = conn.execute('SELECT * FROM rooms').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                          total_rooms=total_rooms,
                          available_rooms=available_rooms,
                          booked_rooms=booked_rooms,
                          total_revenue=total_revenue,
                          rooms=rooms)

@app.route('/rooms')
def rooms():
    if not is_logged_in() or not is_admin():
        flash('Access denied!')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    rooms = conn.execute('SELECT * FROM rooms').fetchall()
    conn.close()
    
    return render_template('rooms.html', rooms=rooms)

@app.route('/add_room', methods=['POST'])
def add_room():
    if not is_logged_in() or not is_admin():
        flash('Access denied!')
        return redirect(url_for('login'))
    
    room_number = request.form['room_number']
    room_type = request.form['room_type']
    price_per_night = request.form['price_per_night']
    
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO rooms (room_number, room_type, price_per_night, status)
            VALUES (?, ?, ?, ?)
        ''', (room_number, room_type, price_per_night, 'Available'))
        conn.commit()
        flash('Room added successfully!')
    except sqlite3.IntegrityError:
        flash('Room number already exists!')
    finally:
        conn.close()
    
    return redirect(url_for('rooms'))

@app.route('/edit_room/<int:room_id>', methods=['POST'])
def edit_room(room_id):
    if not is_logged_in() or not is_admin():
        flash('Access denied!')
        return redirect(url_for('login'))
    
    room_type = request.form['room_type']
    price_per_night = request.form['price_per_night']
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE rooms 
        SET room_type = ?, price_per_night = ?
        WHERE room_id = ?
    ''', (room_type, price_per_night, room_id))
    conn.commit()
    conn.close()
    
    flash('Room updated successfully!')
    return redirect(url_for('rooms'))

@app.route('/delete_room/<int:room_id>')
def delete_room(room_id):
    if not is_logged_in() or not is_admin():
        flash('Access denied!')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM rooms WHERE room_id = ?', (room_id,))
    conn.commit()
    conn.close()
    
    flash('Room deleted successfully!')
    return redirect(url_for('rooms'))

@app.route('/book-room')
def book_room():
    if not is_logged_in():
        flash('Please log in to book a room!')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    available_rooms = conn.execute('''
        SELECT * FROM rooms 
        WHERE status = "Available"
    ''').fetchall()
    conn.close()
    
    return render_template('booking.html', rooms=available_rooms)

@app.route('/process-booking', methods=['POST'])
def process_booking():
    if not is_logged_in():
        flash('Please log in to book a room!')
        return redirect(url_for('login'))
    
    room_id = request.form['room_id']
    check_in = request.form['check_in']
    check_out = request.form['check_out']
    
    # Validate dates
    try:
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        
        if check_out_date <= check_in_date:
            flash('Check-out date must be after check-in date!')
            return redirect(url_for('book_room'))
    except ValueError:
        flash('Invalid date format!')
        return redirect(url_for('book_room'))
    
    conn = get_db_connection()
    
    # Check if room is already booked for these dates
    existing_booking = conn.execute('''
        SELECT * FROM bookings 
        WHERE room_id = ? AND (
            (check_in <= ? AND check_out >= ?) OR
            (check_in <= ? AND check_out >= ?) OR
            (check_in >= ? AND check_out <= ?)
        )
    ''', (room_id, check_in, check_in, check_out, check_out, check_in, check_out)).fetchone()
    
    if existing_booking:
        flash('This room is already booked for the selected dates!')
        conn.close()
        return redirect(url_for('book_room'))
    
    # Get room details
    room = conn.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id,)).fetchone()
    
    # Calculate total amount
    days = (check_out_date - check_in_date).days
    total_amount = days * room['price_per_night']
    
    # Insert booking
    conn.execute('''
        INSERT INTO bookings (user_id, room_id, check_in, check_out, total_amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (session['user_id'], room_id, check_in, check_out, total_amount))
    
    # Update room status
    conn.execute('UPDATE rooms SET status = "Booked" WHERE room_id = ?', (room_id,))
    
    conn.commit()
    
    # Get booking details for receipt
    booking = conn.execute('''
        SELECT b.*, r.room_number, r.room_type, u.username
        FROM bookings b
        JOIN rooms r ON b.room_id = r.room_id
        JOIN users u ON b.user_id = u.user_id
        WHERE b.booking_id = last_insert_rowid()
    ''').fetchone()
    
    conn.close()
    
    flash('Room booked successfully!')
    return render_template('bill.html', booking=booking, days=days)

@app.route('/customer-details', methods=['GET', 'POST'])
def customer_details():
    if not is_logged_in():
        flash('Please log in to view customer details!')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO customers (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            ''', (name, email, phone, address))
            conn.commit()
            flash('Customer details saved successfully!')
        except:
            flash('Error saving customer details!')
        finally:
            conn.close()
    
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    
    return render_template('customer.html', customers=customers)

if __name__ == '__main__':
    app.run(debug=True)