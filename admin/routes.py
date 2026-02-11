"""
Admin routes for Job Portal
Handles admin dashboard and user management
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import User, Job, Application, Profile
from extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
def dashboard():
    """Admin dashboard with statistics"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))

    period = request.args.get('period', 'monthly')

    now = datetime.utcnow()

    if period == 'daily':
        start_date = now - timedelta(days=1)
    elif period == 'weekly':
        start_date = now - timedelta(weeks=1)
    elif period == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = now - timedelta(days=365)

    # -------- TOTAL COUNTS --------
    total_jobs = Job.query.count()
    total_employers = User.query.filter_by(role='employer').count()
    total_jobseekers = User.query.filter_by(role='jobseeker').count()
    total_applications = Application.query.count()

    total_users = User.query.count()

    # -------- NEW RECORDS IN PERIOD --------
    new_employers = User.query.filter(
        User.role == 'employer',
        User.created_at >= start_date
    ).count()

    new_jobseekers = User.query.filter(
        User.role == 'jobseeker',
        User.created_at >= start_date
    ).count()

    new_jobs = Job.query.filter(
        Job.created_at >= start_date
    ).count()

    new_applications = Application.query.filter(
        Application.applied_at >= start_date
    ).count()

    # -------- JOB STATUS --------
    active_jobs = Job.query.filter_by(status='active').count()
    closed_jobs = Job.query.filter_by(status='closed').count()
    draft_jobs = Job.query.filter_by(status='draft').count()

    # -------- PENDING APPLICATIONS --------
    pending_apps = Application.query.filter_by(status='pending').count()

    # -------- RECENT USERS --------
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    # -------- RECENT JOBS --------
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',

        total_users=total_users,
        total_jobs=total_jobs,
        total_employers=total_employers,
        total_jobseekers=total_jobseekers,
        total_applications=total_applications,

        new_employers=new_employers,
        new_jobseekers=new_jobseekers,
        new_jobs=new_jobs,
        new_applications=new_applications,

        active_jobs=active_jobs,
        closed_jobs=closed_jobs,
        draft_jobs=draft_jobs,
        pending_apps=pending_apps,

        recent_users=recent_users,
        recent_jobs=recent_jobs,

        period=period
    )


@admin.route('/employers')
@login_required
def employers():
    """Manage all employers"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query.filter_by(role='employer')
    
    if search:
        query = query.filter(
            (User.name.contains(search)) |
            (User.email.contains(search))
        )
    
    employers_pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/employers.html', employers=employers_pagination)


@admin.route('/jobseekers')
@login_required
def jobseekers():
    """Manage all jobseekers"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = User.query.filter_by(role='jobseeker')
    
    if search:
        query = query.filter(
            (User.name.contains(search)) |
            (User.email.contains(search))
        )
    
    jobseekers_pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/jobseekers.html', jobseekers=jobseekers_pagination)


@admin.route('/jobs')
@login_required
def jobs():
    """Manage all job postings with optimized queries"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    # Build optimized query with application count subquery
    from sqlalchemy import func
    
    # Base query with join to get application counts
    query = db.session.query(
        Job,
        func.count(Application.id).label('application_count')
    ).outerjoin(
        Application, Application.job_id == Job.id
    ).group_by(Job.id)
    
    # Apply filters
    if status:
        query = query.filter(Job.status == status)
    
    if search:
        query = query.filter(
            (Job.title.contains(search)) | 
            (Job.company_name.contains(search))
        )
    
    # Order and paginate
    pagination = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Pass both jobs and the counts to template
    return render_template('admin/jobs.html', 
                         jobs=pagination,
                         job_counts={job.id: count for job, count in pagination.items})


@admin.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.employers'))
    
    # Delete user's jobs and applications
    for job in user.jobs:
        for app in job.applications:
            db.session.delete(app)
        db.session.delete(job)
    
    for app in user.applications:
        db.session.delete(app)
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully.', 'success')
    
    if user.role == 'employer':
        return redirect(url_for('admin.employers'))
    else:
        return redirect(url_for('admin.jobseekers'))


@admin.route('/job/<int:job_id>/close', methods=['POST'])
@login_required
def close_job(job_id):
    """Close a job posting"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    job = Job.query.get_or_404(job_id)
    job.status = 'closed'
    db.session.commit()
    
    flash('Job closed successfully.', 'success')
    return redirect(url_for('admin.jobs'))


