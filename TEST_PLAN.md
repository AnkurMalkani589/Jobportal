# Job Portal Application - Comprehensive Test Plan

## Executive Summary
This document provides a comprehensive test plan for the Job Portal web application built with Python Flask, SQLite, and Bootstrap 5. The test plan covers installation verification, authentication, role-based access control, user interface, database integrity, security, and edge cases.

---

## 1. Application Installation & Setup Tests

### 1.1 Dependency Installation Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| INSTALL-001 | Install Python dependencies | Run `pip install -r requirements.txt` | All packages installed without errors | ☐ |
| INSTALL-002 | Verify Flask version | Check `Flask --version` | Flask 3.0.0+ installed | ☐ |
| INSTALL-003 | Verify SQLAlchemy | Check version | SQLAlchemy 2.0.23+ installed | ☐ |
| INSTALL-004 | Verify Flask-Login | Check version | Flask-Login 0.6.3+ installed | ☐ |
| INSTALL-005 | Verify Flask-Bcrypt | Check version | Flask-Bcrypt 1.0.1+ installed | ☐ |
| INSTALL-006 | Verify Bootstrap-Flask | Check version | Bootstrap-Flask 2.3.3+ installed | ☐ |

### 1.2 Database Creation Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| DB-001 | Create SQLite database | Run application | `job_portal.db` created successfully | ☐ |
| DB-002 | Create tables | Check database schema | Users, Jobs, Applications, Profiles tables created | ☐ |
| DB-003 | Verify foreign keys | Query foreign key constraints | All relationships properly defined | ☐ |
| DB-004 | Test database connection | Run database query | Connection successful, no errors | ☐ |
| DB-005 | Run existing test script | Execute `python test_app.py` | All tests pass | ☐ |

### 1.3 Flask Server Execution Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| SERVER-001 | Start Flask server | Run `python app.py` | Server starts on port 5000 | ☐ |
| SERVER-002 | Access homepage | Navigate to `http://localhost:5000/` | Homepage loads correctly | ☐ |
| SERVER-003 | Verify debug mode | Check console output | Debug mode active | ☐ |
| SERVER-004 | Verify blueprints | Check registered blueprints | Auth, Main, Admin, Employer, Jobseeker registered | ☐ |
| SERVER-005 | Test hot reload | Modify file and refresh | Changes reflect immediately | ☐ |

---

## 2. Authentication System Tests

### 2.1 User Registration Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| REG-001 | Register new jobseeker | Submit valid jobseeker registration form | Account created, redirect to login | ☐ |
| REG-002 | Register new employer | Submit valid employer registration form | Account created, redirect to login | ☐ |
| REG-003 | Duplicate email prevention | Register with existing email | Error message displayed | ☐ |
| REG-004 | Invalid email format | Register with bad email format | Form validation error | ☐ |
| REG-005 | Short password rejection | Register with password < 6 chars | Form validation error | ☐ |
| REG-006 | Password mismatch | Register with mismatched passwords | Form validation error | ☐ |
| REG-007 | Empty name rejection | Register with empty name | Form validation error | ☐ |
| REG-008 | Role selection | Verify role dropdown works | Selected role stored correctly | ☐ |
| REG-009 | Profile creation | Check profile table after registration | Empty profile created for user | ☐ |
| REG-010 | Admin registration disabled | Verify admin role not available | Admin role not in registration options | ☐ |

### 2.2 User Login Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| LOGIN-001 | Valid login | Login with correct credentials | Redirected to role-specific dashboard | ☐ |
| LOGIN-002 | Invalid password | Login with wrong password | Error message displayed | ☐ |
| LOGIN-003 | Invalid email | Login with unregistered email | Error message displayed | ☐ |
| LOGIN-004 | Remember me functionality | Login with remember me checked | Session persists after browser close | ☐ |
| LOGIN-005 | Already authenticated redirect | Access login page when logged in | Redirected to dashboard | ☐ |
| LOGIN-006 | CSRF protection | Submit login without CSRF token | Request rejected | ☐ |
| LOGIN-007 | Empty email field | Submit login with empty email | Form validation error | ☐ |
| LOGIN-008 | Empty password field | Submit login with empty password | Form validation error | ☐ |

