// Job Portal Custom JavaScript
// All code runs after DOMContentLoaded event

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSidebar();
    initTooltips();
    initDropdowns();
    initFormValidation();
    initDeleteConfirmations();
    initFlashMessages();
    initActiveNavHighlight();
});

// ==========================================================================
// SIDEBAR FUNCTIONALITY
// ==========================================================================
function initSidebar() {
    const sidebarWrapper = document.getElementById('sidebarWrapper');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const mobileToggle = document.getElementById('mobileSidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    if (!sidebarWrapper) return;
    
    // Desktop sidebar toggle
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            sidebarWrapper.classList.toggle('collapsed');
            
            // Update toggle icon
            const icon = sidebarToggle.querySelector('i');
            if (icon) {
                if (sidebarWrapper.classList.contains('collapsed')) {
                    icon.className = 'bi bi-chevron-right';
                } else {
                    icon.className = 'bi bi-chevron-left';
                }
            }
            
            // Save state to localStorage
            localStorage.setItem('sidebarCollapsed', sidebarWrapper.classList.contains('collapsed'));
        });
    }
    
    // Mobile sidebar toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Toggle sidebar visibility on mobile
            if (window.innerWidth < 992) {
                sidebarWrapper.classList.toggle('show');
                if (sidebarOverlay) {
                    sidebarOverlay.classList.toggle('show');
                }
                
                // Prevent body scroll when sidebar is open on mobile
                document.body.style.overflow = sidebarWrapper.classList.contains('show') ? 'hidden' : '';
            }
        });
    }
    
    // Close sidebar when clicking overlay
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebarWrapper.classList.remove('show');
            sidebarOverlay.classList.remove('show');
            document.body.style.overflow = '';
        });
    }
    
    // Handle window resize - close sidebar on mobile
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992) {
            sidebarWrapper.classList.remove('show');
            if (sidebarOverlay) {
                sidebarOverlay.classList.remove('show');
            }
            document.body.style.overflow = '';
        }
    });
    
    // Restore sidebar state from localStorage
    const savedState = localStorage.getItem('sidebarCollapsed');
    if (savedState === 'true' && window.innerWidth >= 992) {
        sidebarWrapper.classList.add('collapsed');
        if (sidebarToggle) {
            const icon = sidebarToggle.querySelector('i');
            if (icon) icon.className = 'bi bi-chevron-right';
        }
    }
}

// ==========================================================================
// BOOTSTRAP DROPDOWNS
// ==========================================================================
function initDropdowns() {
    // Ensure all dropdowns are properly initialized
    const dropdownTriggerList = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    dropdownTriggerList.forEach(dropdownTriggerEl => {
        // Bootstrap 5 auto-initializes dropdowns, but we ensure proper setup
        if (typeof bootstrap !== 'undefined') {
            // Dropdowns are handled by Bootstrap's auto-init
            // This is just a fallback check
        }
    });
}

// ==========================================================================
// BOOTSTRAP TOOLTIPS
// ==========================================================================
function initTooltips() {
    if (typeof bootstrap !== 'undefined') {
        // Initialize all tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipTriggerList.forEach(tooltipTriggerEl => {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// ==========================================================================
// FORM VALIDATION
// ==========================================================================
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// ==========================================================================
// DELETE CONFIRMATIONS
// ==========================================================================
function initDeleteConfirmations() {
    const deleteButtons = document.querySelectorAll('[data-delete-confirm]');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-delete-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// ==========================================================================
// FLASH MESSAGES AUTO-HIDE
// ==========================================================================
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    
    flashMessages.forEach(message => {
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined') {
                const bsAlert = new bootstrap.Alert(message);
                bsAlert.close();
            } else {
                message.classList.remove('show');
                message.classList.add('fade');
                setTimeout(() => {
                    if (message.parentNode) {
                        message.parentNode.removeChild(message);
                    }
                }, 300);
            }
        }, 5000);
    });
}

