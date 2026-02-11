"""
Admin User Creation Script
Run this to create an admin account for the Job Portal
"""
from app import create_app
from extensions import db
from models import User

def create_admin():
    """Create an admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@jobportal.com').first()
        if admin:
            print(f'Admin user already exists: {admin.email}')
            return
        
        # Create admin user
        admin = User(
            name='Admin',
            email='admin@jobportal.com',
            password='admin123',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print(f'Admin user created successfully!')
        print(f'Email: admin@jobportal.com')
        print(f'Password: admin123')


if __name__ == '__main__':
    create_admin()