### 2.3 Logout Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| LOGOUT-001 | Successful logout | Click logout button | Session cleared, redirect to home | ☐ |
| LOGOUT-002 | Post-logout redirect | Try to access dashboard after logout | Redirected to login | ☐ |
| LOGOUT-003 | Multiple tab logout | Logout from one tab, refresh other | Other tabs also logged out | ☐ |

### 2.4 Password Hashing Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| PWD-001 | Password encryption | Check database for hashed password | Password stored as bcrypt hash | ☐ |
| PWD-002 | Password verification | Login with correct password | Password verified successfully | ☐ |
| PWD-003 | Rainbow table prevention | Check hashed password | Each hash should be unique (with salt) | ☐ |
| PWD-004 | Different hash for same password | Register two users with same password | Hashes are different | ☐ |

---

## 3. Role-Based Access Control (RBAC) Tests

### 3.1 Admin Access Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| ADMIN-001 | Access admin dashboard | Login as admin, navigate to dashboard | Dashboard loads with statistics | ☐ |
| ADMIN-002 | View all employers | Navigate to employers page | All employers visible | ☐ |
| ADMIN-003 | View all jobseekers | Navigate to jobseekers page | All jobseekers visible | ☐ |
| ADMIN-004 | View all jobs | Navigate to jobs page | All jobs visible with counts | ☐ |
| ADMIN-005 | View all applications | Navigate to applications page | All applications visible | ☐ |
| ADMIN-006 | Delete employer | Delete an employer account | Employer and related data deleted | ☐ |
| ADMIN-007 | Delete jobseeker | Delete a jobseeker account | Jobseeker and related data deleted | ☐ |
| ADMIN-008 | Close job posting | Close an active job | Job status changed to 'closed' | ☐ |
| ADMIN-009 | Reopen closed job | Reopen a closed job | Job status changed to 'active' | ☐ |
| ADMIN-010 | Delete job | Delete a job posting | Job and applications deleted | ☐ |
| ADMIN-011 | Period statistics | View daily/weekly/monthly/yearly stats | Correct counts for period displayed | ☐ |
| ADMIN-012 | Search functionality | Search employers/jobseekers/jobs | Filtered results displayed | ☐ |
| ADMIN-013 | Pagination | Navigate through multiple pages | Pagination works correctly | ☐ |

### 3.2 Employer Access Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| EMP-001 | Access employer dashboard | Login as employer | Dashboard loads with statistics | ☐ |
| EMP-002 | View own jobs | Navigate to my jobs page | Only own jobs visible | ☐ |
| EMP-003 | Post new job | Create new job posting | Job created with 'active' status | ☐ |
| EMP-004 | Edit own job | Edit a job they created | Job updated successfully | ☐ |
| EMP-005 | Edit others' job | Try to edit another employer's job | Access denied message | ☐ |
| EMP-006 | Delete own job | Delete a job they created | Job deleted successfully | ☐ |
| EMP-007 | Delete others' job | Try to delete another employer's job | Access denied message | ☐ |
| EMP-008 | View applications to own jobs | View applications page | Only applications to own jobs visible | ☐ |
| EMP-009 | Review application | Mark application as reviewed | Application status updated | ☐ |
| EMP-010 | Accept application | Accept an application | Application status changed to 'accepted' | ☐ |
| EMP-011 | Reject application | Reject an application | Application status changed to 'rejected' | ☐ |
| EMP-012 | Access admin routes | Try to access admin dashboard | Access denied, redirect to home | ☐ |
| EMP-013 | Update profile | Update employer profile | Profile updated successfully | ☐ |
| EMP-014 | Change password | Update password | Password updated and hashed | ☐ |

