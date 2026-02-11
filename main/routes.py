"""
Main routes for Job Portal
Handles home page, public job listings, and shared pages
"""
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user
from models import Job, Application, User
from extensions import db
from sqlalchemy import func

main = Blueprint('main', __name__)


@main.route('/')
def home():
    """Home page with featured jobs and statistics"""
    # Get featured/active jobs (limit to 6)
    featured_jobs = Job.query.filter_by(status='active').order_by(
        Job.created_at.desc()
    ).limit(6).all()
    
    # Get statistics
    total_jobs = Job.query.filter_by(status='active').count()
    total_applications = Application.query.count()
    total_companies = db.session.query(func.count(User.id)).filter_by(role='employer').scalar() or '100+'
    total_candidates = db.session.query(func.count(User.id)).filter_by(role='jobseeker').scalar() or '1000+'
    
    # Get job counts by category (based on search keywords)
    it_jobs = Job.query.filter(
        Job.status == 'active',
        (Job.title.contains('developer') | Job.title.contains('engineer') | Job.title.contains('tech'))
    ).count()
    
    marketing_jobs = Job.query.filter(
        Job.status == 'active',
        (Job.title.contains('marketing') | Job.title.contains('sales') | Job.title.contains('advertising'))
    ).count()
    
    sales_jobs = Job.query.filter(
        Job.status == 'active',
        (Job.title.contains('sales') | Job.title.contains('account') | Job.title.contains('business'))
    ).count()
    
    design_jobs = Job.query.filter(
        Job.status == 'active',
        (Job.title.contains('design') | Job.title.contains('creative') | Job.title.contains('ui') | Job.title.contains('ux'))
    ).count()
    
    finance_jobs = Job.query.filter(
        Job.status == 'active',
        (Job.title.contains('finance') | Job.title.contains('accounting') | Job.title.contains('bank'))
    ).count()
    
    return render_template('home.html', 
                         featured_jobs=featured_jobs,
                         total_jobs=total_jobs,
                         total_applications=total_applications,
                         total_companies=total_companies,
                         total_candidates=total_candidates,
                         it_jobs=it_jobs,
                         marketing_jobs=marketing_jobs,
                         sales_jobs=sales_jobs,
                         design_jobs=design_jobs,
                         finance_jobs=finance_jobs)


@main.route('/jobs')
def jobs():
    """Public job listings page with search and filters"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('type', '')
    experience = request.args.get('experience', '')
    
    # Build query
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
    jobs = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    
    return render_template('jobs.html', jobs=jobs)


@main.route('/job/<int:job_id>')
def job_detail(job_id):
    """Job detail page (public view)"""
    job = Job.query.get_or_404(job_id)
    
    # Increment view count
    job.views_count += 1
    db.session.commit()
    
    # Check if jobseeker has already applied
    applied_job_ids = []
    if current_user.is_authenticated and current_user.is_jobseeker():
        applications = Application.query.filter_by(
            jobseeker_id=current_user.id
        ).all()
        applied_job_ids = [app.job_id for app in applications]
    
    return render_template('job_detail.html', 
                         job=job,
                         applied_job_ids=applied_job_ids)


@main.route('/about')
def about():
    """About page"""
    # Get statistics
    total_jobs = Job.query.filter_by(status='active').count()
    total_applications = Application.query.count()
    total_employers = User.query.filter_by(role='employer').count()
    total_jobseekers = User.query.filter_by(role='jobseeker').count()
    
    return render_template('about.html',
                         total_jobs=total_jobs,
                         total_applications=total_applications,
                         total_employers=total_employers,
                         total_jobseekers=total_jobseekers)


@main.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

