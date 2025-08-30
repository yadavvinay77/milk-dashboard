// Add confirmation for all destructive actions
document.addEventListener('DOMContentLoaded', () => {
    // Confirmation for delete actions
    const deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteForms.forEach(form => {
        form.onsubmit = () => {
            const message = form.getAttribute('data-confirm') || 'Are you sure?';
            return confirm(message);
        };
    });

    // Add back button functionality
    const addBackButton = () => {
        const contentDiv = document.querySelector('.container.my-4');
        if (contentDiv && !document.querySelector('.back-button')) {
            const backBtn = document.createElement('a');
            backBtn.className = 'btn btn-secondary mb-3 back-button';
            backBtn.innerHTML = '&larr; Back';
            backBtn.href = 'javascript:history.back()';
            contentDiv.insertBefore(backBtn, contentDiv.firstChild);
        }
    };
    
    addBackButton();
});

// Mobile responsive improvements
function checkMobile() {
    if (window.innerWidth < 768) {
        document.body.classList.add('mobile-view');
    } else {
        document.body.classList.remove('mobile-view');
    }
}

window.addEventListener('resize', checkMobile);
checkMobile();