@admin.route('/job/<int:job_id>/open', methods=['POST'])
@login_required
def open_job(job_id):
    """Reopen a closed job posting"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    job = Job.query.get_or_404(job_id)
    job.status = 'active'
    db.session.commit()
    
    flash('Job reopened successfully.', 'success')
    return redirect(url_for('admin.jobs'))


@admin.route('/delete-job/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    """Delete a job posting"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    job = Job.query.get_or_404(job_id)
    
    # Delete applications first
    for app in job.applications:
        db.session.delete(app)
    
    db.session.delete(job)
    db.session.commit()
    
    flash('Job deleted successfully.', 'success')
    return redirect(url_for('admin.jobs'))


@admin.route('/applications')
@login_required
def applications():
    """Manage all applications"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = Application.query
    
    if status:
        query = query.filter_by(status=status)
    
    if search:
        query = query.join(Job).join(User).filter(
            (Job.title.contains(search)) |
            (User.name.contains(search)) |
            (User.email.contains(search))
        )
    
    applications_pagination = query.order_by(Application.applied_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/applications.html', applications=applications_pagination)


@admin.route('/employer/<int:employer_id>')
@login_required
def view_employer(employer_id):
    """View employer details"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    employer = User.query.get_or_404(employer_id)
    if employer.role != 'employer':
        flash('User is not an employer.', 'danger')
        return redirect(url_for('admin.employers'))
    
    jobs = Job.query.filter_by(employer_id=employer_id).all()
    applications = Application.query.join(Job).filter(Job.employer_id == employer_id).all()
    
    return render_template('admin/view_employer.html', employer=employer, jobs=jobs, applications=applications)


@admin.route('/employer/<int:employer_id>/approve', methods=['POST'])
@login_required
def approve_employer(employer_id):
    """Approve an employer"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    employer = User.query.get_or_404(employer_id)
    if employer.role != 'employer':
        flash('User is not an employer.', 'danger')
        return redirect(url_for('admin.employers'))
    
    # Update employer approval status (if such a field exists)
    # For now, just flash success
    flash(f'Employer {employer.name} has been approved.', 'success')
    return redirect(url_for('admin.employers'))


@admin.route('/delete-employer/<int:employer_id>', methods=['POST'])
@login_required
def delete_employer(employer_id):
    """Delete an employer"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    employer = User.query.get_or_404(employer_id)
    
    if employer.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.employers'))
    
    if employer.role != 'employer':
        flash('User is not an employer.', 'danger')
        return redirect(url_for('admin.employers'))
    
    # Delete employer's jobs and applications
    for job in employer.jobs:
        for app in job.applications:
            db.session.delete(app)
        db.session.delete(job)
    
    for app in employer.applications:
        db.session.delete(app)
    
    db.session.delete(employer)
    db.session.commit()
    
    flash('Employer deleted successfully.', 'success')
    return redirect(url_for('admin.employers'))


@admin.route('/jobseeker/<int:jobseeker_id>')
@login_required
def view_jobseeker(jobseeker_id):
    """View job seeker details"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    jobseeker = User.query.get_or_404(jobseeker_id)
    if jobseeker.role != 'jobseeker':
        flash('User is not a job seeker.', 'danger')
        return redirect(url_for('admin.jobseekers'))
    
    profile = Profile.query.filter_by(user_id=jobseeker_id).first()
    applications = Application.query.filter_by(jobseeker_id=jobseeker_id).all()
    
    return render_template('admin/view_jobseeker.html', jobseeker=jobseeker, profile=profile, applications=applications)


@admin.route('/delete-jobseeker/<int:jobseeker_id>', methods=['POST'])
@login_required
def delete_jobseeker(jobseeker_id):
    """Delete a job seeker"""
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    jobseeker = User.query.get_or_404(jobseeker_id)
    
    if jobseeker.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.jobseekers'))
    
    if jobseeker.role != 'jobseeker':
        flash('User is not a job seeker.', 'danger')
        return redirect(url_for('admin.jobseekers'))
    
    # Delete job seeker's applications
    for app in jobseeker.applications:
        db.session.delete(app)
    
    # Delete job seeker's profile
    profile = Profile.query.filter_by(user_id=jobseeker_id).first()
    if profile:
        db.session.delete(profile)
    
    db.session.delete(jobseeker)
    db.session.commit()
    
    flash('Job seeker deleted successfully.', 'success')
    return redirect(url_for('admin.jobseekers'))

