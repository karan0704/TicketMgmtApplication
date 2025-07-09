// api.js

const BASE_URL = 'http://localhost:8080/api'; // Your Spring Boot backend URL

/**
 * Generic function to make authenticated API requests.
 * @param {string} endpoint - The API endpoint (e.g., '/tickets').
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE).
 * @param {object} [body=null] - Request body for POST/PUT requests.
 * @returns {Promise<object>} The JSON response from the API.
 */
async function apiRequest(endpoint, method = 'GET', body = null) {
    const token = getToken(); // Get JWT token from utils.js
    const headers = {
        'Content-Type': 'application/json',
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`; // Add Authorization header
    }

    const config = {
        method: method,
        headers: headers,
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, config);

        if (response.status === 401 || response.status === 403) {
            // Handle unauthorized/forbidden access, e.g., redirect to login
            showMessage('Session expired or unauthorized. Please log in again.', 'error');
            removeToken();
            window.location.hash = '#login';
            return; // Stop further processing
        }

        const data = await response.json();

        if (!response.ok) {
            // If response is not OK (e.g., 400, 500), throw an error with the backend message
            const errorMessage = data.error || 'Something went wrong';
            throw new Error(errorMessage);
        }

        return data;
    } catch (error) {
        console.error(`API Error (${endpoint}):`, error);
        showMessage(error.message || 'Network error or API is down.', 'error');
        throw error; // Re-throw to be caught by the calling function
    }
}

// --- Specific API functions ---

// Auth
async function loginUser(username, password) {
    return apiRequest('/auth/login', 'POST', { username, password });
}

async function registerUser(username, email, password, role) {
    return apiRequest('/auth/register', 'POST', { username, email, password, role });
}

// Tickets
async function getAllTickets() {
    return apiRequest('/tickets/all', 'GET');
}

async function createTicket(customerName, issue, priority) {
    return apiRequest('/tickets/create', 'POST', { customerName, issue, priority });
}

async function assignTicket(ticketId, engineerId) {
    return apiRequest(`/tickets/${ticketId}/assign/${engineerId}`, 'POST');
}

async function unassignTicket(ticketId) {
    return apiRequest(`/tickets/${ticketId}/unassign`, 'POST');
}

// Customers
async function getAllCustomers() {
    return apiRequest('/customers', 'GET');
}

async function createCustomer(name, email, phoneNumber, companyName) {
    return apiRequest('/customers', 'POST', { name, email, phoneNumber, companyName });
}

// Engineers
async function getAllEngineers() {
    return apiRequest('/engineers', 'GET');
}

async function createEngineer(name, email, designation) {
    return apiRequest('/engineers', 'POST', { name, email, designation });
}

// Files
async function uploadFile(ticketId, file) {
    const formData = new FormData();
    formData.append('file', file);

    const token = getToken();
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    try {
        const response = await fetch(`${BASE_URL}/files/upload/${ticketId}`, {
            method: 'POST',
            headers: headers, // No 'Content-Type' header here; browser sets it for FormData
            body: formData,
        });

        if (response.status === 401 || response.status === 403) {
            showMessage('Session expired or unauthorized. Please log in again.', 'error');
            removeToken();
            window.location.hash = '#login';
            return;
        }

        const textResponse = await response.text(); // File upload might return plain text
        if (!response.ok) {
            throw new Error(textResponse || 'File upload failed');
        }
        return { message: textResponse }; // Wrap in an object for consistency
    } catch (error) {
        console.error('File Upload Error (' + ticketId + '):', error);
        showMessage(error.message || 'Network error during file upload.', 'error');
        throw error;
    }
}

async function getFilesForTicket(ticketId) {
    return apiRequest(`/files/ticket/${ticketId}`, 'GET');
}