### 3.3 Jobseeker Access Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| JS-001 | Access jobseeker dashboard | Login as jobseeker | Dashboard loads with statistics | ☐ |
| JS-002 | Browse jobs | Navigate to browse jobs | All active jobs visible | ☐ |
| JS-003 | Search jobs | Use search functionality | Jobs filtered by search term | ☐ |
| JS-004 | Filter jobs by location | Filter by location | Only jobs in location shown | ☐ |
| JS-005 | Filter by job type | Filter by full-time/part-time | Only matching jobs shown | ☐ |
| JS-006 | Filter by experience | Filter by experience level | Only matching jobs shown | ☐ |
| JS-007 | View job details | Click on a job | Full job details displayed | ☐ |
| JS-008 | Apply to job | Submit application form | Application created with 'pending' status | ☐ |
| JS-009 | Duplicate application prevention | Apply to same job twice | Error: Already applied | ☐ |
| JS-010 | Apply to closed job | Try to apply to closed job | Error: Job no longer accepting applications | ☐ |
| JS-011 | View application history | Navigate to applications page | All applications visible | ☐ |
| JS-012 | Filter applications by status | Filter applications | Only matching applications shown | ☐ |
| JS-013 | View application details | Click on an application | Full application details shown | ☐ |
| JS-014 | Withdraw pending application | Withdraw application | Application deleted | ☐ |
| JS-015 | Withdraw reviewed application | Try to withdraw reviewed app | Error: Cannot withdraw | ☐ |
| JS-016 | Update profile | Update jobseeker profile | Profile updated successfully | ☐ |
| JS-017 | Upload resume | Upload resume file | File saved to uploads folder | ☐ |
| JS-018 | Update password | Change password | Password updated and hashed | ☐ |
| JS-019 | Access admin routes | Try to access admin dashboard | Access denied | ☐ |
| JS-020 | Access employer routes | Try to access employer dashboard | Access denied | ☐ |

### 3.4 Unauthenticated Access Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| UNAUTH-001 | Access login page | Navigate to /login | Login page loads | ☐ |
| UNAUTH-002 | Access register page | Navigate to /register | Register page loads | ☐ |
| UNAUTH-003 | Access home page | Navigate to / | Home page loads | ☐ |
| UNAUTH-004 | Access public jobs | Navigate to /jobs | Jobs list page loads | ☐ |
| UNAUTH-005 | Access public job detail | Navigate to /job/1 | Job detail page loads | ☐ |
| UNAUTH-006 | Access about page | Navigate to /about | About page loads | ☐ |
| UNAUTH-007 | Access contact page | Navigate to /contact | Contact page loads | ☐ |
| UNAUTH-008 | Access admin dashboard | Navigate to /admin | Redirected to login | ☐ |
| UNAUTH-009 | Access employer dashboard | Navigate to /employer | Redirected to login | ☐ |
| UNAUTH-010 | Access jobseeker dashboard | Navigate to /jobseeker | Redirected to login | ☐ |

---

## 4. User Interface Tests

### 4.1 Header & Navigation Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| UI-001 | Logo visibility | Load any authenticated page | Logo visible in navbar | ☐ |
| UI-002 | Navbar links for admin | Login as admin | Admin-specific nav items visible | ☐ |
| UI-003 | Navbar links for employer | Login as employer | Employer-specific nav items visible | ☐ |
| UI-004 | Navbar links for jobseeker | Login as jobseeker | Jobseeker-specific nav items visible | ☐ |
| UI-005 | User dropdown | Click user avatar | Dropdown with profile/logout options | ☐ |
| UI-006 | Mobile hamburger menu | Resize to mobile width | Hamburger menu appears | ☐ |
| UI-007 | Navbar responsiveness | Test on mobile | Navbar collapses correctly | ☐ |

### 4.2 Sidebar Navigation Tests (Desktop)

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| SIDEBAR-001 | Sidebar visibility | Load dashboard on desktop | Sidebar visible on left | ☐ |
| SIDEBAR-002 | Sidebar sections | Check sidebar content | Admin/Employer/Jobseeker sections correct | ☐ |
| SIDEBAR-003 | Sidebar collapse | Click collapse button | Sidebar collapses to icons only | ☐ |
| SIDEBAR-004 | Sidebar expand on hover | Hover over collapsed sidebar | Sidebar expands | ☐ |
| SIDEBAR-005 | State persistence | Collapse, refresh page | Collapsed state maintained | ☐ |
| SIDEBAR-006 | Active menu highlight | Navigate to different pages | Correct menu item highlighted | ☐ |
| SIDEBAR-007 | Sidebar icons | Check all menu icons | All icons visible and correct | ☐ |
| SIDEBAR-008 | Sidebar navigation links | Click each sidebar link | Correct page loads | ☐ |

