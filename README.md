# Job Portal Web Application

A full-stack, mobile-responsive Job Portal Web Application built with Python Flask, SQLite, HTML, and Bootstrap. This application follows clean architecture principles and implements role-based authentication for three distinct user roles: Admin, Employer, and Jobseeker.

## 🌟 Features

### User Roles & Authentication
- **Admin**: Full system access, analytics dashboard, user management
- **Employer**: Job posting, application management, profile management
- **Jobseeker**: Browse jobs, apply to jobs, profile management

### Core Features
- 🔐 Secure authentication with password hashing
- 📱 Fully responsive design (Bootstrap 5)
- 👥 Role-based access control (RBAC)
- 📊 Admin dashboard with analytics
- 💼 Job posting and management
- 📝 Job application system
- 👤 Profile management for jobseekers
- 🔍 Advanced job search and filtering

### Technical Features
- Modular Flask Blueprint architecture
- SQLAlchemy ORM for database operations
- Session-based authentication with Flask-Login
- CSRF protection with Flask-WTF
- Password hashing with Flask-Bcrypt

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd job_portal
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ...     exit()
   ```

5. **Create an admin user**
   ```python
   python
   >>> from app import create_app, db
   >>> from models import User
   >>> app = create_app()
   >>> with app.app_context():
   ...     admin = User(name='Admin', email='admin@jobportal.com', password='admin123', role='admin')
   ...     db.session.add(admin)
   ...     db.session.commit()
   ...     exit()
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
job_portal/
│
├── app.py                    # Main application entry point
├── config.py                 # Configuration settings
├── extensions.py             # Flask extensions initialization
├── models.py                 # Database models
├── requirements.txt          # Python dependencies
│
├── auth/                     # Authentication blueprint
│   ├── __init__.py
│   └── routes.py
│
├── admin/                    # Admin blueprint
│   ├── __init__.py
│   └── routes.py
│
├── employer/                 # Employer blueprint
│   ├── __init__.py
│   └── routes.py
│
├── jobseeker/                # Jobseeker blueprint
│   ├── __init__.py
│   └── routes.py
│
├── main/                     # Main routes blueprint
│   ├── __init__.py
│   └── routes.py
│
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── home.html            # Home page
│   ├── jobs.html            # Job listings (public)
│   ├── job_detail.html      # Job details (public)
│   ├── 404.html             # Error page
│   ├── admin/               # Admin templates
│   ├── employer/           # Employer templates
│   └── jobseeker/          # Jobseeker templates
│
└── static/                   # Static files
    ├── css/
    │   └── main.css         # Custom styles
    ├── js/
    │   └── main.js          # Custom JavaScript
    └── images/              # Image assets
```

## 👥 User Roles & Permissions

### Admin
- **Access**: `/admin/dashboard`
- **Features**:
  - View system analytics (total jobs, employers, jobseekers)
  - Filter statistics by daily, weekly, monthly, yearly
  - View all employers and jobseekers
  - Manage (view/delete) all job postings
  - Delete users

### Employer
- **Access**: `/employer/dashboard`
- **Features**:
  - Create, edit, delete job postings
  - View applications to their jobs
  - Review and update application status
  - Manage company profile

### Jobseeker
- **Access**: `/jobseeker/dashboard`
- **Features**:
  - Browse and search available jobs
  - View job details
  - Apply to jobs
  - Manage profile (resume, skills, experience)
  - View application history

## 🔑 Sample Credentials

After running the setup, you can use these sample credentials:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@jobportal.com | admin123 |
| Employer | employer@demo.com | demo123 |
| Jobseeker | jobseeker@demo.com | demo123 |

**Note**: The employer and jobseeker accounts need to be created through the registration page.

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.23
- **Authentication**: Flask-Login 0.6.3
- **Forms**: Flask-WTF 1.2.1
- **Security**: Flask-Bcrypt 1.0.1

### Frontend
- **HTML5**: Semantic markup
- **Bootstrap 5**: Responsive CSS framework
- **CSS**: Custom styles with Bootstrap compatibility
- **JavaScript**: Vanilla JS for interactivity
- **Icons**: Bootstrap Icons

### Database
- **SQLite**: Lightweight, file-based database

## 📝 Database Schema

### Users Table
- `id`: Primary Key
- `name`: Full name
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: 'admin', 'employer', or 'jobseeker'
- `created_at`: Account creation timestamp

### Jobs Table
- `id`: Primary Key
- `title`: Job title
- `description`: Full job description
- `company_name`: Company name
- `location`: Job location
- `salary`: Salary range
- `employer_id`: Foreign Key to User
- `status`: 'active', 'closed', or 'draft'
- `created_at`: Job posting timestamp

### Applications Table
- `id`: Primary Key
- `job_id`: Foreign Key to Job
- `jobseeker_id`: Foreign Key to User
- `status`: 'pending', 'reviewed', 'accepted', or 'rejected'
- `cover_letter`: Optional cover letter
- `applied_at`: Application timestamp

### Profiles Table
- `id`: Primary Key
- `user_id`: Foreign Key to User (one-to-one)
- `resume_path`: Path to resume file
- `phone`: Contact phone
- `address`: Physical address
- `bio`: Professional summary
- `skills`: Comma-separated skills
- `experience_years`: Years of experience

## 🎨 UI Features

### Responsive Design
- Mobile-first approach
- Collapsible sidebar navigation
- Fluid Bootstrap grid system
- Touch-friendly interface

### Dashboard Analytics
- Summary statistics cards
- Visual charts and metrics
- Time-based filtering
- Recent activity feeds

### Job Search
- Keyword search
- Location filtering
- Job type filtering
- Experience level filtering
- Pagination support

## 🔒 Security Features

- **Password Hashing**: Using Flask-Bcrypt (bcrypt)
- **Session Management**: Secure session handling
- **CSRF Protection**: Flask-WTF form tokens
- **Input Validation**: Server-side validation
- **Role-Based Access**: Decorator-based authorization
- **SQL Injection Prevention**: SQLAlchemy ORM

## 🚀 Deployment

### Production Settings
1. Set environment variables:
   ```bash
   export SECRET_KEY='your-secure-secret-key'
   export FLASK_ENV=production
   ```

2. Use a production database (PostgreSQL, MySQL):
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/job_portal'
   ```

3. Run with a WSGI server:
   ```bash
   gunicorn app:app -w 4
   ```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For questions or support, please open an issue in the repository.

---

**Happy Job Hunting! 🎉**

