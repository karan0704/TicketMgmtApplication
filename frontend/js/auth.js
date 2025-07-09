// auth.js

/**
 * Handles user login.
 * @param {Event} event - The form submission event.
 */
async function handleLogin(event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const data = await loginUser(username, password);
        if (data && data.token) {
            saveToken(data.token); // Save the JWT token
            // Store username in local storage for display on dashboard
            localStorage.setItem('loggedInUsername', data.username);
            showMessage('Login successful!', 'success');
            window.location.hash = '#dashboard'; // Redirect to dashboard
        } else {
            showMessage(data.message || 'Login failed. Please check your credentials.', 'error');
        }
    } catch (error) {
        // Error already handled by apiRequest, just log or re-throw if needed
        console.error('Login error:', error);
    }
}

/**
 * Handles user registration.
 * @param {Event} event - The form submission event.
 */
async function handleRegister(event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const role = document.getElementById('registerRole').value; // Get selected role

    try {
        const data = await registerUser(username, email, password, role);
        if (data) {
            showMessage('Registration successful! Please log in.', 'success');
            window.location.hash = '#login'; // Redirect to login page
        }
    } catch (error) {
        console.error('Registration error:', error);
    }
}

/**
 * Handles user logout.
 */
function handleLogout() {
    removeToken(); // Remove token from local storage
    localStorage.removeItem('loggedInUsername'); // Clear stored username
    showMessage('Logged out successfully!', 'info');
    window.location.hash = '#login'; // Redirect to login page
}
