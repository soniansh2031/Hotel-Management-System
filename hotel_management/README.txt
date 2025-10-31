Hotel Management System
=======================

A Flask-based web application for managing hotel rooms, bookings, and customer information.

Features:
- User authentication (Admin and Customer roles)
- Room management (Add, Edit, Delete rooms)
- Booking system with date validation
- Automatic billing and receipt generation
- Admin dashboard with statistics

Tech Stack:
- Backend: Python + Flask
- Database: SQLite
- Frontend: HTML + CSS (No Bootstrap or external frameworks)

Setup Instructions:
-------------------

1. Install Python (version 3.6 or higher) if not already installed

2. Install required packages:
   - Double-click install_deps.bat
   OR
   - Run: pip install -r requirements.txt

3. Navigate to the project directory:
   cd hotel_management

4. (Optional) Initialize the database with sample data:
   - Run: python init_db.py

5. Run the application:
   - Double-click run_app.bat
   OR
   - Run: python app.py

5. Open your web browser and go to:
   http://localhost:5000

Default Admin Account:
- Username: admin
- Password: admin123

Project Structure:
------------------
/hotel_management/
    app.py              # Main Flask application
    init_db.py          # Database initialization script
    requirements.txt    # Python dependencies
    run_app.bat         # Windows batch file to run the application
    install_deps.bat    # Windows batch file to install dependencies
    test_app.py         # Test script to verify application components
    /templates/         # HTML templates
        base.html       # Base template
        index.html      # Homepage
        login.html      # Login page
        register.html   # Registration page
        dashboard.html  # Admin dashboard
        rooms.html      # Room management
        booking.html    # Booking form
        bill.html       # Receipt page
        customer.html   # Customer management
    /static/
        style.css       # CSS stylesheet
    /database/
        hotel.db        # SQLite database (created automatically)
        hotel_schema.sql # SQL schema file for manual database creation

How to Use:
-----------

1. Login as Admin:
   - Use the default admin credentials
   - Manage rooms, view statistics, and see all bookings

2. Register as Customer:
   - Create a new customer account
   - Browse available rooms and make bookings

3. Booking a Room:
   - Select an available room
   - Choose check-in and check-out dates
   - Confirm booking to generate receipt

Database Schema:
----------------
1. users: user_id, username, password, role
2. rooms: room_id, room_number, room_type, price_per_night, status
3. customers: customer_id, name, email, phone, address
4. bookings: booking_id, user_id, room_id, check_in, check_out, total_amount

Troubleshooting:
----------------
- If you encounter any issues, ensure all required packages are installed
- The database is created automatically on first run
- For reset, delete the database/hotel.db file and restart the application