"""
Flask extensions initialization
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from functools import wraps
from flask import current_app, request, flash, redirect, url_for

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def role_required(roles):
    """
    Decorator to require specific roles for a route.
    Moved to extensions.py for consistent reuse across all blueprints.
    
    Usage:
        @role_required(['admin'])
        def admin_route():
            ...
    
    Args:
        roles: List of role names that are allowed to access the route
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask_login import current_user
            
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                if current_user.is_admin():
                    return redirect(url_for('admin.dashboard'))
                elif current_user.is_employer():
                    return redirect(url_for('employer.dashboard'))
                elif current_user.is_jobseeker():
                    return redirect(url_for('jobseeker.dashboard'))
                else:
                    return redirect(url_for('main.home'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