### 4.3 Sidebar Navigation Tests (Mobile/Tablet)

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| SIDEBAR-M-001 | Hidden sidebar | Load dashboard on mobile | Sidebar hidden by default | ☐ |
| SIDEBAR-M-002 | Mobile toggle button | Click hamburger menu | Sidebar opens from left | ☐ |
| SIDEBAR-M-003 | Sidebar overlay | Sidebar open | Dark overlay on content | ☐ |
| SIDEBAR-M-004 | Close sidebar | Click overlay | Sidebar closes | ☐ |
| SIDEBAR-M-005 | Sidebar content on mobile | Open sidebar on mobile | All menu items visible | ☐ |
| SIDEBAR-M-006 | Touch scrolling | Swipe sidebar | Smooth scrolling | ☐ |

### 4.4 Footer Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| FOOTER-001 | Footer visibility | Load any page | Footer visible at bottom | ☐ |
| FOOTER-002 | Copyright text | Check footer | Current year displayed | ☐ |
| FOOTER-003 | Footer position on short pages | Load short content page | Footer at bottom of viewport | ☐ |
| FOOTER-004 | Footer on long pages | Load page with lots of content | Footer at page end | ☐ |

### 4.5 Responsive Design Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| RESP-001 | Desktop view (≥992px) | Resize browser to 1200px | Full sidebar, normal layout | ☐ |
| RESP-002 | Tablet view (768-991px) | Resize browser to 850px | Collapsible sidebar | ☐ |
| RESP-003 | Mobile view (<768px) | Resize browser to 375px | Single column, hidden sidebar | ☐ |
| RESP-004 | Dashboard cards on mobile | Check mobile view | Cards stack vertically | ☐ |
| RESP-005 | Tables on mobile | Check table pages | Horizontal scroll enabled | ☐ |
| RESP-006 | Forms on mobile | Check form pages | Inputs full width | ☐ |
| RESP-007 | Modals on mobile | Open modal on mobile | Properly sized and centered | ☐ |

---

## 5. Database Integrity Tests

### 5.1 Relationship Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| DBINT-001 | User-Profile relationship | Query user profile | Profile linked correctly to user | ☐ |
| DBINT-002 | User-Job relationship | Query employer jobs | Jobs linked correctly to employer | ☐ |
| DBINT-003 | User-Application relationship | Query jobseeker applications | Applications linked correctly | ☐ |
| DBINT-004 | Job-Application relationship | Query job applications | Applications linked to job | ☐ |
| DBINT-005 | Cascade delete user | Delete user with jobs/applications | Related records deleted | ☐ |
| DBINT-006 | Cascade delete job | Delete job with applications | Applications deleted | ☐ |

### 5.2 Data Consistency Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| CONSIST-001 | Unique email constraint | Try to create duplicate email | Database error prevented | ☐ |
| CONSIST-002 | Required fields | Try to create user without email | Validation error | ☐ |
| CONSIST-003 | Role values | Check user roles | Only valid roles stored (admin/employer/jobseeker) | ☐ |
| CONSIST-004 | Job status values | Check job statuses | Only valid statuses (active/closed/draft) | ☐ |
| CONSIST-005 | Application status values | Check application statuses | Only valid statuses (pending/reviewed/accepted/rejected) | ☐ |
| CONSIST-006 | Timestamps | Create records | created_at and updated_at set correctly | ☐ |

### 5.3 Data Integrity Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| DATA-001 | User count accuracy | Count users | Correct count returned | ☐ |
| DATA-002 | Job count accuracy | Count jobs | Correct count returned | ☐ |
| DATA-003 | Application count accuracy | Count applications | Correct count returned | ☐ |
| DATA-004 | Application per job count | Query job application count | Correct count for each job | ☐ |
| DATA-005 | Jobs per employer count | Query employer job count | Correct count for each employer | ☐ |

---

## 6. Security Tests

### 6.1 Session Security Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| SEC-001 | Session timeout | Inactive for 24 hours | Session expired, require re-login | ☐ |
| SEC-002 | Session fixation | Check session ID after login | New session ID created | ☐ |
| SEC-003 | Session cookies | Check cookie attributes | HttpOnly, Secure flags set | ☐ |
| SEC-004 | CSRF protection | Submit form without CSRF token | Request rejected with 400 error | ☐ |
| SEC-005 | Valid CSRF token | Submit form with valid token | Request accepted | ☐ |

