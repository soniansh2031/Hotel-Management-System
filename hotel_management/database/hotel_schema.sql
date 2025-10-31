-- Hotel Management System Database Schema

-- Drop tables if they exist (for fresh setup)
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

-- Create rooms table
CREATE TABLE rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number TEXT UNIQUE NOT NULL,
    room_type TEXT NOT NULL,
    price_per_night REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'Available'
);

-- Create customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL
);

-- Create bookings table
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (room_id) REFERENCES rooms (room_id)
);

-- Insert default admin user
INSERT INTO users (username, password, role) 
VALUES ('admin', 'pbkdf2:sha256:260000$xyz123$abcdef456789hashvalue', 'admin');

-- Insert sample rooms
INSERT INTO rooms (room_number, room_type, price_per_night, status) VALUES
('101', 'Single', 100.00, 'Available'),
('102', 'Single', 100.00, 'Available'),
('201', 'Double', 150.00, 'Available'),
('202', 'Double', 150.00, 'Available'),
('301', 'Suite', 250.00, 'Available');

-- Sample customer data
INSERT INTO customers (name, email, phone, address) VALUES
('John Doe', 'john.doe@email.com', '123-456-7890', '123 Main St, City, State'),
('Jane Smith', 'jane.smith@email.com', '098-765-4321', '456 Oak Ave, Town, State');

-- Sample booking data
INSERT INTO bookings (user_id, room_id, check_in, check_out, total_amount) VALUES
(2, 1, '2025-11-01', '2025-11-05', 400.00),
(2, 3, '2025-11-10', '2025-11-12', 300.00);

-- Indexes for better performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_rooms_status ON rooms(status);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_room_id ON bookings(room_id);
CREATE INDEX idx_bookings_dates ON bookings(check_in, check_out);