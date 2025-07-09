// utils.js

/**
 * Displays a message in a dedicated message box.
 * @param {string} message - The message to display.
 * @param {string} type - The type of message ('success', 'error', 'info').
 */
function showMessage(message, type = 'info') {
    const messageBox = document.getElementById('message-box');
    messageBox.textContent = message;
    messageBox.className = `fixed bottom-4 right-4 p-3 rounded-lg shadow-lg transition-all duration-300 ${type === 'success' ? 'bg-green-500' : type === 'error' ? 'bg-red-500' : 'bg-blue-500'} text-white block`;

    // Automatically hide the message after 3 seconds
    setTimeout(() => {
        messageBox.classList.add('hidden');
    }, 3000);
}

/**
 * Loads an HTML file into a specified container.
 * @param {string} filePath - The path to the HTML file.
 * @param {string} containerId - The ID of the HTML element to load content into.
 * @returns {Promise<void>}
 */
async function loadPage(filePath, containerId = 'app') {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const html = await response.text();
        document.getElementById(containerId).innerHTML = html;
    } catch (error) {
        console.error('Failed to load page:', error);
        showMessage(`Failed to load page: ${filePath}`, 'error');
        // Optionally load a 404 page
        if (filePath !== 'pages/notfound.html') {
            loadPage('pages/notfound.html');
        }
    }
}

/**
 * Saves a JWT token to local storage.
 * @param {string} token - The JWT token to save.
 */
function saveToken(token) {
    localStorage.setItem('jwtToken', token);
}

/**
 * Retrieves a JWT token from local storage.
 * @returns {string|null} The JWT token or null if not found.
 */
function getToken() {
    return localStorage.getItem('jwtToken');
}

/**
 * Removes the JWT token from local storage.
 */
function removeToken() {
    localStorage.removeItem('jwtToken');
}

/**
 * Checks if a user is authenticated by checking for a JWT token.
 * @returns {boolean} True if a token exists, false otherwise.
 */
function isAuthenticated() {
    return getToken() !== null;
}
