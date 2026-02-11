# Job Portal Debugging & Fix Plan

## Issues Identified and Fixes Required

### 1. MISSING ROUTES IN BLUEPRINTS

#### 1.1 employer/routes.py - Missing Routes
**Issue**: The admin/jobs.html template references these routes that don't exist:
- `employer.close_job` 
- `employer.open_job`
- `employer.delete_job`

**Fix**: Add these routes to employer/routes.py

#### 1.2 admin/routes.py - Missing Routes  
**Issue**: Template admin/jobs.html references routes that don't exist:
- `admin.close_job`
- `admin.open_job`
- `admin.delete_job`

**Fix**: Add these routes to admin/routes.py

#### 1.3 jobseeker/routes.py - Missing Route
**Issue**: Template jobseeker/applications.html references:
- `jobseeker.application_detail` (doesn't exist)

**Fix**: Either create the route OR fix the template to link to a valid route

---

### 2. TEMPLATE ISSUES

#### 2.1 main/job_detail.html - Wrong Variable Name
**Issue**: Line uses `has_applied` variable that is never passed
```python
{% if has_applied %}
```
But the route passes `applied_job_ids` list.

**Fix**: Change to `{% if job.id in applied_job_ids %}`

#### 2.2 employer/job_form.html - Wrong Field Name
**Issue**: Uses `job.application_deadline` but Job model uses `deadline`
```python
value="{{ job.application_deadline.strftime('%Y-%m-%d') if job and job.application_deadline else '' }}"
```

**Fix**: Change `application_deadline` to `deadline`

#### 2.3 jobseeker/job_detail.html - Wrong Field Name  
**Issue**: Uses `job.application_deadline` and `job.application_count`
- `application_deadline` → `deadline`
- `job.application_count` → need to pass from route

**Fix**: Update field references and pass application_count

#### 2.4 employer/profile.html - Non-existent Field
**Issue**: Uses `user.company_name` but User model doesn't have this field
```python
value="{{ user.company_name if user and not job else job.company_name if job else '' }}"
```

**Fix**: Remove or handle gracefully

#### 2.5 admin/jobs.html - References Missing Routes
**Issue**: Template uses routes that don't exist:
- `admin.close_job`
- `admin.open_job`  
- `admin.delete_job`

**Fix**: Either create the routes OR fix templates to use existing routes

---

### 3. JAVASCRIPT/UI ISSUES

#### 3.1 base.html - User Dropdown Not Working
**Issue**: User dropdown uses `data-bs-toggle="dropdown"` on element with class `user-dropdown` which doesn't have proper Bootstrap dropdown structure.

**Fix**: Add `data-bs-toggle="dropdown"` to proper element and ensure dropdown structure is correct

#### 3.2 base.html - Navbar Toggle Issues
**Issue**: The authenticated navbar has a mobile toggle button but navbar collapse may not work properly

**Fix**: Ensure Bootstrap data attributes are properly set

---

### 4. BLUEPRINT INITIALIZATION

#### 4.1 auth/__init__.py - Empty File
**Issue**: The auth/__init__.py file is empty but might need initialization code

**Fix**: Typically Flask blueprints don't need initialization in __init__.py unless there are before_request handlers, etc. Current setup is fine as routes are directly imported in app.py

---

### 5. OTHER ISSUES

#### 5.1 home.html - Invalid Route Parameter
**Issue**: Links use `url_for('auth.register', role='jobseeker')` 
- Registration form doesn't accept `role` parameter

**Fix**: Either accept role in form or remove from URL

---

## Implementation Order

1. **Phase 1: Critical Route Fixes**
   - Add missing routes to employer/routes.py
   - Add missing routes to admin/routes.py
   - Fix jobseeker application_detail route

2. **Phase 2: Template Fixes**
   - Fix variable names in job_detail.html templates
   - Fix field names in job_form.html
   - Fix profile.html non-existent fields
   - Fix admin/jobs.html missing routes

3. **Phase 3: JavaScript/UI Fixes**
   - Fix user dropdown in base.html
   - Fix navbar toggle

4. **Phase 4: Testing**
   - Verify all buttons, links, forms work
   - Test role-based access
   - Test authentication flow

