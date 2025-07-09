// app.js
// Main application logic for navigation and initialization.

// Get all view sections
const viewSections = document.querySelectorAll('.view-section');

/**
 * Shows a specific view and hides all others.
 * @param {string} viewId - The ID of the view section to show (e.g., 'home-view').
 */
function showView(viewId) {
    viewSections.forEach(section => {
        if (section.id === viewId) {
            section.classList.remove('hidden');
        } else {
            section.classList.add('hidden');
        }
    });

    // Perform initial data fetch/render when navigating to a list view
    if (viewId === 'customer-list-view') {
        fetchAndRenderCustomers();
    } else if (viewId === 'engineer-list-view') {
        fetchAndRenderEngineers();
    } else if (viewId === 'ticket-list-view') {
        fetchAndRenderTickets();
    }
}

// --- Navigation Button Event Listeners ---
document.getElementById('nav-home').addEventListener('click', () => showView('home-view'));
document.getElementById('nav-customers').addEventListener('click', () => showView('customer-list-view'));
document.getElementById('nav-engineers').addEventListener('click', () => showView('engineer-list-view'));
document.getElementById('nav-tickets').addEventListener('click', () => showView('ticket-list-view'));

// --- Home Page Button Event Listeners ---
document.getElementById('home-manage-customers').addEventListener('click', () => showView('customer-list-view'));
document.getElementById('home-manage-engineers').addEventListener('click', () => showView('engineer-list-view'));
document.getElementById('home-manage-tickets').addEventListener('click', () => showView('ticket-list-view'));


// Initialize the application by showing the home view when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    showView('home-view');
});
