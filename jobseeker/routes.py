"""
Jobseeker routes for Job Portal
Handles job browsing, applications, and profile management
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from flask_wtf.csrf import CSRFProtect
from models import Job, Application, Profile
from extensions import db
from werkzeug.utils import secure_filename
import os
import time

jobseeker = Blueprint('jobseeker', __name__)

# Allowed file extensions for resume
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@jobseeker.route('/')
@login_required
def dashboard():
    """Jobseeker dashboard with statistics"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    # Statistics
    total_applications = Application.query.filter_by(
        jobseeker_id=current_user.id
    ).count()
    
    pending_applications = Application.query.filter_by(
        jobseeker_id=current_user.id,
        status='pending'
    ).count()
    
    accepted_applications = Application.query.filter_by(
        jobseeker_id=current_user.id,
        status='accepted'
    ).count()
    
    rejected_applications = Application.query.filter_by(
        jobseeker_id=current_user.id,
        status='rejected'
    ).count()
    
    # Recent applications
    applications = Application.query.filter_by(
        jobseeker_id=current_user.id
    ).order_by(
        Application.applied_at.desc()
    ).limit(5).all()
    
    # Get applied job IDs for exclusion
    applied_job_ids = [app.job_id for app in applications]
    
    # Recommended jobs (active jobs not yet applied to)
    # Always use the filter to ensure scalability - even with empty list
    recommended_jobs = Job.query.filter(
        Job.status == 'active'
    ).filter(
        ~Job.id.in_(applied_job_ids) if applied_job_ids else Job.id.in_([-1])
    ).order_by(
        Job.created_at.desc()
    ).limit(5).all()
    
    return render_template('jobseeker/dashboard.html',
                         total_applications=total_applications,
                         pending_applications=pending_applications,
                         accepted_applications=accepted_applications,
                         rejected_applications=rejected_applications,
                         applications=applications,
                         recommended_jobs=recommended_jobs)


@jobseeker.route('/jobs')
@login_required
def jobs():
    """Browse available jobs"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('type', '')
    experience = request.args.get('experience', '')
    
    # Get already applied job IDs
    applications = Application.query.filter_by(jobseeker_id=current_user.id).all()
    applied_job_ids = [app.job_id for app in applications]
    
    # Build query for active jobs
    query = Job.query.filter_by(status='active')
    
    # Apply filters
    if search:
        query = query.filter(
            (Job.title.contains(search)) | 
            (Job.company_name.contains(search)) |
            (Job.description.contains(search))
        )
    
    if location:
        query = query.filter(Job.location.contains(location))
    
    if job_type:
        query = query.filter(Job.job_type == job_type)
    
    if experience:
        query = query.filter(Job.experience_level == experience)
    
    # Order and paginate
    jobs_pagination = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    
    return render_template('jobseeker/jobs.html', 
                         jobs=jobs_pagination,
                         applied_job_ids=applied_job_ids)


@jobseeker.route('/job/<int:job_id>')
@login_required
def job_detail(job_id):
    """View job details and apply"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied and get the application object
    application = Application.query.filter_by(
        jobseeker_id=current_user.id,
        job_id=job_id
    ).first()
    
    applied_job_ids = [job_id] if application else []
    
    # Get application count for this job
    application_count = Application.query.filter_by(job_id=job_id).count()
    
    return render_template('jobseeker/job_detail.html',
                         job=job,
                         applied_job_ids=applied_job_ids,
                         application=application,
                         application_count=application_count)


