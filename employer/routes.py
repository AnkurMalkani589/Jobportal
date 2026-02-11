"""
Employer routes for Job Portal
Handles employer dashboard, job management, and application handling
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Job, Application, User
from extensions import db
from datetime import datetime

employer = Blueprint('employer', __name__)


@employer.route('/')
@login_required
def dashboard():
    """Employer dashboard with statistics"""
    if not current_user.is_employer():
        flash('Access denied. Employer privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    # Statistics
    total_jobs = Job.query.filter_by(employer_id=current_user.id).count()
    active_jobs = Job.query.filter_by(employer_id=current_user.id, status='active').count()
    closed_jobs = Job.query.filter_by(employer_id=current_user.id, status='closed').count()
    
    # Get applications
    employer_jobs = Job.query.filter_by(employer_id=current_user.id).all()
    job_ids = [job.id for job in employer_jobs]
    
    total_applications = Application.query.filter(Application.job_id.in_(job_ids)).count()
    pending_apps = Application.query.filter(
        Application.job_id.in_(job_ids),
        Application.status == 'pending'
    ).count()
    
    # Recent jobs
    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(
        Job.created_at.desc()
    ).limit(5).all()
    
    # Recent applications
    recent_applications = Application.query.filter(
        Application.job_id.in_(job_ids)
    ).order_by(
        Application.applied_at.desc()
    ).limit(5).all()
    
    return render_template('employer/dashboard.html',
                         total_jobs=total_jobs,
                         active_jobs=active_jobs,
                         closed_jobs=closed_jobs,
                         total_applications=total_applications,
                         pending_apps=pending_apps,
                         jobs=jobs,
                         recent_applications=recent_applications)


@employer.route('/jobs')
@login_required
def jobs():
    """List all jobs posted by employer"""
    if not current_user.is_employer():
        flash('Access denied. Employer privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Job.query.filter_by(employer_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    jobs_pagination = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('employer/jobs.html', jobs=jobs_pagination)


@employer.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_job():
    """Create a new job posting"""
    if not current_user.is_employer():
        flash('Access denied. Employer privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        job = Job(
            title=request.form.get('title'),
            description=request.form.get('description'),
            company_name=request.form.get('company_name'),
            company_description=request.form.get('company_description'),
            location=request.form.get('location'),
            salary=request.form.get('salary'),
            job_type=request.form.get('job_type'),
            experience_level=request.form.get('experience_level'),
            required_skills=request.form.get('required_skills'),
            benefits=request.form.get('benefits'),
            how_to_apply=request.form.get('how_to_apply'),
            application_email=request.form.get('application_email'),
            status=request.form.get('status', 'active'),
            employer_id=current_user.id
        )
        
        # Handle deadline
        deadline_str = request.form.get('deadline')
        if deadline_str:
            job.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        
        db.session.add(job)
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer.jobs'))
    
    return render_template('employer/job_form.html', job=None)


@employer.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    """Edit an existing job posting"""
    job = Job.query.get_or_404(job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only edit your own jobs.', 'danger')
        return redirect(url_for('employer.jobs'))
    
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.description = request.form.get('description')
        job.company_name = request.form.get('company_name')
        job.company_description = request.form.get('company_description')
        job.location = request.form.get('location')
        job.salary = request.form.get('salary')
        job.job_type = request.form.get('job_type')
        job.experience_level = request.form.get('experience_level')
        job.required_skills = request.form.get('required_skills')
        job.benefits = request.form.get('benefits')
        job.how_to_apply = request.form.get('how_to_apply')
        job.application_email = request.form.get('application_email')
        job.status = request.form.get('status', 'active')
        
        # Handle deadline
        deadline_str = request.form.get('deadline')
        if deadline_str:
            job.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        else:
            job.deadline = None
        
        db.session.commit()
        
        flash('Job updated successfully!', 'success')
        return redirect(url_for('employer.jobs'))
    
    return render_template('employer/job_form.html', job=job)


@employer.route('/job/<int:job_id>/close', methods=['POST'])
@login_required
def close_job(job_id):
    """Close a job posting"""
    job = Job.query.get_or_404(job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only close your own jobs.', 'danger')
        return redirect(url_for('employer.jobs'))
    
    job.status = 'closed'
    db.session.commit()
    
    flash('Job closed successfully!', 'success')
    return redirect(url_for('employer.jobs'))


@employer.route('/job/<int:job_id>/open', methods=['POST'])
@login_required
def open_job(job_id):
    """Reopen a closed job posting"""
    job = Job.query.get_or_404(job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only reopen your own jobs.', 'danger')
        return redirect(url_for('employer.jobs'))
    
    job.status = 'active'
    db.session.commit()
    
    flash('Job reopened successfully!', 'success')
    return redirect(url_for('employer.jobs'))


@employer.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    """Delete a job posting"""
    job = Job.query.get_or_404(job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only delete your own jobs.', 'danger')
        return redirect(url_for('employer.jobs'))
    
    # Delete applications
    for app in job.applications:
        db.session.delete(app)
    
    db.session.delete(job)
    db.session.commit()
    
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('employer.jobs'))


@employer.route('/applications')
@login_required
def applications():
    """View all applications to employer's jobs"""
    if not current_user.is_employer():
        flash('Access denied. Employer privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    employer_jobs = Job.query.filter_by(employer_id=current_user.id).all()
    job_ids = [job.id for job in employer_jobs]
    
    query = Application.query.filter(Application.job_id.in_(job_ids))
    
    if status:
        query = query.filter_by(status=status)
    
    applications_pagination = query.order_by(Application.applied_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('employer/applications.html', applications=applications_pagination)


@employer.route('/job/<int:job_id>/applications')
@login_required
def job_applications(job_id):
    """View applications for a specific job"""
    job = Job.query.get_or_404(job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only view applications for your own jobs.', 'danger')
        return redirect(url_for('employer.jobs'))
    
    applications = Application.query.filter_by(job_id=job_id).order_by(
        Application.applied_at.desc()
    ).all()
    
    return render_template('employer/applications.html', 
                         applications=applications,
                         job=job)


@employer.route('/application/<int:app_id>/review', methods=['POST'])
@login_required
def review_application(app_id):
    """Mark application as reviewed"""
    app = Application.query.get_or_404(app_id)
    job = Job.query.get(app.job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only review applications for your own jobs.', 'danger')
        return redirect(url_for('employer.applications'))
    
    app.status = 'reviewed'
    db.session.commit()
    
    flash('Application marked as reviewed.', 'info')
    return redirect(url_for('employer.applications'))


@employer.route('/application/<int:app_id>/accept', methods=['POST'])
@login_required
def accept_application(app_id):
    """Accept an application"""
    app = Application.query.get_or_404(app_id)
    job = Job.query.get(app.job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only accept applications for your own jobs.', 'danger')
        return redirect(url_for('employer.applications'))
    
    app.status = 'accepted'
    db.session.commit()
    
    flash('Application accepted!', 'success')
    return redirect(url_for('employer.applications'))


@employer.route('/application/<int:app_id>/reject', methods=['POST'])
@login_required
def reject_application(app_id):
    """Reject an application"""
    app = Application.query.get_or_404(app_id)
    job = Job.query.get(app.job_id)
    
    if job.employer_id != current_user.id:
        flash('You can only reject applications for your own jobs.', 'danger')
        return redirect(url_for('employer.applications'))
    
    app.status = 'rejected'
    db.session.commit()
    
    flash('Application rejected.', 'warning')
    return redirect(url_for('employer.applications'))


@employer.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Manage employer profile"""
    if not current_user.is_employer():
        flash('Access denied. Employer privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.email = request.form.get('email')
        
        # Update password if provided with validation
        new_password = request.form.get('password')
        if new_password:
            # Password validation: minimum 8 characters
            if len(new_password) < 8:
                flash('Password must be at least 8 characters long.', 'danger')
                return redirect(url_for('employer.profile'))
            current_user.password = new_password
        
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('employer.profile'))
    
    return render_template('employer/profile.html', user=current_user)

