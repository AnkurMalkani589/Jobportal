# Comprehensive Fix Plan - Job Portal Debugging & Audit

## Phase 1: Missing Routes (Critical - Breaks Buttons/Links)

### 1.1 Add Missing Routes to employer/routes.py
- `close_job(job_id)` - Change job status to closed
- `open_job(job_id)` - Change job status to active
- Fix delete_job to use POST or add confirmation

### 1.2 Add Missing Routes to admin/routes.py
- `close_job(job_id)` - Admin can close any job
- `open_job(job_id)` - Admin can reopen any job

### 1.3 Fix jobseeker/routes.py
- `application_detail(app_id)` - View application details OR update template to use existing route

---

## Phase 2: Template Variable Fixes (Breaks Display)

### 2.1 main/job_detail.html
- Change `{% if has_applied %}` to `{% if job.id in applied_job_ids %}`

### 2.2 employer/job_form.html
- Change `job.application_deadline` to `job.deadline`
- Add missing fields: requirements, company_description

### 2.3 jobseeker/job_detail.html
- Change `job.application_deadline` to `job.deadline`
- Pass application_count from route

### 2.4 employer/profile.html
- Remove `user.company_name` reference (doesn't exist in model)

### 2.5 admin/jobs.html
- Fix routes or add missing ones: close_job, open_job, delete_job

---

## Phase 3: Security Fixes (POST instead of GET for Actions)

### 3.1 Convert GET links to POST forms for:
- employer/routes.py: delete_job (should be POST)
- admin/routes.py: delete_user, delete_job (should be POST)
- All delete actions should use POST with confirmation

### 3.2 Add CSRF Tokens to Forms
- employer/profile.html - form needs CSRF token
- All POST forms should have CSRF protection

---

## Phase 4: Flash Message Fixes

### 4.1 Remove Duplicate Flash Messages
- login.html: Has both base.html flash AND manual flash loop
- Remove manual flash loop in templates (flash already shown in base.html)

---

## Phase 5: JavaScript & UI Fixes

### 5.1 JavaScript DOM Ready
- Move all JavaScript initialization inside DOMContentLoaded
- Ensure sidebar, dropdowns, toggles work after DOM loads

### 5.2 Mobile Sidebar Fixes
- Remove hover-only sidebar logic
- Add click/touch handlers for mobile
- Ensure sidebar-overlay works properly

### 5.3 User Dropdown Fix
- Fix Bootstrap dropdown structure in base.html
- Ensure data-bs-toggle is on correct element

---

## Phase 6: Role-Based Access & Redirects

### 6.1 Verify redirect_after_login()
- Admin → admin.dashboard
- Employer → employer.dashboard  
- Jobseeker → jobseeker.dashboard

### 6.2 Add Role Checks to All Protected Routes
- @login_required already in place
- Check role before accessing blueprint routes
- Redirect to appropriate dashboard if wrong role

---

## Implementation Order

1. Phase 1: Add missing routes
2. Phase 2: Fix template variables
3. Phase 3: Convert GET to POST for actions
4. Phase 4: Fix flash messages
5. Phase 5: JavaScript & UI fixes
6. Phase 6: Role-based access verification

---

## Files to Modify

1. employer/routes.py - Add missing routes
2. admin/routes.py - Add missing routes  
3. jobseeker/routes.py - Add application_detail route
4. templates/employer/job_form.html - Fix field names
5. templates/main/job_detail.html - Fix variable names
6. templates/jobseeker/job_detail.html - Fix field names
7. templates/employer/profile.html - Fix company_name reference
8. templates/admin/jobs.html - Fix routes
9. templates/login.html - Remove duplicate flash
10. static/js/main.js - Fix DOM ready issues
11. templates/base.html - Fix dropdown and sidebar

