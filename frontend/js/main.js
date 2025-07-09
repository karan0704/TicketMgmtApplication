// main.js

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
                const fileName = filePath.split('\').pop().split('/').pop();
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
