"""
Authentication routes for Job Portal
Handles login, registration, and logout functionality
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from extensions import db
from models import User, Profile
from extensions import role_required

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect_after_login()
    
    from auth.forms import LoginForm
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.verify_password(password):
            login_user(user, remember=bool(remember))
            flash('Welcome back, {}!'.format(user.name), 'success')
            return redirect_after_login()
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect_after_login()
    
    from auth.forms import RegistrationForm
    form = RegistrationForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html', form=form)
        
        if role not in ['employer', 'jobseeker']:
            flash('Invalid role selected.', 'danger')
            return render_template('register.html', form=form)
        
        # Create user
        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        
        # Create empty profile
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))


def redirect_after_login():
    """Redirect user to their role-specific dashboard after login"""
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_employer():
        return redirect(url_for('employer.dashboard'))
    elif current_user.is_jobseeker():
        return redirect(url_for('jobseeker.dashboard'))
    else:
        return redirect(url_for('main.home'))

