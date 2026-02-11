"""
Database models for Job Portal Application
"""
from datetime import datetime
from extensions import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User model with role-based authentication"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, employer, jobseeker
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('Profile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    jobs = db.relationship('Job', back_populates='employer', foreign_keys='Job.employer_id', cascade='all, delete-orphan')
    applications = db.relationship('Application', back_populates='jobseeker', foreign_keys='Application.jobseeker_id', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
    
    @property
    def password(self):
        """Prevent direct password access"""
        raise AttributeError('Password is not readable')
    
    @password.setter
    def password(self, password):
        """Hash password when setting"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """Verify password"""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_employer(self):
        """Check if user is employer"""
        return self.role == 'employer'
    
    def is_jobseeker(self):
        """Check if user is jobseeker"""
        return self.role == 'jobseeker'
    
    def get_role_display(self):
        """Get human-readable role"""
        roles = {
            'admin': 'Admin',
            'employer': 'Employer',
            'jobseeker': 'Jobseeker'
        }
        return roles.get(self.role, self.role)


class Profile(db.Model):
    """Profile model for additional user information"""
    
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False, index=True)
    resume_path = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    github = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)  # Comma-separated skills
    experience_years = db.Column(db.Integer, nullable=True)
    education = db.Column(db.Text, nullable=True)
    additional_details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', back_populates='profile')
    
    def __repr__(self):
        return f'<Profile for User {self.user_id}>'


class Job(db.Model):
    """Job posting model"""
    
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    company_description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.String(100), nullable=True)  # Can be range or specific amount
    salary_min = db.Column(db.Integer, nullable=True)
    salary_max = db.Column(db.Integer, nullable=True)
    job_type = db.Column(db.String(50), nullable=True)  # Full-time, Part-time, Contract, etc.
    experience_level = db.Column(db.String(50), nullable=True)  # Entry, Mid, Senior
    required_skills = db.Column(db.Text, nullable=True)  # Comma-separated
    benefits = db.Column(db.Text, nullable=True)
    how_to_apply = db.Column(db.Text, nullable=True)
    application_email = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(20), default='active')  # active, closed, draft
    views_count = db.Column(db.Integer, default=0)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    employer = db.relationship('User', back_populates='jobs', foreign_keys=[employer_id])
    applications = db.relationship('Application', back_populates='job', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Job {self.title} at {self.company_name}>'
    
    @hybrid_property
    def application_count(self):
        """Optimized application count using hybrid property - avoids loading full relationship"""
        return len(self.applications)
    
    @application_count.expression
    def application_count(cls):
        """SQL expression for application count (used in queries)"""
        return db.select([db.func.count(Application.id)]).where(Application.job_id == cls.id).scalar_subquery()
    
    def get_status_display(self):
        """Get human-readable status"""
        statuses = {
            'active': 'Active',
            'closed': 'Closed',
            'draft': 'Draft'
        }
        return statuses.get(self.status, self.status)
    
    def get_applications_count(self):
        """Get total applications count"""
        return len(self.applications)
    
    def get_applied_user_ids(self):
        """Get list of user IDs who applied"""
        return [app.jobseeker_id for app in self.applications]


class Application(db.Model):
    """Job application model"""
    
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    jobseeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, accepted, rejected
    cover_letter = db.Column(db.Text, nullable=True)
    additional_notes = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = db.relationship('Job', back_populates='applications')
    jobseeker = db.relationship('User', back_populates='applications', foreign_keys=[jobseeker_id])
    
    def __repr__(self):
        return f'<Application {self.id} for Job {self.job_id}>'
    
    def get_status_display(self):
        """Get human-readable status"""
        statuses = {
            'pending': 'Pending',
            'reviewed': 'Reviewed',
            'accepted': 'Accepted',
            'rejected': 'Rejected'
        }
        return statuses.get(self.status, self.status)

