// utils.js
// Contains utility functions for displaying messages and loading indicators.

const messageBox = document.getElementById('message-box');
const loadingSpinner = document.getElementById('loading-spinner');

/**
 * Displays a temporary message to the user.
 * @param {string} text - The message text.
 * @param {'success'|'error'} type - The type of message (determines color).
 */
function showMessage(text, type = 'success') {
    messageBox.textContent = text;
    messageBox.classList.remove('hidden', 'bg-green-500', 'bg-red-500');
    if (type === 'success') {
        messageBox.classList.add('bg-green-500');
    } else {
        messageBox.classList.add('bg-red-500');
    }
    messageBox.style.display = 'block'; // Ensure it's visible

    setTimeout(() => {
        messageBox.classList.add('hidden');
        messageBox.style.display = 'none'; // Hide after timeout
    }, 3000); // Hide after 3 seconds
}

/**
 * Shows or hides the global loading spinner.
 * @param {boolean} isLoading - True to show, false to hide.
 */
function setLoading(isLoading) {
    if (isLoading) {
        loadingSpinner.classList.remove('hidden');
        loadingSpinner.style.display = 'flex'; // Use flex to center content
    } else {
        loadingSpinner.classList.add('hidden');
        loadingSpinner.style.display = 'none';
    }
}