@jobseeker.route('/job/<int:job_id>/apply', methods=['POST'])
@login_required
def apply_job(job_id):
    """Apply for a job"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied
    existing = Application.query.filter_by(
        jobseeker_id=current_user.id,
        job_id=job_id
    ).first()
    
    if existing:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('jobseeker.job_detail', job_id=job_id))
    
    # Check if job is active
    if job.status != 'active':
        flash('This job is no longer accepting applications.', 'danger')
        return redirect(url_for('jobseeker.job_detail', job_id=job_id))
    
    # Create application
    application = Application(
        job_id=job_id,
        jobseeker_id=current_user.id,
        cover_letter=request.form.get('cover_letter', ''),
        additional_notes=request.form.get('additional_notes', ''),
        status='pending'
    )
    
    db.session.add(application)
    db.session.commit()
    
    flash('Your application has been submitted successfully!', 'success')
    return redirect(url_for('jobseeker.applications'))


@jobseeker.route('/applications')
@login_required
def applications():
    """View application history"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Application.query.filter_by(jobseeker_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    
    applications_pagination = query.order_by(Application.applied_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('jobseeker/applications.html',
                         applications=applications_pagination,
                         status_filter=status)


@jobseeker.route('/application/<int:app_id>')
@login_required
def application_detail(app_id):
    """View application details"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    application = Application.query.get_or_404(app_id)
    
    # Ensure the application belongs to the current user
    if application.jobseeker_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('jobseeker.applications'))
    
    job = Job.query.get(application.job_id)
    
    return render_template('jobseeker/application_detail.html',
                         application=application,
                         job=job)


@jobseeker.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Manage jobseeker profile"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    # Get or create profile
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    if request.method == 'POST':
        # Update user
        current_user.name = request.form.get('name')
        current_user.email = request.form.get('email')
        
        # Update profile
        profile.phone = request.form.get('phone', '')
        profile.address = request.form.get('address', '')
        profile.bio = request.form.get('bio', '')
        profile.skills = request.form.get('skills', '')
        profile.education = request.form.get('education', '')
        profile.experience_years = request.form.get('experience_years', 0)
        profile.linkedin = request.form.get('linkedin', '')
        profile.github = request.form.get('github', '')
        profile.additional_details = request.form.get('additional_details', '')
        
        # Handle resume upload with secure path handling
        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename and allowed_file(file.filename):
                # Use Flask config UPLOAD_FOLDER instead of hardcoded path
                upload_path = current_app.config.get('UPLOAD_FOLDER')
                if not upload_path:
                    flash('Upload configuration error.', 'danger')
                    return redirect(url_for('jobseeker.profile'))
                
                # Create directory if it doesn't exist
                os.makedirs(upload_path, exist_ok=True)
                
                # Generate safe filename using secure_filename
                original_filename = secure_filename(file.filename)
                ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'pdf'
                filename = f"resume_{current_user.id}_{int(time.time())}.{ext}"
                
                # Save file
                file.save(os.path.join(upload_path, filename))
                profile.resume_path = filename
        
        # Update password if provided with validation
        new_password = request.form.get('password')
        if new_password:
            # Password validation: minimum 8 characters
            if len(new_password) < 8:
                flash('Password must be at least 8 characters long.', 'danger')
                return redirect(url_for('jobseeker.profile'))
            current_user.password = new_password
        
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('jobseeker.profile'))
    
    return render_template('jobseeker/profile.html',
                         user=current_user,
                         profile=profile)


@jobseeker.route('/withdraw-application/<int:app_id>', methods=['POST'])
@login_required
def withdraw_application(app_id):
    """Withdraw an application"""
    if not current_user.is_jobseeker():
        flash('Access denied. Jobseeker privileges required.', 'danger')
        return redirect(url_for('main.home'))
    
    application = Application.query.get_or_404(app_id)
    
    # Ensure the application belongs to the current user
    if application.jobseeker_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('jobseeker.applications'))
    
    # Only allow withdrawal of pending applications
    if application.status != 'pending':
        flash('Cannot withdraw application that has already been reviewed.', 'warning')
        return redirect(url_for('jobseeker.applications'))
    
    db.session.delete(application)
    db.session.commit()
    
    flash('Application withdrawn successfully.', 'success')
    return redirect(url_for('jobseeker.applications'))

