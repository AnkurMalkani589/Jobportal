#!/usr/bin/env python
"""Test script to verify Job Portal application works correctly"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, '/home/ankurmalkani/job_portal')

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from config import Config
        print("  ✓ config.py imported")
    except Exception as e:
        print(f"  ✗ config.py failed: {e}")
        return False
    
    try:
        from extensions import db, login_manager, bcrypt, mail
        print("  ✓ extensions.py imported")
    except Exception as e:
        print(f"  ✗ extensions.py failed: {e}")
        return False
    
    try:
        from models import User, Job, Application, Profile
        print("  ✓ models.py imported")
    except Exception as e:
        print(f"  ✗ models.py failed: {e}")
        return False
    
    try:
        from auth.routes import auth
        from auth.forms import LoginForm, RegistrationForm
        print("  ✓ auth module imported")
    except Exception as e:
        print(f"  ✗ auth module failed: {e}")
        return False
    
    try:
        from main.routes import main
        print("  ✓ main module imported")
    except Exception as e:
        print(f"  ✗ main module failed: {e}")
        return False
    
    try:
        from admin.routes import admin
        print("  ✓ admin module imported")
    except Exception as e:
        print(f"  ✗ admin module failed: {e}")
        return False
    
    try:
        from employer.routes import employer
        print("  ✓ employer module imported")
    except Exception as e:
        print(f"  ✗ employer module failed: {e}")
        return False
    
    try:
        from jobseeker.routes import jobseeker
        print("  ✓ jobseeker module imported")
    except Exception as e:
        print(f"  ✗ jobseeker module failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Test that the Flask app can be created"""
    print("\nTesting app creation...")
    
    try:
        from app import create_app
        app = create_app()
        print("  ✓ Flask app created successfully")
        
        # Test that blueprints are registered
        blueprints = [bp.name for bp in app.blueprints.values()]
        print(f"  ✓ Registered blueprints: {', '.join(blueprints)}")
        
        return True
    except Exception as e:
        print(f"  ✗ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 50)
    print("Job Portal Application Test")
    print("=" * 50)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_app_creation():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("All tests passed! ✓")
    else:
        print("Some tests failed! ✗")
    print("=" * 50)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())