### 6.2 Password Security Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| SEC-006 | Password minimum length | Try to set password < 6 chars | Validation error | ☐ |
| SEC-007 | Password hashing algorithm | Check hash format | Bcrypt hash with salt | ☐ |
| SEC-008 | Direct password access | Try to read user.password | AttributeError raised | ☐ |

### 6.3 Access Control Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| SEC-009 | Admin-only routes | Try admin routes as employer | 403 Forbidden | ☐ |
| SEC-010 | Employer-only routes | Try employer routes as jobseeker | 403 Forbidden | ☐ |
| SEC-011 | Jobseeker-only routes | Try jobseeker routes as employer | 403 Forbidden | ☐ |
| SEC-012 | Protected route access | Access protected route without login | Redirect to login | ☐ |
| SEC-013 | Direct URL access | Try to access other user's data | Access denied | ☐ |

### 6.4 Input Validation Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| SEC-014 | XSS prevention | Submit script tag in form | Script escaped in output | ☐ |
| SEC-015 | SQL injection | Submit SQL in search form | Query parameterization prevents injection | ☐ |
| SEC-016 | File upload restrictions | Upload invalid file type | Upload rejected | ☐ |
| SEC-017 | Upload size limit | Upload file > 16MB | Upload rejected | ☐ |
| SEC-018 | Path traversal prevention | Upload file with ../../../ | Filename sanitized | ☐ |

### 6.5 Error Handling Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| ERR-001 | 404 page | Navigate to non-existent page | Custom 404 page displayed | ☐ |
| ERR-002 | 500 page | Trigger server error | Custom 500 page displayed | ☐ |
| ERR-003 | 403 page | Access forbidden page | Custom 403 page displayed | ☐ |
| ERR-004 | Database error handling | Query non-existent record | Graceful error handling | ☐ |

---

## 7. Feature-Specific Tests

### 7.1 Dashboard Statistics Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| DASH-001 | Admin daily stats | View dashboard with period=daily | Correct daily counts | ☐ |
| DASH-002 | Admin weekly stats | View dashboard with period=weekly | Correct weekly counts | ☐ |
| DASH-003 | Admin monthly stats | View dashboard with period=monthly | Correct monthly counts | ☐ |
| DASH-004 | Admin yearly stats | View dashboard with period=yearly | Correct yearly counts | ☐ |
| DASH-005 | Employer job stats | View employer dashboard | Correct job counts (total/active/closed) | ☐ |
| DASH-006 | Employer application stats | View employer dashboard | Correct application counts | ☐ |
| DASH-007 | Jobseeker application stats | View jobseeker dashboard | Correct application counts by status | ☐ |

### 7.2 Job Posting Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| JOB-001 | Create job with all fields | Submit complete job form | Job created with all fields | ☐ |
| JOB-002 | Create job with required fields | Submit minimal job form | Job created with defaults | ☐ |
| JOB-003 | Job with draft status | Create job with draft status | Job created as draft | ☐ |
| JOB-004 | Job with deadline | Set job deadline | Deadline saved correctly | ☐ |
| JOB-005 | Edit existing job | Modify job fields | Job updated successfully | ☐ |
| JOB-006 | View job on public page | Navigate to /job/id | Job visible to public | ☐ |
| JOB-007 | View count increment | Access job detail | View count increases | ☐ |

### 7.3 Application Workflow Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| APP-001 | Complete application | Submit application with cover letter | Application created | ☐ |
| APP-002 | Minimal application | Submit application without cover letter | Application created | ☐ |
| APP-003 | Employer views application | Access application detail | Full details visible | ☐ |
| APP-004 | Application status workflow | Review → Accept/Reject | Status updates correctly | ☐ |
| APP-005 | Jobseeker views own application | Access application detail | Details visible | ☐ |

### 7.4 Profile Management Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| PROF-001 | Update profile name | Change name | Name updated | ☐ |
| PROF-002 | Update profile email | Change email | Email updated | ☐ |
| PROF-003 | Update jobseeker skills | Add skills | Skills saved | ☐ |
| PROF-004 | Update employer company | Update company info | Company info saved | ☐ |
| PROF-005 | Upload resume file | Upload PDF resume | File saved, path stored | ☐ |
| PROF-006 | Download resume | Access resume file | File downloads correctly | ☐ |

