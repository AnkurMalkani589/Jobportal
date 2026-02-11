"""
Fix Admin User Script
Run this on your LIVE server to recreate the admin user with correct password hash.

Upload this file to your live server and run:
    python fix_admin.py
"""
from app import create_app
from extensions import db, bcrypt
from models import User

def fix_admin():
    """Fix the admin user by recreating with proper password hash"""
    app = create_app()
    
    with app.app_context():
        # Delete existing admin if any
        admin = User.query.filter_by(email='admin@jobportal.com').first()
        if admin:
            print(f'Deleting existing admin user: {admin.email}')
            db.session.delete(admin)
            db.session.commit()
        
        # Create new admin user with proper password hashing
        admin = User(
            name='Admin',
            email='admin@jobportal.com',
            role='admin'
        )
        # Set password using the model's setter which handles bcrypt hashing
        admin.password = 'admin123'
        
        db.session.add(admin)
        db.session.commit()
        
        print('Admin user created successfully!')
        print(f'Email: admin@jobportal.com')
        print(f'Password: admin123')
        print(f'Role: admin')
        print(f'Password Hash: {admin.password_hash}')
        
        # Verify the password works
        if admin.verify_password('admin123'):
            print('✓ Password verification: SUCCESS')
        else:
            print('✗ Password verification: FAILED')
        
        print('\nTry logging in now at your live application!')


if __name__ == '__main__':
    fix_admin()

