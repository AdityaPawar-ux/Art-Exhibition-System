// Art Exhibition System - Basic Interactions (Vanilla JS)
// Enhances UX without dependencies. Loads after DOM.

// Global Delete Confirmation (Themed Alert - Replaces Inline onclick)
function confirmDelete(itemType = 'item') {
    return confirm(`Are you sure you want to delete this ${itemType}? This action cannot be undone.`);
}

// Example Usage in HTML: onclick="return confirmDelete('Painting')" or onclick="return confirmDelete('Contact')"

// Smooth Scrolling for Anchor Links (e.g., Navbar to Sections)
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for all internal links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

        // Form Submit Loading Indicator (Subtle Spinner on Buttons)
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = 'Saving... <span style="font-size: 12px;">⏳</span>'; // Simple spinner emoji
                submitBtn.disabled = true;
                // Reset on page unload (handled by browser reload)
            }
        });
    });

    // Admin Edit Form Enhancements (e.g., Auto-Focus on First Input)
    const editForms = document.querySelectorAll('form[action*="/edit_painting"]');
    editForms.forEach(form => {
        const firstInput = form.querySelector('input[type="text"]');
        if (firstInput) {
            firstInput.focus(); // Auto-focus title field on load
        }
    });

    // Flash Message Auto-Hide (After 3s - For Better UX)
    const flashMessages = document.querySelectorAll('.flash-message, .flash');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s ease-out';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500); // Remove after fade
        }, 3000);
    });
});

// Polyfill for Older Browsers (Optional - Ensures Compatibility)
if (!Element.prototype.matches) {
    Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector;
}

// End of Script - No Conflicts with CSS Animations
console.log('Art Exhibition JS Loaded Successfully! 🚀');