// ==========================================================================
// ACTIVE MENU ITEM HIGHLIGHTING
// ==========================================================================
function initActiveNavHighlight() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href) {
            // Remove existing active class
            link.classList.remove('active');
            
            // Check if current path matches or starts with href
            if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
                link.classList.add('active');
            }
        }
    });
}

// ==========================================================================
// SEARCH FUNCTIONALITY
// ==========================================================================
function initSearchHighlight() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput && searchInput.value) {
        const cards = document.querySelectorAll('.job-card');
        cards.forEach(card => {
            const text = card.textContent.toLowerCase();
            if (text.includes(searchInput.value.toLowerCase())) {
                card.style.border = '2px solid #4f46e5';
            }
        });
    }
}

// ==========================================================================
// PHONE NUMBER FORMATTING
// ==========================================================================
function formatPhoneNumber(input) {
    input.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 0) {
            if (value.length <= 3) {
                value = `(${value}`;
            } else if (value.length <= 6) {
                value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
            } else {
                value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
            }
        }
        e.target.value = value;
    });
}

// Initialize phone formatting if exists
const phoneInput = document.querySelector('input[name="phone"]');
if (phoneInput) {
    formatPhoneNumber(phoneInput);
}

// ==========================================================================
// JOB COUNTDOWNS
// ==========================================================================
function initJobCountdowns() {
    const deadlineElements = document.querySelectorAll('[data-deadline]');
    
    deadlineElements.forEach(el => {
        const deadline = new Date(el.dataset.deadline);
        const now = new Date();
        const diff = deadline - now;
        
        if (diff > 0) {
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            el.innerHTML = `<span class="text-warning">${days} days left</span>`;
        } else {
            el.innerHTML = `<span class="text-danger">Expired</span>`;
        }
    });
}

// ==========================================================================
// EXPORT TO CSV
// ==========================================================================
function exportToCSV(data, filename) {
    const csvContent = "data:text/csv;charset=utf-8," 
        + data.map(e => e.join(",")).join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ==========================================================================
// PRINT PAGE
// ==========================================================================
function printPage() {
    window.print();
}

// ==========================================================================
// COPY TO CLIPBOARD
// ==========================================================================
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            alert('Copied to clipboard!');
        }).catch(err => {
            console.error('Failed to copy:', err);
        });
    } else {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            alert('Copied to clipboard!');
        } catch (err) {
            console.error('Failed to copy:', err);
        }
        document.body.removeChild(textarea);
    }
}

// ==========================================================================
// DEBOUNCE FUNCTION
// ==========================================================================
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==========================================================================
// AJAX FORM SUBMISSION HELPERS
// ==========================================================================
function submitFormAsync(form, successUrl) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton ? submitButton.innerHTML : '';
    
    if (submitButton) {
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';
    }
    
    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = successUrl;
        } else {
            throw new Error('Form submission failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
        }
        alert('An error occurred. Please try again.');
    });
}

// ==========================================================================
// CONFIRMATION DIALOG
// ==========================================================================
function confirmAction(message, onConfirm) {
    if (confirm(message)) {
        if (typeof onConfirm === 'function') {
            onConfirm();
        }
    }
}

// ==========================================================================
// STATUS BADGE COLOR HELPERS
// ==========================================================================
function getStatusBadgeClass(status) {
    const statusClasses = {
        'pending': 'bg-warning-subtle text-warning',
        'reviewed': 'bg-info-subtle text-info',
        'accepted': 'bg-success-subtle text-success',
        'rejected': 'bg-danger-subtle text-danger',
        'active': 'bg-success-subtle text-success',
        'closed': 'bg-secondary-subtle text-secondary',
        'draft': 'bg-warning-subtle text-warning'
    };
    return statusClasses[status] || 'bg-secondary-subtle text-secondary';
}

function getStatusIcon(status) {
    const statusIcons = {
        'pending': 'bi-clock',
        'reviewed': 'bi-eye',
        'accepted': 'bi-check-circle',
        'rejected': 'bi-x-circle',
        'active': 'bi-check-circle',
        'closed': 'bi-x-circle',
        'draft': 'bi-file-earmark'
    };
    return statusIcons[status] || 'bi-info-circle';
}

