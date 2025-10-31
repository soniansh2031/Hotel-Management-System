"""
Test script for Hotel Management System
This script verifies that all components of the application are working correctly.
"""

import os
import sys
import sqlite3

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Change to the project directory
dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)

def test_database_creation():
    """Test if database and tables are created correctly"""
    print("Testing database creation...")
    
    db_path = os.path.join('database', 'hotel.db')
    if not os.path.exists(db_path):
        print("❌ Database file not found")
        return False
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if all tables exist
        tables = ['users', 'rooms', 'customers', 'bookings']
        for table in tables:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                print(f"❌ Table '{table}' not found")
                return False
        
        print("✅ Database and all tables exist")
        return True
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
        return False
    finally:
        if conn:
            conn.close()

def test_default_admin():
    """Test if default admin user exists"""
    print("Testing default admin user...")
    
    conn = None
    try:
        conn = sqlite3.connect(os.path.join('database', 'hotel.db'))
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        admin = cursor.fetchone()
        
        if not admin:
            print("❌ Default admin user not found")
            return False
            
        # Check if password is hashed
        if len(admin[2]) < 20:  # Password hash should be long
            print("❌ Admin password not properly hashed")
            return False
            
        if admin[3] != 'admin':  # Role should be 'admin'
            print("❌ Admin user has incorrect role")
            return False
            
        print("✅ Default admin user exists with proper credentials")
        return True
    except Exception as e:
        print(f"❌ Error checking admin user: {e}")
        return False
    finally:
        if conn:
            conn.close()

def test_sample_rooms():
    """Test if sample rooms were added"""
    print("Testing sample rooms...")
    
    conn = None
    try:
        conn = sqlite3.connect(os.path.join('database', 'hotel.db'))
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM rooms")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("❌ No rooms found in database")
            return False
            
        print(f"✅ {count} rooms found in database")
        return True
    except Exception as e:
        print(f"❌ Error checking rooms: {e}")
        return False
    finally:
        if conn:
            conn.close()

def test_template_files():
    """Test if all required template files exist"""
    print("Testing template files...")
    
    required_templates = [
        'base.html',
        'index.html',
        'login.html',
        'register.html',
        'dashboard.html',
        'rooms.html',
        'booking.html',
        'bill.html',
        'customer.html'
    ]
    
    template_dir = 'templates'
    missing_files = []
    
    for template in required_templates:
        file_path = os.path.join(template_dir, template)
        if not os.path.exists(file_path):
            missing_files.append(template)
    
    if missing_files:
        print(f"❌ Missing template files: {missing_files}")
        return False
        
    print(f"✅ All {len(required_templates)} template files exist")
    return True

def test_static_files():
    """Test if required static files exist"""
    print("Testing static files...")
    
    required_files = [
        os.path.join('static', 'style.css')
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing static files: {missing_files}")
        return False
        
    print("✅ All required static files exist")
    return True

def test_requirements_file():
    """Test if requirements.txt exists and has required packages"""
    print("Testing requirements file...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt file not found")
        return False
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        required_packages = ['flask', 'werkzeug']
        missing_packages = []
        
        for package in required_packages:
            if package not in content.lower():
                missing_packages.append(package)
                
        if missing_packages:
            print(f"❌ Missing packages in requirements.txt: {missing_packages}")
            return False
            
        print("✅ requirements.txt file exists with required packages")
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def main():
    """Run all tests"""
    print("Hotel Management System - Test Suite")
    print("=" * 40)
    
    tests = [
        test_database_creation,
        test_default_admin,
        test_sample_rooms,
        test_template_files,
        test_static_files,
        test_requirements_file
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()
    
    print("=" * 40)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The application is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)