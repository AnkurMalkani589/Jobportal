"""
Job Portal Application
A full-stack job portal web application with role-based authentication
"""
import os
from flask import Flask, config, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_login import current_user
from config import Config
from extensions import db, login_manager, bcrypt, mail
from models import User

# Import blueprints
from auth.routes import auth
from main.routes import main
from admin.routes import admin
from employer.routes import employer
from jobseeker.routes import jobseeker


# Set up user loader
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


def create_app():
    """Create and configure the Flask application"""
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    # Create upload folder if it doesn't exist
    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(employer, url_prefix='/employer')
    app.register_blueprint(jobseeker, url_prefix='/jobseeker')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', error=e), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('404.html', error=e), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('404.html', error=e), 403
    
    return app


# Create application instance
app = create_app()


# Context processor for sidebar state
@app.context_processor
def inject_sidebar_state():
    """Inject sidebar collapsed state for all templates"""
    # Check if user is authenticated and has a sidebar
    # Use getattr with default False to handle anonymous users
    is_auth = getattr(current_user, 'is_authenticated', False)
    if is_auth:
        # Get sidebar collapsed state from localStorage (via session)
        sidebar_collapsed = request.cookies.get('sidebar_collapsed', 'false') == 'true'
    else:
        sidebar_collapsed = False
    return dict(sidebar_collapsed=sidebar_collapsed)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

