import os

def create_frontend_project_structure(base_path="frontend"):
    """
    Creates the frontend project structure and populates it with HTML, CSS, and JS files.
    """
    print(f"Creating frontend project structure in: {os.path.abspath(base_path)}")

    # Define the core directories
    dirs = [
        os.path.join(base_path, "css"),
        os.path.join(base_path, "js"),
        os.path.join(base_path, "pages"),
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"Created directory: {d}")

    # Define file contents
    files_content = {
        # Root HTML
        "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ticket Management System</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/auth.css">
</head>
<body class="bg-gray-100 font-sans antialiased">
    <div id="navbar-container"></div>
    <div id="app" class="container mx-auto p-4 max-w-4xl mt-10">
        <!-- Content will be loaded here by JavaScript -->
    </div>
    <div id="message-box" class="fixed bottom-4 right-4 bg-blue-500 text-white p-3 rounded-lg shadow-lg hidden"></div>

    <script src="js/utils.js"></script>
    <script src="js/api.js"></script>
    <script src="js/auth.js"></script>
    <script src="js/main.js"></script>
</body>
</html>
""",
        # CSS Files
        "css/style.css": """/* General styles */
body {
    font-family: 'Inter', sans-serif;
}

/* Utility classes for messages */
.message-success {
    background-color: #4CAF50; /* Green */
}

.message-error {
    background-color: #f44336; /* Red */
}

.message-info {
    background-color: #2196F3; /* Blue */
}
""",
        "css/auth.css": """/* Auth form specific styles */
.auth-container {
    max-width: 400px;
    margin: 50px auto;
    padding: 30px;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid #e0e0e0;
}

.auth-container h2 {
    text-align: center;
    color: #333;
    margin-bottom: 25px;
    font-size: 1.8rem;
    font-weight: 700;
}

.auth-form label {
    display: block;
    margin-bottom: 8px;
    color: #555;
    font-weight: 600;
}

.auth-form input[type="text"],
.auth-form input[type="email"],
.auth-form input[type="password"] {
    width: 100%;
    padding: 12px 15px;
    margin-bottom: 20px;
    border: 1px solid #dcdcdc;
    border-radius: 8px;
    box-sizing: border-box;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.auth-form input[type="text"]:focus,
.auth-form input[type="email"]:focus,
.auth-form input[type="password"]:focus {
    outline: none;
    border-color: #6366f1; /* Tailwind indigo-500 */
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.auth-form button {
    width: 100%;
    padding: 12px 20px;
    background-color: #6366f1; /* Tailwind indigo-600 */
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 600;
    transition: background-color 0.3s ease, transform 0.2s ease;
    box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
}

.auth-form button:hover {
    background-color: #4f46e5; /* Tailwind indigo-700 */
    transform: translateY(-2px);
}

.auth-form button:active {
    transform: translateY(0);
}

.auth-form p {
    text-align: center;
    margin-top: 20px;
    color: #666;
}

.auth-form p a {
    color: #6366f1;
    text-decoration: none;
    font-weight: 600;
    transition: color 0.3s ease;
}

.auth-form p a:hover {
    color: #4f46e5;
    text-decoration: underline;
}
""",
        # JS Files
        "js/utils.js": """// utils.js

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
""",
        "js/api.js": """// api.js

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
""",
        "js/auth.js": """// auth.js

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
""",
        "js/main.js": """// main.js

// Function to load the navigation bar
async function loadNavbar() {
    const navbarContainer = document.getElementById('navbar-container');
    const isLoggedIn = isAuthenticated(); // Check if user is logged in

    let navbarHtml = `
        <nav class="bg-indigo-600 p-4 shadow-md">
            <div class="container mx-auto flex justify-between items-center">
                <a href="#dashboard" class="text-white text-2xl font-bold rounded-md hover:text-indigo-100 transition-colors">TicketMgmt</a>
                <div class="space-x-4">
    `;

    if (isLoggedIn) {
        navbarHtml += `
                    <a href="#dashboard" class="text-white hover:bg-indigo-700 px-3 py-2 rounded-md transition-colors">Dashboard</a>
                    <a href="#tickets" class="text-white hover:bg-indigo-700 px-3 py-2 rounded-md transition-colors">Tickets</a>
                    <a href="#customers" class="text-white hover:bg-indigo-700 px-3 py-2 rounded-md transition-colors">Customers</a>
                    <a href="#engineers" class="text-white hover:bg-indigo-700 px-3 py-2 rounded-md transition-colors">Engineers</a>
                    <button id="logoutButton" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md shadow-md transition-colors">Logout</button>
        `;
    } else {
        navbarHtml += `
                    <a href="#login" class="text-white hover:bg-indigo-700 px-3 py-2 rounded-md transition-colors">Login</a>
                    <a href="#register" class="text-white hover:bg-indigo-700 px-3 py-2 rounded-md transition-colors">Register</a>
        `;
    }

    navbarHtml += `
                </div>
            </div>
        </nav>
    `;
    navbarContainer.innerHTML = navbarHtml;

    // Attach event listener for logout button if it exists
    if (isLoggedIn) {
        const logoutBtn = document.getElementById('logoutButton');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', handleLogout);
        }
    }
}

// Function to handle route changes
async function handleRouteChange() {
    const hash = window.location.hash;
    await loadNavbar(); // Always reload navbar to reflect auth status

    const appContainer = document.getElementById('app');
    appContainer.innerHTML = ''; // Clear previous content

    if (isAuthenticated()) {
        // Authenticated routes
        switch (hash) {
            case '#dashboard':
                await loadPage('pages/dashboard.html');
                setupDashboardPage(); // Call function to set up dashboard interactions
                break;
            case '#tickets':
                await loadPage('pages/tickets.html');
                setupTicketsPage(); // Call function to set up tickets interactions
                break;
            case '#customers':
                await loadPage('pages/customers.html');
                setupCustomersPage(); // Call function to set up customers interactions
                break;
            case '#engineers':
                await loadPage('pages/engineers.html');
                setupEngineersPage(); // Call function to set up engineers interactions
                break;
            default:
                // Default authenticated route
                window.location.hash = '#dashboard';
                break;
        }
    } else {
        // Unauthenticated routes
        switch (hash) {
            case '#register':
                await loadPage('pages/register.html');
                document.getElementById('registerForm').addEventListener('submit', handleRegister);
                break;
            case '#login':
            case '': // Default to login if no hash
                await loadPage('pages/login.html');
                document.getElementById('loginForm').addEventListener('submit', handleLogin);
                break;
            default:
                // If trying to access an authenticated route without login, redirect to login
                window.location.hash = '#login';
                break;
        }
    }
}

// Event listener for hash changes
window.addEventListener('hashchange', handleRouteChange);

// Initial page load
document.addEventListener('DOMContentLoaded', handleRouteChange);


// --- Page-specific setup functions (to be implemented in main.js or separate files) ---

// Dashboard Page Setup
async function setupDashboardPage() {
    const usernameDisplay = document.getElementById('usernameDisplay');
    if (usernameDisplay) {
        // In a real app, you'd decode the JWT or fetch user info to get the username
        // For simplicity, we'll just show a generic welcome or ask user to refresh
        usernameDisplay.textContent = localStorage.getItem('loggedInUsername') || 'User';
    }

    // Example: Fetch and display some summary data
    try {
        const tickets = await getAllTickets();
        document.getElementById('totalTickets').textContent = tickets.length;

        const openTickets = tickets.filter(t => t.ticketStatus === 'OPEN').length;
        document.getElementById('openTickets').textContent = openTickets;
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
}

// Tickets Page Setup
async function setupTicketsPage() {
    const ticketsTableBody = document.getElementById('ticketsTableBody');
    const createTicketForm = document.getElementById('createTicketForm');

    if (createTicketForm) {
        createTicketForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const customerName = document.getElementById('ticketCustomerName').value;
            const issue = document.getElementById('ticketIssue').value;
            const priority = document.getElementById('ticketPriority').value;

            try {
                const newTicket = await createTicket(customerName, issue, priority);
                showMessage(`Ticket created with ID: ${newTicket.id}`, 'success');
                loadTickets(); // Refresh the list
                createTicketForm.reset();
            } catch (error) {
                console.error('Error creating ticket:', error);
            }
        });
    }

    async function loadTickets() {
        if (!ticketsTableBody) return; // Ensure element exists
        ticketsTableBody.innerHTML = '<tr><td colspan="6" class="text-center py-4">Loading tickets...</td></tr>';
        try {
            const tickets = await getAllTickets();
            ticketsTableBody.innerHTML = ''; // Clear loading message
            if (tickets.length === 0) {
                ticketsTableBody.innerHTML = '<tr><td colspan="6" class="text-center py-4">No tickets found.</td></tr>';
                return;
            }
            tickets.forEach(ticket => {
                const row = document.createElement('tr');
                row.className = 'bg-white border-b hover:bg-gray-50';
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${ticket.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${ticket.customer ? ticket.customer.name : 'N/A'}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${ticket.issueDescription}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${ticket.ticketStatus}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${ticket.priority}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        ${ticket.assignedEngineer ? ticket.assignedEngineer.name : 'Unassigned'}
                        <div class="flex space-x-2 mt-2">
                            <button onclick="handleAssignTicket(${ticket.id})" class="bg-blue-500 hover:bg-blue-600 text-white text-xs px-2 py-1 rounded-md">Assign</button>
                            <button onclick="handleUnassignTicket(${ticket.id})" class="bg-yellow-500 hover:bg-yellow-600 text-white text-xs px-2 py-1 rounded-md">Unassign</button>
                            <button onclick="showUploadModal(${ticket.id})" class="bg-green-500 hover:bg-green-600 text-white text-xs px-2 py-1 rounded-md">Upload File</button>
                            <button onclick="showFilesForTicket(${ticket.id})" class="bg-purple-500 hover:bg-purple-600 text-white text-xs px-2 py-1 rounded-md">View Files</button>
                        </div>
                    </td>
                `;
                ticketsTableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading tickets:', error);
            ticketsTableBody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-red-500">Failed to load tickets.</td></tr>';
        }
    }

    loadTickets();
}

// Global functions for ticket actions (called from inline onclick)
async function handleAssignTicket(ticketId) {
    const engineerId = prompt('Enter Engineer ID to assign:');
    if (engineerId) {
        try {
            await assignTicket(ticketId, parseInt(engineerId));
            showMessage(`Ticket ${ticketId} assigned successfully!`, 'success');
            setupTicketsPage(); // Refresh list
        } catch (error) {
            console.error('Error assigning ticket:', error);
        }
    }
}

async function handleUnassignTicket(ticketId) {
    if (confirm(`Are you sure you want to unassign engineer from Ticket ${ticketId}?`)) {
        try {
            await unassignTicket(ticketId);
            showMessage(`Ticket ${ticketId} unassigned successfully!`, 'success');
            setupTicketsPage(); // Refresh list
        } catch (error) {
            console.error('Error unassigning ticket:', error);
        }
    }
}

// File Upload Modal
function showUploadModal(ticketId) {
    const modal = document.createElement('div');
    modal.id = 'uploadModal';
    modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white p-6 rounded-lg shadow-xl w-96">
            <h3 class="text-lg font-bold mb-4">Upload File for Ticket ${ticketId}</h3>
            <input type="file" id="fileInput" class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"/>
            <div class="flex justify-end mt-4 space-x-2">
                <button id="uploadFileBtn" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md">Upload</button>
                <button id="cancelUploadBtn" class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-md">Cancel</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    document.getElementById('uploadFileBtn').addEventListener('click', async () => {
        const fileInput = document.getElementById('fileInput');
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            try {
                await uploadFile(ticketId, file);
                showMessage('File uploaded successfully!', 'success');
                modal.remove();
            } catch (error) {
                console.error('File upload failed:', error);
            }
        } else {
            showMessage('Please select a file to upload.', 'info');
        }
    });

    document.getElementById('cancelUploadBtn').addEventListener('click', () => {
        modal.remove();
    });
}

// View Files Modal
async function showFilesForTicket(ticketId) {
    const modal = document.createElement('div');
    modal.id = 'viewFilesModal';
    modal.className = 'fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="bg-white p-6 rounded-lg shadow-xl w-96">
            <h3 class="text-lg font-bold mb-4">Files for Ticket ${ticketId}</h3>
            <ul id="fileList" class="list-disc pl-5">
                <li>Loading files...</li>
            </ul>
            <div class="flex justify-end mt-4">
                <button id="closeFilesModalBtn" class="bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-md">Close</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);

    const fileList = document.getElementById('fileList');
    try {
        const files = await getFilesForTicket(ticketId);
        fileList.innerHTML = ''; // Clear loading message
        if (files.length === 0) {
            fileList.innerHTML = '<li>No files attached.</li>';
        } else {
            files.forEach(filePath => {
                const listItem = document.createElement('li');
                // Extract filename from path for display
                const fileName = filePath.split('\\').pop().split('/').pop();
                listItem.textContent = fileName;
                fileList.appendChild(listItem);
            });
        }
    } catch (error) {
        console.error('Error fetching files:', error);
        fileList.innerHTML = '<li class="text-red-500">Failed to load files.</li>';
    }

    document.getElementById('closeFilesModalBtn').addEventListener('click', () => {
        modal.remove();
    });
}


// Customers Page Setup
async function setupCustomersPage() {
    const customersTableBody = document.getElementById('customersTableBody');
    const createCustomerForm = document.getElementById('createCustomerForm');

    if (createCustomerForm) {
        createCustomerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const name = document.getElementById('customerName').value;
            const email = document.getElementById('customerEmail').value;
            const phoneNumber = document.getElementById('customerPhone').value;
            const companyName = document.getElementById('customerCompany').value;

            try {
                const newCustomer = await createCustomer(name, email, phoneNumber, companyName);
                showMessage(`Customer ${newCustomer.name} created!`, 'success');
                loadCustomers(); // Refresh the list
                createCustomerForm.reset();
            } catch (error) {
                console.error('Error creating customer:', error);
            }
        });
    }

    async function loadCustomers() {
        if (!customersTableBody) return;
        customersTableBody.innerHTML = '<tr><td colspan="5" class="text-center py-4">Loading customers...</td></tr>';
        try {
            const customers = await getAllCustomers();
            customersTableBody.innerHTML = '';
            if (customers.length === 0) {
                customersTableBody.innerHTML = '<tr><td colspan="5" class="text-center py-4">No customers found.</td></tr>';
                return;
            }
            customers.forEach(customer => {
                const row = document.createElement('tr');
                row.className = 'bg-white border-b hover:bg-gray-50';
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${customer.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${customer.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${customer.email}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${customer.phoneNumber}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${customer.companyName}</td>
                `;
                customersTableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading customers:', error);
            customersTableBody.innerHTML = '<tr><td colspan="5" class="text-center py-4 text-red-500">Failed to load customers.</td></tr>';
        }
    }

    loadCustomers();
}

// Engineers Page Setup
async function setupEngineersPage() {
    const engineersTableBody = document.getElementById('engineersTableBody');
    const createEngineerForm = document.getElementById('createEngineerForm');

    if (createEngineerForm) {
        createEngineerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const name = document.getElementById('engineerName').value;
            const email = document.getElementById('engineerEmail').value;
            const designation = document.getElementById('engineerDesignation').value;

            try {
                const newEngineer = await createEngineer(name, email, designation);
                showMessage(`Engineer ${newEngineer.name} created!`, 'success');
                loadEngineers(); // Refresh the list
                createEngineerForm.reset();
            } catch (error) {
                console.error('Error creating engineer:', error);
            }
        });
    }

    async function loadEngineers() {
        if (!engineersTableBody) return;
        engineersTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4">Loading engineers...</td></tr>';
        try {
            const engineers = await getAllEngineers();
            engineersTableBody.innerHTML = '';
            if (engineers.length === 0) {
                engineersTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4">No engineers found.</td></tr>';
                return;
            }
            engineers.forEach(engineer => {
                const row = document.createElement('tr');
                row.className = 'bg-white border-b hover:bg-gray-50';
                row.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">${engineer.id}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${engineer.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${engineer.email}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${engineer.designation}</td>
                `;
                engineersTableBody.appendChild(row);
            });
        } catch (error) {
            console.error('Error loading engineers:', error);
            engineersTableBody.innerHTML = '<tr><td colspan="4" class="text-center py-4 text-red-500">Failed to load engineers.</td></tr>';
        }
    }

    loadEngineers();
}
""",
        "pages/login.html": """<div class="auth-container">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Login</h2>
    <form id="loginForm" class="auth-form">
        <div class="mb-4">
            <label for="loginUsername" class="block text-gray-700 text-sm font-bold mb-2">Username:</label>
            <input type="text" id="loginUsername" name="username" class="shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
        </div>
        <div class="mb-6">
            <label for="loginPassword" class="block text-gray-700 text-sm font-bold mb-2">Password:</label>
            <input type="password" id="loginPassword" name="password" class="shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
        </div>
        <div class="flex items-center justify-between">
            <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:shadow-outline transition-all duration-200 ease-in-out transform hover:-translate-y-1">
                Sign In
            </button>
        </div>
        <p class="text-center text-gray-600 text-sm mt-6">
            Don't have an account? <a href="#register" class="font-bold text-indigo-600 hover:text-indigo-800">Register here</a>
        </p>
    </form>
</div>
""",
        "pages/register.html": """<div class="auth-container">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Register</h2>
    <form id="registerForm" class="auth-form">
        <div class="mb-4">
            <label for="registerUsername" class="block text-gray-700 text-sm font-bold mb-2">Username:</label>
            <input type="text" id="registerUsername" name="username" class="shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
        </div>
        <div class="mb-4">
            <label for="registerEmail" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
            <input type="email" id="registerEmail" name="email" class="shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
        </div>
        <div class="mb-4">
            <label for="registerPassword" class="block text-gray-700 text-sm font-bold mb-2">Password:</label>
            <input type="password" id="registerPassword" name="password" class="shadow appearance-none border rounded-lg w-full py-3 px-4 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
        </div>
        <div class="mb-6">
            <label for="registerRole" class="block text-gray-700 text-sm font-bold mb-2">Role:</label>
            <select id="registerRole" name="role" class="shadow border rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500">
                <option value="ROLE_CUSTOMER">Customer</option>
                <option value="ROLE_ENGINEER">Engineer</option>
            </select>
        </div>
        <div class="flex items-center justify-between">
            <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:shadow-outline transition-all duration-200 ease-in-out transform hover:-translate-y-1">
                Register
            </button>
        </div>
        <p class="text-center text-gray-600 text-sm mt-6">
            Already have an account? <a href="#login" class="font-bold text-indigo-600 hover:text-indigo-800">Login here</a>
        </p>
    </form>
</div>
""",
        "pages/dashboard.html": """<div class="bg-white p-6 rounded-lg shadow-xl">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Welcome to Your Dashboard, <span id="usernameDisplay" class="text-indigo-600">User</span>!</h2>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Card 1: Total Tickets -->
        <div class="bg-blue-100 p-5 rounded-lg shadow-md flex items-center justify-between">
            <div>
                <h3 class="text-lg font-semibold text-blue-800">Total Tickets</h3>
                <p id="totalTickets" class="text-4xl font-bold text-blue-600 mt-2">0</p>
            </div>
            <svg class="w-12 h-12 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M12 5a3 3 0 11-6 0 3 3 0 016 0zM15 12a3 3 0 11-6 0 3 3 0 016 0zM15 19a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
        </div>

        <!-- Card 2: Open Tickets -->
        <div class="bg-yellow-100 p-5 rounded-lg shadow-md flex items-center justify-between">
            <div>
                <h3 class="text-lg font-semibold text-yellow-800">Open Tickets</h3>
                <p id="openTickets" class="text-4xl font-bold text-yellow-600 mt-2">0</p>
            </div>
            <svg class="w-12 h-12 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        </div>

        <!-- Card 3: Quick Actions -->
        <div class="bg-green-100 p-5 rounded-lg shadow-md flex flex-col justify-center items-center">
            <h3 class="text-lg font-semibold text-green-800 mb-3">Quick Actions</h3>
            <div class="flex flex-wrap gap-3">
                <a href="#tickets" class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-md shadow-sm transition-colors">View Tickets</a>
                <a href="#customers" class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-md shadow-sm transition-colors">View Customers</a>
                <a href="#engineers" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md shadow-sm transition-colors">View Engineers</a>
            </div>
        </div>
    </div>

    <div class="mt-8">
        <h3 class="text-2xl font-bold text-gray-800 mb-4">Recent Activity</h3>
        <p class="text-gray-600">No recent activity to display yet. Create a ticket to see updates!</p>
        <!-- You can dynamically load recent audit logs here -->
    </div>
</div>
""",
        "pages/tickets.html": """<div class="bg-white p-6 rounded-lg shadow-xl">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Manage Tickets</h2>

    <!-- Create New Ticket Form -->
    <div class="mb-8 p-6 bg-gray-50 rounded-lg shadow-inner">
        <h3 class="text-2xl font-bold text-gray-700 mb-4">Create New Ticket</h3>
        <form id="createTicketForm" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label for="ticketCustomerName" class="block text-gray-700 text-sm font-bold mb-2">Customer Name:</label>
                <input type="text" id="ticketCustomerName" name="customerName" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
            </div>
            <div>
                <label for="ticketIssue" class="block text-gray-700 text-sm font-bold mb-2">Issue Description:</label>
                <input type="text" id="ticketIssue" name="issue" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
            </div>
            <div class="md:col-span-2">
                <label for="ticketPriority" class="block text-gray-700 text-sm font-bold mb-2">Priority:</label>
                <select id="ticketPriority" name="priority" class="shadow border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500">
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                    <option value="CRITICAL">CRITICAL</option>
                </select>
            </div>
            <div class="md:col-span-2 flex justify-end">
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-all duration-200 ease-in-out transform hover:-translate-y-1">
                    Create Ticket
                </button>
            </div>
        </form>
    </div>

    <!-- Tickets List -->
    <h3 class="text-2xl font-bold text-gray-700 mb-4">All Tickets</h3>
    <div class="overflow-x-auto relative shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left text-gray-500">
            <thead class="text-xs text-gray-700 uppercase bg-gray-200">
                <tr>
                    <th scope="col" class="py-3 px-6">ID</th>
                    <th scope="col" class="py-3 px-6">Customer</th>
                    <th scope="col" class="py-3 px-6">Issue</th>
                    <th scope="col" class="py-3 px-6">Status</th>
                    <th scope="col" class="py-3 px-6">Priority</th>
                    <th scope="col" class="py-3 px-6">Actions</th>
                </tr>
            </thead>
            <tbody id="ticketsTableBody">
                <!-- Tickets will be loaded here by JavaScript -->
            </tbody>
        </table>
    </div>
</div>
""",
        "pages/customers.html": """<div class="bg-white p-6 rounded-lg shadow-xl">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Manage Customers</h2>

    <!-- Create New Customer Form -->
    <div class="mb-8 p-6 bg-gray-50 rounded-lg shadow-inner">
        <h3 class="text-2xl font-bold text-gray-700 mb-4">Add New Customer</h3>
        <form id="createCustomerForm" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label for="customerName" class="block text-gray-700 text-sm font-bold mb-2">Name:</label>
                <input type="text" id="customerName" name="name" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
            </div>
            <div>
                <label for="customerEmail" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
                <input type="email" id="customerEmail" name="email" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
            </div>
            <div>
                <label for="customerPhone" class="block text-gray-700 text-sm font-bold mb-2">Phone Number:</label>
                <input type="text" id="customerPhone" name="phoneNumber" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500">
            </div>
            <div>
                <label for="customerCompany" class="block text-gray-700 text-sm font-bold mb-2">Company Name:</label>
                <input type="text" id="customerCompany" name="companyName" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500">
            </div>
            <div class="md:col-span-2 flex justify-end">
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-all duration-200 ease-in-out transform hover:-translate-y-1">
                    Add Customer
                </button>
            </div>
        </form>
    </div>

    <!-- Customers List -->
    <h3 class="text-2xl font-bold text-gray-700 mb-4">All Customers</h3>
    <div class="overflow-x-auto relative shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left text-gray-500">
            <thead class="text-xs text-gray-700 uppercase bg-gray-200">
                <tr>
                    <th scope="col" class="py-3 px-6">ID</th>
                    <th scope="col" class="py-3 px-6">Name</th>
                    <th scope="col" class="py-3 px-6">Email</th>
                    <th scope="col" class="py-3 px-6">Phone</th>
                    <th scope="col" class="py-3 px-6">Company</th>
                </tr>
            </thead>
            <tbody id="customersTableBody">
                <!-- Customers will be loaded here by JavaScript -->
            </tbody>
        </table>
    </div>
</div>
""",
        "pages/engineers.html": """<div class="bg-white p-6 rounded-lg shadow-xl">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Manage Engineers</h2>

    <!-- Create New Engineer Form -->
    <div class="mb-8 p-6 bg-gray-50 rounded-lg shadow-inner">
        <h3 class="text-2xl font-bold text-gray-700 mb-4">Add New Engineer</h3>
        <form id="createEngineerForm" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label for="engineerName" class="block text-gray-700 text-sm font-bold mb-2">Name:</label>
                <input type="text" id="engineerName" name="name" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
            </div>
            <div>
                <label for="engineerEmail" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
                <input type="email" id="engineerEmail" name="email" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500" required>
            </div>
            <div class="md:col-span-2">
                <label for="engineerDesignation" class="block text-gray-700 text-sm font-bold mb-2">Designation:</label>
                <input type="text" id="engineerDesignation" name="designation" class="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:border-indigo-500">
            </div>
            <div class="md:col-span-2 flex justify-end">
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:shadow-outline transition-all duration-200 ease-in-out transform hover:-translate-y-1">
                    Add Engineer
                </button>
            </div>
        </form>
    </div>

    <!-- Engineers List -->
    <h3 class="text-2xl font-bold text-gray-700 mb-4">All Engineers</h3>
    <div class="overflow-x-auto relative shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left text-gray-500">
            <thead class="text-xs text-gray-700 uppercase bg-gray-200">
                <tr>
                    <th scope="col" class="py-3 px-6">ID</th>
                    <th scope="col" class="py-3 px-6">Name</th>
                    <th scope="col" class="py-3 px-6">Email</th>
                    <th scope="col" class="py-3 px-6">Designation</th>
                </tr>
            </thead>
            <tbody id="engineersTableBody">
                <!-- Engineers will be loaded here by JavaScript -->
            </tbody>
        </table>
    </div>
</div>
""",
        "pages/notfound.html": """<div class="flex flex-col items-center justify-center min-h-[60vh]">
    <h1 class="text-6xl font-bold text-gray-800 mb-4">404</h1>
    <p class="text-xl text-gray-600 mb-8">Page Not Found</p>
    <a href="#dashboard" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg focus:outline-none focus:shadow-outline transition-all duration-200 ease-in-out transform hover:-translate-y-1">
        Go to Dashboard
    </a>
</div>
"""
    }

    for file_path, content in files_content.items():
        full_path = os.path.join(base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        print(f"Created/Updated file: {full_path}")

    print("\nFrontend project structure and files created successfully!")

if __name__ == "__main__":
    create_frontend_project_structure()
