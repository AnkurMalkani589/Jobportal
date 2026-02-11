import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string-keep-it-secret'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'job_portal.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BCRYPT_LOG_ROUNDS = 12

    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@jobportal.com'

    ROLES = {
        'admin': 'Admin',
        'employer': 'Employer',
        'jobseeker': 'Jobseeker'
    }

    JOB_STATUS = {
        'active': 'Active',
        'closed': 'Closed',
        'draft': 'Draft'
    }

    APPLICATION_STATUS = {
        'pending': 'Pending',
        'reviewed': 'Reviewed',
        'accepted': 'Accepted',
        'rejected': 'Rejected'
    }