---

## 8. Edge Cases & Boundary Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| EDGE-001 | Empty database | Start with fresh DB | All tables created, no errors | ☐ |
| EDGE-002 | No jobs in database | Browse jobs page | Empty state displayed | ☐ |
| EDGE-003 | No applications | View applications page | Empty state displayed | ☐ |
| EDGE-004 | Multiple pagination pages | Create > 10 items | Pagination works | ☐ |
| EDGE-005 | Very long job description | Submit job with 5000 char description | Description truncated or fully displayed | ☐ |
| EDGE-006 | Special characters in input | Use emojis, symbols | Handled correctly | ☐ |
| EDGE-007 | Unicode characters | Use non-ASCII characters | Displayed correctly | ☐ |
| EDGE-008 | Duplicate job titles | Create multiple jobs with same title | All created successfully | ☐ |
| EDGE-009 | Self-application prevention | Apply to own job (as employer) | Not applicable (employers can't apply) | ☐ |
| EDGE-010 | Expired job deadline | Apply to expired job | Deadline check prevents application | ☐ |
| EDGE-011 | Concurrent applications | Multiple users apply simultaneously | All applications recorded | ☐ |
| EDGE-012 | Bulk delete employers | Delete multiple employers | All deleted with cascading | ☐ |
| EDGE-013 | Session during password change | Change password then use old session | Old session invalidated | ☐ |
| EDGE-014 | Remember me persistence | Login with remember, close browser, reopen | Still logged in | ☐ |
| EDGE-015 | Login with different roles | Login, logout, login as different role | Role-specific access works | ☐ |

---

## 9. Performance Tests

| Test Case ID | Description | Steps | Expected Result | Status |
|--------------|-------------|-------|-----------------|--------|
| PERF-001 | Page load time | Measure homepage load | < 2 seconds | ☐ |
| PERF-002 | Dashboard load time | Measure dashboard load | < 3 seconds | ☐ |
| PERF-003 | Search response time | Search with results | < 1 second | ☐ |
| PERF-004 | Pagination performance | Navigate through 10+ pages | Quick response | ☐ |
| PERF-005 | Large dataset query | Query > 1000 records | Still performant | ☐ |

---

## 10. Test Results Summary

### Test Execution Log

| Date | Tester | Total Tests | Passed | Failed | Skipped | Notes |
|------|--------|-------------|--------|--------|---------|-------|
| | | | | | | |

### Defect Log

| Defect ID | Description | Severity | Status | Fix Date |
|-----------|-------------|----------|--------|----------|
| | | | | |

### Improvement Suggestions

#### High Priority
1. **Add email verification**: Implement email confirmation before account activation
2. **Add password strength meter**: Visual feedback on password complexity
3. **Implement rate limiting**: Prevent brute force attacks on login
4. **Add audit logging**: Track all administrative actions

#### Medium Priority
1. **Add social login**: Google/Facebook OAuth integration
2. **Implement job alerts**: Email notifications for matching jobs
3. **Add file type preview**: Show PDF resumes in browser
4. **Implement lazy loading**: For job listings and images

#### Low Priority
1. **Add dark mode**: Theme toggle for user preference
2. **Implement keyboard shortcuts**: Quick navigation for power users
3. **Add breadcrumb navigation**: Improved navigation UX
4. **Implement print styles**: Better printing for applications

---

## Appendix A: Test Environment

- **Python Version**: 3.12.x
- **Flask Version**: 3.0.0
- **Database**: SQLite (job_portal.db)
- **Browser**: Chrome/Firefox/Safari (latest)
- **OS**: Linux

## Appendix B: Test Data Requirements

### Required Test Accounts
1. Admin account (created via `create_admin.py`)
2. At least 2 employer accounts
3. At least 3 jobseeker accounts
4. At least 5 job postings
5. At least 10 applications

### Sample Test Data
- Various job types (Full-time, Part-time, Contract, Remote)
- Various experience levels (Entry, Mid, Senior)
- Different locations and salaries

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: QA Team

