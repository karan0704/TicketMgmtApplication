import os

def create_frontend_files():
    """
    Creates the frontend directory structure and populates it with HTML, CSS, and JS files.
    """
    base_dir = "frontend"
    js_dir = os.path.join(base_dir, "js")
    modules_dir = os.path.join(js_dir, "modules")
    css_dir = os.path.join(base_dir, "css")

    # Create directories
    os.makedirs(modules_dir, exist_ok=True)
    os.makedirs(css_dir, exist_ok=True)

    # --- index.html content ---
    index_html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ticket Management System</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-ticket-alt"></i> Ticket Management System</h1>
            <div class="nav-tabs">
                <button class="nav-tab active" onclick="App.Handlers.showTab('dashboard')">
                    <i class="fas fa-tachometer-alt"></i> Dashboard
                </button>
                <button class="nav-tab" onclick="App.Handlers.showTab('customers')">
                    <i class="fas fa-users"></i> Customers
                </button>
                <button class="nav-tab" onclick="App.Handlers.showTab('engineers')">
                    <i class="fas fa-user-tie"></i> Engineers
                </button>
                <button class="nav-tab" onclick="App.Handlers.showTab('tickets')">
                    <i class="fas fa-ticket-alt"></i> Tickets
                </button>
                <button class="nav-tab" onclick="App.Handlers.showTab('files')">
                    <i class="fas fa-file-upload"></i> Files
                </button>
            </div>
        </div>

        <div class="alert alert-success" id="successAlert"></div>
        <div class="alert alert-error" id="errorAlert"></div>

        <!-- Dashboard Tab -->
        <div id="dashboard" class="tab-content active">
            <div class="two-column">
                <div class="card">
                    <h3><i class="fas fa-chart-bar"></i> Statistics</h3>
                    <div id="statsContainer">
                        <div class="loading">
                            <div class="spinner"></div>
                            Loading statistics...
                        </div>
                    </div>
                </div>
                <div class="card">
                    <h3><i class="fas fa-clock"></i> Recent Activity</h3>
                    <div id="recentActivity">
                        <div class="loading">
                            <div class="spinner"></div>
                            Loading recent activity...
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Customers Tab -->
        <div id="customers" class="tab-content">
            <div class="two-column">
                <div class="card">
                    <h3><i class="fas fa-user-plus"></i> Add Customer</h3>
                    <form id="customerForm">
                        <div class="form-group">
                            <label for="customerName">Name *</label>
                            <input type="text" id="customerName" name="name" required>
                            <div class="error-message" id="customerNameError"></div>
                        </div>
                        <div class="form-group">
                            <label for="customerEmail">Email *</label>
                            <input type="email" id="customerEmail" name="email" required>
                            <div class="error-message" id="customerEmailError"></div>
                        </div>
                        <div class="form-group">
                            <label for="customerPhone">Phone Number</label>
                            <input type="tel" id="customerPhone" name="phoneNumber">
                            <div class="error-message" id="customerPhoneError"></div>
                        </div>
                        <div class="form-group">
                            <label for="customerCompany">Company Name *</label>
                            <input type="text" id="customerCompany" name="companyName" required>
                            <div class="error-message" id="customerCompanyError"></div>
                        </div>
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-plus"></i> Add Customer
                        </button>
                    </form>
                </div>
                <div class="card">
                    <h3><i class="fas fa-users"></i> Customer List</h3>
                    <div id="customersList">
                        <div class="loading">
                            <div class="spinner"></div>
                            Loading customers...
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Engineers Tab -->
        <div id="engineers" class="tab-content">
            <div class="two-column">
                <div class="card">
                    <h3><i class="fas fa-user-tie"></i> Add Engineer</h3>
                    <form id="engineerForm">
                        <div class="form-group">
                            <label for="engineerName">Name *</label>
                            <input type="text" id="engineerName" name="name" required>
                            <div class="error-message" id="engineerNameError"></div>
                        </div>
                        <div class="form-group">
                            <label for="engineerEmail">Email *</label>
                            <input type="email" id="engineerEmail" name="email" required>
                            <div class="error-message" id="engineerEmailError"></div>
                        </div>
                        <div class="form-group">
                            <label for="engineerDesignation">Designation *</label>
                            <input type="text" id="engineerDesignation" name="designation" required>
                            <div class="error-message" id="engineerDesignationError"></div>
                        </div>
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-plus"></i> Add Engineer
                        </button>
                    </form>
                </div>
                <div class="card">
                    <h3><i class="fas fa-user-tie"></i> Engineer List</h3>
                    <div id="engineersList">
                        <div class="loading">
                            <div class="spinner"></div>
                            Loading engineers...
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tickets Tab -->
        <div id="tickets" class="tab-content">
            <div class="card">
                <h3><i class="fas fa-ticket-alt"></i> Create New Ticket</h3>
                <form id="ticketForm">
                    <div class="two-column">
                        <div class="form-group">
                            <label for="ticketCustomer">Customer *</label>
                            <select id="ticketCustomer" name="customerName" required>
                                <option value="">Select Customer</option>
                            </select>
                            <div class="error-message" id="ticketCustomerError"></div>
                        </div>
                        <div class="form-group">
                            <label for="ticketPriority">Priority *</label>
                            <select id="ticketPriority" name="priority" required>
                                <option value="">Select Priority</option>
                                <option value="LOW">Low</option>
                                <option value="MEDIUM">Medium</option>
                                <option value="HIGH">High</option>
                                <option value="CRITICAL">Critical</option>
                            </select>
                            <div class="error-message" id="ticketPriorityError"></div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="ticketIssue">Issue Description *</label>
                        <textarea id="ticketIssue" name="issue" rows="4" required></textarea>
                        <div class="error-message" id="ticketIssueError"></div>
                    </div>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-plus"></i> Create Ticket
                    </button>
                </form>
            </div>

            <div class="card">
                <h3><i class="fas fa-list"></i> All Tickets</h3>
                <div id="ticketsList">
                    <div class="loading">
                        <div class="spinner"></div>
                        Loading tickets...
                    </div>
                </div>
            </div>
        </div>

        <!-- Files Tab -->
        <div id="files" class="tab-content">
            <div class="card">
                <h3><i class="fas fa-file-upload"></i> Upload File</h3>
                <form id="fileUploadForm">
                    <div class="form-group">
                        <label for="fileTicketId">Ticket ID *</label>
                        <input type="number" id="fileTicketId" name="ticketId" required>
                        <div class="error-message" id="fileTicketIdError"></div>
                    </div>
                    <div class="form-group">
                        <label>File *</label>
                        <div class="file-upload" id="fileUploadArea">
                            <i class="fas fa-cloud-upload-alt" style="font-size: 48px; color: #ddd; margin-bottom: 10px;"></i>
                            <p>Drag and drop a file here or <strong>click to browse</strong></p>
                            <input type="file" id="fileInput" name="file" style="display: none;" required>
                        </div>
                        <div class="error-message" id="fileError"></div>
                        <div class="success-message" id="fileSuccess"></div>
                    </div>
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-upload"></i> Upload File
                    </button>
                </form>
            </div>
            <div class="card">
                <h3><i class="fas fa-folder-open"></i> Files by Ticket</h3>
                <div class="form-group">
                    <label for="viewFilesTicketId">Enter Ticket ID to view files:</label>
                    <input type="number" id="viewFilesTicketId" placeholder="Ticket ID">
                    <button class="btn btn-secondary" onclick="App.Handlers.viewFilesForTicket()">View Files</button>
                </div>
                <div id="ticketFilesList">
                    <p class="loading">Enter a Ticket ID to view associated files.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Ticket Details -->
    <div id="ticketDetailsModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="App.UI.closeModal('ticketDetailsModal')">&times;</span>
            <h2 id="ticketDetailsModalTitle">Ticket Details</h2>
            <div id="ticketDetailsModalContent"></div>
        </div>
    </div>

    <!-- Modal for Assign Engineer -->
    <div id="assignEngineerModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="App.UI.closeModal('assignEngineerModal')">&times;</span>
            <h2 id="assignEngineerModalTitle">Assign Engineer</h2>
            <div id="assignEngineerModalContent"></div>
        </div>
    </div>

    <!-- Modal for Change Status -->
    <div id="changeStatusModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="App.UI.closeModal('changeStatusModal')">&times;</span>
            <h2 id="changeStatusModalTitle">Change Ticket Status</h2>
            <div id="changeStatusModalContent"></div>
        </div>
    </div>

    <script type="module" src="js/app.js"></script>
</body>
</html>
    """

    # --- styles.css content ---
    styles_css_content = """
/* Base Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Header */
.header {
    background: rgba(255, 255, 255, 0.95);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 30px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
}

.header h1 {
    text-align: center;
    color: #2c3e50;
    font-size: 2.5em;
    margin-bottom: 10px;
}

/* Navigation Tabs */
.nav-tabs {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
    flex-wrap: wrap;
}

.nav-tab {
    padding: 12px 25px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.nav-tab:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.nav-tab.active {
    background: #e74c3c;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}

/* Tab Content */
.tab-content {
    display: none;
    background: rgba(255, 255, 255, 0.95);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
}

.tab-content.active {
    display: block;
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Form Elements */
.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: #2c3e50;
    font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
    width: 100%;
    padding: 12px 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 14px;
    transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.error-message {
    color: #e74c3c;
    font-size: 12px;
    margin-top: 5px;
    display: none;
}

.success-message {
    color: #27ae60;
    font-size: 12px;
    margin-top: 5px;
    display: none;
}

/* Buttons */
.btn {
    background: #3498db;
    color: white;
    padding: 12px 25px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
    margin-right: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn:hover {
    background: #2980b9;
    transform: translateY(-2px);
}

.btn-success {
    background: #27ae60;
}

.btn-success:hover {
    background: #219a52;
}

.btn-danger {
    background: #e74c3c;
}

.btn-danger:hover {
    background: #c0392b;
}

.btn-secondary {
    background: #6c757d;
}

.btn-secondary:hover {
    background: #5a6268;
}

/* Cards */
.card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
}

/* Grids */
.ticket-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

/* Ticket Card Specifics */
.ticket-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.ticket-card:hover {
    transform: translateY(-5px);
}

.ticket-card h4 {
    margin-bottom: 10px;
    color: #2c3e50;
}

.ticket-card p {
    font-size: 0.9em;
    color: #555;
    margin-bottom: 8px;
}

.ticket-card .card-actions {
    margin-top: 15px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

/* Badges */
.priority-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    margin-right: 5px;
}

.priority-LOW { background: #d4edda; color: #155724; }
.priority-MEDIUM { background: #fff3cd; color: #856404; }
.priority-HIGH { background: #f8d7da; color: #721c24; }
.priority-CRITICAL { background: #f5c6cb; color: #491217; }

.status-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
}

.status-OPEN { background: #cce5ff; color: #004085; }
.status-ACKNOWLEDGED { background: #fff2cc; color: #856404; }
.status-CLOSED { background: #d4edda; color: #155724; }

/* Loading State */
.loading {
    text-align: center;
    padding: 20px;
    color: #666;
}

.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 2s linear infinite;
    margin: 0 auto 10px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* File Upload Area */
.file-upload {
    border: 2px dashed #ddd;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.file-upload:hover {
    border-color: #3498db;
    background: #f8f9fa;
}

.file-upload.dragover {
    border-color: #3498db;
    background: #e3f2fd;
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    justify-content: center;
    align-items: center;
    animation: fadeInModal 0.3s ease-out;
}

.modal.active {
    display: flex;
}

@keyframes fadeInModal {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content {
    background: white;
    padding: 30px;
    border-radius: 15px;
    width: 90%;
    max-width: 600px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    position: relative;
    animation: slideInModal 0.3s ease-out;
}

@keyframes slideInModal {
    from { transform: translateY(-50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.modal-content h2 {
    margin-bottom: 20px;
    color: #2c3e50;
    text-align: center;
}

.modal-content p {
    margin-bottom: 10px;
    font-size: 1.1em;
    color: #444;
}

.modal-content p strong {
    color: #333;
}

.modal-content ul {
    list-style: none;
    padding: 0;
    margin-top: 15px;
}

.modal-content ul li {
    background: #f8f9fa;
    padding: 10px 15px;
    border-radius: 8px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.95em;
}

.modal-content ul li:last-child {
    margin-bottom: 0;
}

.close {
    color: #aaa;
    float: right;
    font-size: 32px;
    font-weight: bold;
    cursor: pointer;
    position: absolute;
    top: 15px;
    right: 20px;
    transition: color 0.3s ease;
}

.close:hover {
    color: #333;
}

/* Alerts */
.alert {
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 8px;
    display: none;
    font-weight: 500;
}

.alert-success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .two-column {
        grid-template-columns: 1fr;
    }
    
    .nav-tabs {
        flex-direction: column;
        align-items: stretch;
    }
    
    .nav-tab {
        width: 100%;
        text-align: center;
    }
    
    .ticket-grid {
        grid-template-columns: 1fr;
    }

    .modal-content {
        margin: 10% auto;
        width: 95%;
    }
}
    """

    # --- js/app.js content ---
    app_js_content = """
import { App } from './modules/main.js'; // Import the main App object

document.addEventListener('DOMContentLoaded', () => {
    App.Events.init(); // Set up all event listeners
    App.Handlers.showTab('dashboard'); // Load dashboard data by default
});
    """

    # --- js/modules/main.js content (This will be the new 'App' object) ---
    # This file will consolidate the App object and export it.
    # It will import all other modules.
    main_js_content = """
import { Config } from './config.js';
import { Utils } from './utils.js';
import { UI } from './ui.js';
import { Validation } from './validation.js';
import { Api } from './api.js';
import { State } from './state.js';
import { Data } from './data.js';
import { Handlers } from './handlers.js';

export const App = {
    Config,
    Utils,
    UI,
    Validation,
    Api,
    State,
    Data,
    Handlers
};
    """

    # --- js/modules/config.js content ---
    config_js_content = """
export const Config = {
    API_BASE_URL: 'http://localhost:8080/api'
};
    """

    # --- js/modules/utils.js content ---
    utils_js_content = """
export const Utils = {
    validateEmail: (email) => {
        const re = /^[^\s@]+@[^\s@]+\\.[^\\s@]+$/;
        return re.test(email);
    },
    validatePhone: (phone) => {
        const re = /^[\\+]?[\\d\\s\\-\\(]{10,}$/;
        return re.test(phone);
    },
    validateRequired: (value) => {
        return value && String(value).trim().length > 0;
    },
    validateMinLength: (value, min) => {
        return value && String(value).trim().length >= min;
    }
};
    """

    # --- js/modules/ui.js content ---
    ui_js_content = """
import { State } from './state.js'; // Import State to clear currentTicketIdForModal

export const UI = {
    displayFormErrors: (errors, formElement) => {
        formElement.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });

        for (const field in errors) {
            const specificErrorElement = formElement.querySelector(`#${formElement.id.replace('Form', '')}${field.charAt(0).toUpperCase() + field.slice(1)}Error`);
            if (specificErrorElement) {
                specificErrorElement.textContent = errors[field];
                specificErrorElement.style.display = 'block';
            }
        }
    },

    clearFormErrors: (formElement) => {
        formElement.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });
    },

    showAlert: (message, isSuccess) => {
        const successAlert = document.getElementById('successAlert');
        const errorAlert = document.getElementById('errorAlert');

        successAlert.style.display = 'none';
        errorAlert.style.display = 'none';

        if (isSuccess) {
            successAlert.textContent = message;
            successAlert.style.display = 'block';
        } else {
            errorAlert.textContent = message;
            errorAlert.style.display = 'block';
        }

        setTimeout(() => {
            successAlert.style.display = 'none';
            errorAlert.style.display = 'none';
        }, 5000);
    },

    showLoading: (container) => {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                Loading...
            </div>
        `;
    },

    hideLoading: (container) => {
        container.innerHTML = '';
    },

    openModal: (modalId, title, contentHtml) => {
        const modal = document.getElementById(modalId);
        const modalTitle = modal.querySelector('h2');
        const modalContent = modal.querySelector('div[id$="Content"]');

        modalTitle.textContent = title;
        modalContent.innerHTML = contentHtml;
        modal.classList.add('active');
    },

    closeModal: (modalId) => {
        document.getElementById(modalId).classList.remove('active');
        if (modalId === 'assignEngineerModal' || modalId === 'changeStatusModal') {
            State.currentTicketIdForModal = null;
        }
    }
};
    """

    # --- js/modules/validation.js content ---
    validation_js_content = """
import { Utils } from './utils.js';

export const Validation = {
    validateCustomerForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.name)) {
            errors.name = 'Name is required';
        } else if (!Utils.validateMinLength(formData.name, 2)) {
            errors.name = 'Name must be at least 2 characters';
        }
        if (!Utils.validateRequired(formData.email)) {
            errors.email = 'Email is required';
        } else if (!Utils.validateEmail(formData.email)) {
            errors.email = 'Please enter a valid email address';
        }
        if (formData.phoneNumber && !Utils.validatePhone(formData.phoneNumber)) {
            errors.phoneNumber = 'Please enter a valid phone number';
        }
        if (!Utils.validateRequired(formData.companyName)) {
            errors.companyName = 'Company name is required';
        }
        return errors;
    },

    validateEngineerForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.name)) {
            errors.name = 'Name is required';
        } else if (!Utils.validateMinLength(formData.name, 2)) {
            errors.name = 'Name must be at least 2 characters';
        }
        if (!Utils.validateRequired(formData.email)) {
            errors.email = 'Email is required';
        } else if (!Utils.validateEmail(formData.email)) {
            errors.email = 'Please enter a valid email address';
        }
        if (!Utils.validateRequired(formData.designation)) {
            errors.designation = 'Designation is required';
        } else if (!Utils.validateMinLength(formData.designation, 2)) {
            errors.designation = 'Designation must be at least 2 characters';
        }
        return errors;
    },

    validateTicketForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.customerName)) {
            errors.customerName = 'Customer is required';
        }
        if (!Utils.validateRequired(formData.priority)) {
            errors.priority = 'Priority is required';
        }
        if (!Utils.validateRequired(formData.issue)) {
            errors.issue = 'Issue description is required';
        } else if (!Utils.validateMinLength(formData.issue, 10)) {
            errors.issue = 'Issue description must be at least 10 characters';
        }
        return errors;
    },

    validateFileUploadForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.ticketId)) {
            errors.ticketId = 'Ticket ID is required';
        } else if (isNaN(formData.ticketId) || parseInt(formData.ticketId) <= 0) {
            errors.ticketId = 'Ticket ID must be a positive number';
        }
        if (!formData.file) {
            errors.file = 'Please select a file to upload';
        }
        return errors;
    }
};
    """

    # --- js/modules/api.js content ---
    api_js_content = """
import { Config } from './config.js';

export const Api = {
    call: async (endpoint, method, body = null, isFormData = false) => {
        const url = `${Config.API_BASE_URL}${endpoint}`;
        const options = {
            method: method,
            headers: {}
        };

        if (body) {
            if (isFormData) {
                options.body = body;
            } else {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(body);
            }
        }

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                const contentType = response.headers.get('content-type');
                let errorData;
                if (contentType && contentType.includes('application/json')) {
                    errorData = await response.json().catch(() => ({ message: response.statusText || 'Unknown error' }));
                } else {
                    errorData = { message: await response.text().catch(() => response.statusText || 'Unknown error') };
                }
                throw new Error(errorData.message || JSON.stringify(errorData));
            }

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return response.json();
            } else {
                return response.text();
            }
        } catch (error) {
            console.error(`API Error (${method} ${endpoint}):`, error);
            throw error;
        }
    },

    createCustomer: async (customerData) => Api.call('/customers', 'POST', customerData),
    getAllCustomers: async () => Api.call('/customers', 'GET'),

    createEngineer: async (engineerData) => Api.call('/engineers', 'POST', engineerData),
    getAllEngineers: async () => Api.call('/engineers', 'GET'),

    createTicket: async (ticketData) => Api.call('/tickets/create', 'POST', ticketData),
    getAllTickets: async () => Api.call('/tickets/all', 'GET'),
    assignTicketToEngineer: async (ticketId, engineerId) => Api.call(`/tickets/${ticketId}/assign/${engineerId}`, 'POST'),
    unassignEngineer: async (ticketId) => Api.call(`/tickets/${ticketId}/unassign`, 'POST'),
    updateTicketStatus: async (ticketId, status) => Api.call(`/tickets/${ticketId}/status?status=${status}`, 'PUT'),
    getTicketById: async (ticketId) => Api.call(`/tickets/${ticketId}`, 'GET'),

    uploadFile: async (ticketId, file) => {
        const formData = new FormData();
        formData.append('file', file);
        return Api.call(`/files/upload/${ticketId}`, 'POST', formData, true);
    },
    getFilesByTicket: async (ticketId) => Api.call(`/files/ticket/${ticketId}`, 'GET')
};
    """

    # --- js/modules/state.js content ---
    state_js_content = """
export const State = {
    currentTicketIdForModal: null
};
    """

    # --- js/modules/data.js content ---
    data_js_content = """
import { Api } from './api.js';
import { UI } from './ui.js';
import { Handlers } from './handlers.js'; // For openTicketDetailsModal, openAssignEngineerModal, openChangeStatusModal

export const Data = {
    fetchCustomers: async () => {
        const customersListDiv = document.getElementById('customersList');
        UI.showLoading(customersListDiv);
        try {
            const customers = await Api.getAllCustomers();
            UI.hideLoading(customersListDiv);
            if (customers.length === 0) {
                customersListDiv.innerHTML = '<p>No customers found.</p>';
                return;
            }
            customersListDiv.innerHTML = customers.map(customer => `
                <div class="card">
                    <h4>${customer.name}</h4>
                    <p><strong>Email:</strong> ${customer.email}</p>
                    <p><strong>Company:</strong> ${customer.companyName}</p>
                    ${customer.phoneNumber ? `<p><strong>Phone:</strong> ${customer.phoneNumber}</p>` : ''}
                </div>
            `).join('');
        } catch (error) {
            UI.hideLoading(customersListDiv);
            customersListDiv.innerHTML = `<p class="error-message" style="display:block;">Failed to load customers: ${error.message}</p>`;
            UI.showAlert('Failed to load customers.', false);
        }
    },

    fetchEngineers: async () => {
        const engineersListDiv = document.getElementById('engineersList');
        UI.showLoading(engineersListDiv);
        try {
            const engineers = await Api.getAllEngineers();
            UI.hideLoading(engineersListDiv);
            if (engineers.length === 0) {
                engineersListDiv.innerHTML = '<p>No engineers found.</p>';
                return;
            }
            engineersListDiv.innerHTML = engineers.map(engineer => `
                <div class="card">
                    <h4>${engineer.name}</h4>
                    <p><strong>Email:</strong> ${engineer.email}</p>
                    <p><strong>Designation:</strong> ${engineer.designation}</p>
                </div>
            `).join('');
        } catch (error) {
            UI.hideLoading(engineersListDiv);
            engineersListDiv.innerHTML = `<p class="error-message" style="display:block;">Failed to load engineers: ${error.message}</p>`;
            UI.showAlert('Failed to load engineers.', false);
        }
    },

    fetchCustomersForTicketForm: async () => {
        const ticketCustomerSelect = document.getElementById('ticketCustomer');
        ticketCustomerSelect.innerHTML = '<option value="">Select Customer</option>';
        try {
            const customers = await Api.getAllCustomers();
            customers.forEach(customer => {
                const option = document.createElement('option');
                option.value = customer.name;
                option.textContent = customer.name;
                ticketCustomerSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load customers for ticket form:', error);
            UI.showAlert('Failed to load customers for ticket form.', false);
        }
    },

    fetchAllTickets: async () => {
        const ticketsListDiv = document.getElementById('ticketsList');
        UI.showLoading(ticketsListDiv);
        try {
            const tickets = await Api.getAllTickets();
            UI.hideLoading(ticketsListDiv);
            if (tickets.length === 0) {
                ticketsListDiv.innerHTML = '<p>No tickets found.</p>';
                return;
            }

            ticketsListDiv.innerHTML = `
                <div class="ticket-grid">
                    ${tickets.map(ticket => `
                        <div class="ticket-card">
                            <h4>Ticket #${ticket.id} - ${ticket.customer ? ticket.customer.name : 'N/A'}</h4>
                            <p><strong>Issue:</strong> ${ticket.issueDescription}</p>
                            <p>
                                <span class="priority-badge priority-${ticket.priority}">${ticket.priority}</span>
                                <span class="status-badge status-${ticket.ticketStatus}">${ticket.ticketStatus}</span>
                            </p>
                            <p><strong>Assigned To:</strong> ${ticket.assignedEngineer ? ticket.assignedEngineer.name : 'Unassigned'}</p>
                            <div class="card-actions">
                                <button class="btn btn-secondary" onclick="App.Handlers.openTicketDetailsModal(${ticket.id})">
                                    <i class="fas fa-info-circle"></i> Details
                                </button>
                                ${ticket.assignedEngineer ? `
                                    <button class="btn btn-danger" onclick="App.Handlers.handleUnassignTicket(${ticket.id})">
                                        <i class="fas fa-user-times"></i> Unassign
                                    </button>
                                ` : `
                                    <button class="btn btn-success" onclick="App.Handlers.openAssignEngineerModal(${ticket.id})">
                                        <i class="fas fa-user-plus"></i> Assign
                                    </button>
                                `}
                                <button class="btn btn-secondary" onclick="App.Handlers.openChangeStatusModal(${ticket.id}, '${ticket.ticketStatus}')">
                                    <i class="fas fa-sync-alt"></i> Change Status
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } catch (error) {
            UI.hideLoading(ticketsListDiv);
            ticketsListDiv.innerHTML = `<p class="error-message" style="display:block;">Failed to load tickets: ${error.message}</p>`;
            UI.showAlert('Failed to load tickets.', false);
        }
    },

    fetchDashboardStats: async () => {
        const statsContainer = document.getElementById('statsContainer');
        UI.showLoading(statsContainer);
        try {
            const tickets = await Api.getAllTickets();
            const customers = await Api.getAllCustomers();
            const engineers = await Api.getAllEngineers();

            const openTickets = tickets.filter(t => t.ticketStatus === 'OPEN').length;
            const acknowledgedTickets = tickets.filter(t => t.ticketStatus === 'ACKNOWLEDGED').length;
            const closedTickets = tickets.filter(t => t.ticketStatus === 'CLOSED').length;

            UI.hideLoading(statsContainer);
            statsContainer.innerHTML = `
                <p><strong>Total Customers:</strong> ${customers.length}</p>
                <p><strong>Total Engineers:</strong> ${engineers.length}</p>
                <p><strong>Total Tickets:</strong> ${tickets.length}</p>
                <p><strong>Open Tickets:</strong> ${openTickets}</p>
                <p><strong>Acknowledged Tickets:</strong> ${acknowledgedTickets}</p>
                <p><strong>Closed Tickets:</strong> ${closedTickets}</p>
            `;
        } catch (error) {
            UI.hideLoading(statsContainer);
            statsContainer.innerHTML = `<p class="error-message" style="display:block;">Failed to load stats: ${error.message}</p>`;
            UI.showAlert('Failed to load dashboard statistics.', false);
        }
    },

    fetchRecentActivity: async () => {
        const recentActivityDiv = document.getElementById('recentActivity');
        UI.showLoading(recentActivityDiv);
        try {
            const tickets = await Api.getAllTickets();
            const recentTickets = tickets.sort((a, b) => b.id - a.id).slice(0, 5);

            UI.hideLoading(recentActivityDiv);
            if (recentTickets.length === 0) {
                recentActivityDiv.innerHTML = '<p>No recent activity.</p>';
                return;
            }
            recentActivityDiv.innerHTML = `
                <ul>
                    ${recentTickets.map(ticket => `
                        <li>
                            Ticket #${ticket.id} (${ticket.customer ? ticket.customer.name : 'N/A'}) - ${ticket.issueDescription.substring(0, 50)}...
                            <span class="status-badge status-${ticket.ticketStatus}">${ticket.ticketStatus}</span>
                        </li>
                    `).join('')}
                </ul>
            `;
        } catch (error) {
            UI.hideLoading(recentActivityDiv);
            recentActivityDiv.innerHTML = `<p class="error-message" style="display:block;">Failed to load recent activity: ${error.message}</p>`;
            UI.showAlert('Failed to load recent activity.', false);
        }
    }
};
    """

    # --- js/modules/handlers.js content ---
    handlers_js_content = """
import { UI } from './ui.js';
import { Api } from './api.js';
import { State } from './state.js';
import { Data } from './data.js';
import { Validation } from './validation.js';

export const Handlers = {
    showTab: (tabId) => {
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });

        document.getElementById(tabId).classList.add('active');
        document.querySelector(`.nav-tab[onclick="App.Handlers.showTab('${tabId}')"]`).classList.add('active');

        if (tabId === 'customers') {
            Data.fetchCustomers();
        } else if (tabId === 'engineers') {
            Data.fetchEngineers();
        } else if (tabId === 'tickets') {
            Data.fetchCustomersForTicketForm();
            Data.fetchAllTickets();
        } else if (tabId === 'dashboard') {
            Data.fetchDashboardStats();
            Data.fetchRecentActivity();
        }
    },

    openTicketDetailsModal: async (ticketId) => {
        const modalId = 'ticketDetailsModal';
        UI.openModal(modalId, `Ticket Details - Loading...`, `<div class="loading"><div class="spinner"></div>Loading ticket details...</div>`);

        try {
            const ticket = await Api.getTicketById(ticketId);
            if (ticket) {
                const contentHtml = `
                    <p><strong>Customer:</strong> ${ticket.customer ? ticket.customer.name : 'N/A'}</p>
                    <p><strong>Issue:</strong> ${ticket.issueDescription}</p>
                    <p><strong>Priority:</strong> <span class="priority-badge priority-${ticket.priority}">${ticket.priority}</span></p>
                    <p><strong>Status:</strong> <span class="status-badge status-${ticket.ticketStatus}">${ticket.ticketStatus}</span></p>
                    <p><strong>Response:</strong> ${ticket.ticketResponse || 'N/A'}</p>
                    <p><strong>Assigned Engineer:</strong> ${ticket.assignedEngineer ? ticket.assignedEngineer.name : 'Unassigned'}</p>
                    ${ticket.logFiles && ticket.logFiles.length > 0 ? `
                        <h4>Attachments:</h4>
                        <ul>
                            ${ticket.logFiles.map(file => `<li><i class="fas fa-file"></i> ${file.fileName}</li>`).join('')}
                        </ul>
                    ` : '<p>No attachments.</p>'}
                    ${ticket.auditLogs && ticket.auditLogs.length > 0 ? `
                        <h4>Audit Log:</h4>
                        <ul>
                            ${ticket.auditLogs.map(log => `<li>[${new Date(log.timestamp).toLocaleString()}] ${log.message}</li>`).join('')}
                        </ul>
                    ` : '<p>No audit logs.</p>'}
                `;
                UI.openModal(modalId, `Ticket Details #${ticket.id}`, contentHtml);
            } else {
                UI.openModal(modalId, `Ticket Not Found`, `<p class="error-message" style="display:block;">Ticket with ID ${ticketId} not found.</p>`);
            }
        } catch (error) {
            UI.openModal(modalId, `Error Loading Ticket`, `<p class="error-message" style="display:block;">Failed to load ticket details: ${error.message}</p>`);
            UI.showAlert('Failed to load ticket details.', false);
        }
    },

    openAssignEngineerModal: async (ticketId) => {
        State.currentTicketIdForModal = ticketId;
        const modalId = 'assignEngineerModal';
        UI.openModal(modalId, `Assign Engineer to Ticket #${ticketId}`, `<div class="loading"><div class="spinner"></div>Loading engineers...</div>`);

        try {
            const engineers = await Api.getAllEngineers();
            if (engineers.length === 0) {
                UI.openModal(modalId, `Assign Engineer to Ticket #${ticketId}`, '<p>No engineers available to assign.</p>');
                return;
            }

            const contentHtml = `
                <div class="form-group">
                    <label for="assignEngineerSelect">Select Engineer:</label>
                    <select id="assignEngineerSelect" class="w-full p-2 border rounded">
                        <option value="">Select an Engineer</option>
                        ${engineers.map(engineer => `<option value="${engineer.id}">${engineer.name} (${engineer.designation})</option>`).join('')}
                    </select>
                </div>
                <button class="btn btn-success" onclick="App.Handlers.handleAssignTicket()">Assign</button>
            `;
            UI.openModal(modalId, `Assign Engineer to Ticket #${ticketId}`, contentHtml);
        } catch (error) {
            UI.openModal(modalId, `Error Loading Engineers`, `<p class="error-message" style="display:block;">Failed to load engineers: ${error.message}</p>`);
            UI.showAlert('Failed to load engineers for assignment.', false);
        }
    },

    handleAssignTicket: async () => {
        const engineerId = document.getElementById('assignEngineerSelect').value;
        if (!engineerId) {
            UI.showAlert('Please select an engineer.', false);
            return;
        }

        if (!State.currentTicketIdForModal) {
            UI.showAlert('No ticket selected for assignment.', false);
            return;
        }

        try {
            await Api.assignTicketToEngineer(State.currentTicketIdForModal, parseInt(engineerId));
            UI.showAlert('Ticket assigned successfully!', true);
            UI.closeModal('assignEngineerModal');
            Data.fetchAllTickets();
        } catch (error) {
            UI.showAlert(`Failed to assign ticket: ${error.message}`, false);
        }
    },

    handleUnassignTicket: async (ticketId) => {
        if (!confirm('Are you sure you want to unassign the engineer from this ticket?')) {
            return;
        }
        try {
            await Api.unassignEngineer(ticketId);
            UI.showAlert('Engineer unassigned successfully!', true);
            Data.fetchAllTickets();
        } catch (error) {
            UI.showAlert(`Failed to unassign engineer: ${error.message}`, false);
        }
    },

    openChangeStatusModal: (ticketId, currentStatus) => {
        State.currentTicketIdForModal = ticketId;
        const modalId = 'changeStatusModal';
        const statuses = ['OPEN', 'ACKNOWLEDGED', 'CLOSED'];

        const optionsHtml = statuses.map(status =>
            `<option value="${status}" ${status === currentStatus ? 'selected' : ''}>${status}</option>`
        ).join('');

        const contentHtml = `
            <div class="form-group">
                <label for="changeStatusSelect">Select New Status:</label>
                <select id="changeStatusSelect" class="w-full p-2 border rounded">
                    ${optionsHtml}
                </select>
            </div>
            <button class="btn btn-success" onclick="App.Handlers.handleChangeStatus()">Change Status</button>
        `;
        UI.openModal(modalId, `Change Status for Ticket #${ticketId}`, contentHtml);
    },

    handleChangeStatus: async () => {
        const newStatus = document.getElementById('changeStatusSelect').value;
        if (!newStatus) {
            UI.showAlert('Please select a status.', false);
            return;
        }

        if (!State.currentTicketIdForModal) {
            UI.showAlert('No ticket selected for status change.', false);
            return;
        }

        try {
            await Api.updateTicketStatus(State.currentTicketIdForModal, newStatus);
            UI.showAlert('Ticket status updated successfully!', true);
            UI.closeModal('changeStatusModal');
            Data.fetchAllTickets();
            Data.fetchDashboardStats();
        } catch (error) {
            UI.showAlert(`Failed to update ticket status: ${error.message}`, false);
        }
    },

    viewFilesForTicket: async () => {
        const ticketIdInput = document.getElementById('viewFilesTicketId');
        const ticketId = parseInt(ticketIdInput.value);
        const ticketFilesListDiv = document.getElementById('ticketFilesList');

        if (isNaN(ticketId) || ticketId <= 0) {
            ticketFilesListDiv.innerHTML = '<p class="error-message" style="display:block;">Please enter a valid Ticket ID.</p>';
            return;
        }

        UI.showLoading(ticketFilesListDiv);
        try {
            const files = await Api.getFilesByTicket(ticketId);
            UI.hideLoading(ticketFilesListDiv);
            if (files.length === 0) {
                ticketFilesListDiv.innerHTML = `<p>No files found for Ticket ID ${ticketId}.</p>`;
                return;
            }
            ticketFilesListDiv.innerHTML = `
                <h4>Files for Ticket #${ticketId}:</h4>
                <ul>
                    ${files.map(filePath => {
                        const fileName = filePath.split(/[\\\\/]/).pop();
                        return `<li><i class="fas fa-file"></i> ${fileName}</li>`;
                    }).join('')}
                </ul>
            `;
        } catch (error) {
            UI.hideLoading(ticketFilesListDiv);
            ticketFilesListDiv.innerHTML = `<p class="error-message" style="display:block;">Failed to load files: ${error.message}</p>`;
            UI.showAlert(`Failed to load files for Ticket ID ${ticketId}.`, false);
        }
    }
};
    """

    # --- js/modules/events.js content (New file for event listener setup) ---
    events_js_content = """
import { UI } from './ui.js';
import { Api } from './api.js';
import { Data } from './data.js';
import { Validation } from './validation.js';

export const Events = {
    init: () => {
        document.getElementById('customerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = {
                name: form.name.value,
                email: form.email.value,
                phoneNumber: form.phoneNumber.value,
                companyName: form.companyName.value
            };

            UI.clearFormErrors(form);
            const errors = Validation.validateCustomerForm(formData);
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                await Api.createCustomer(formData);
                UI.showAlert('Customer added successfully!', true);
                form.reset();
                Data.fetchCustomers();
            } catch (error) {
                UI.showAlert(`Failed to add customer: ${error.message}`, false);
            }
        });

        document.getElementById('engineerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = {
                name: form.name.value,
                email: form.email.value,
                designation: form.designation.value
            };

            UI.clearFormErrors(form);
            const errors = Validation.validateEngineerForm(formData);
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                await Api.createEngineer(formData);
                UI.showAlert('Engineer added successfully!', true);
                form.reset();
                Data.fetchEngineers();
            } catch (error) {
                UI.showAlert(`Failed to add engineer: ${error.message}`, false);
            }
        });

        document.getElementById('ticketForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = {
                customerName: form.customerName.value,
                priority: form.priority.value,
                issue: form.issue.value
            };

            UI.clearFormErrors(form);
            const errors = Validation.validateTicketForm(formData);
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                await Api.createTicket(formData);
                UI.showAlert('Ticket created successfully!', true);
                form.reset();
                Data.fetchAllTickets();
                Data.fetchDashboardStats();
                Data.fetchRecentActivity();
            } catch (error) {
                UI.showAlert(`Failed to create ticket: ${error.message}`, false);
            }
        });

        document.getElementById('fileUploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const ticketId = form.fileTicketId.value;
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];

            UI.clearFormErrors(form);
            const errors = Validation.validateFileUploadForm({ ticketId, file });
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                const uploadMessage = document.getElementById('fileSuccess');
                uploadMessage.textContent = 'Uploading...';
                uploadMessage.style.display = 'block';

                const response = await Api.uploadFile(parseInt(ticketId), file);
                if (response.success) {
                    UI.showAlert(response.message, true);
                    uploadMessage.textContent = response.message;
                    form.reset();
                } else {
                    throw new Error(response.message || "Unknown file upload error.");
                }
            } catch (error) {
                const uploadError = document.getElementById('fileError');
                uploadError.textContent = `Failed to upload file: ${error.message}`;
                uploadError.style.display = 'block';
                UI.showAlert(`Failed to upload file: ${error.message}`, false);
            } finally {
                setTimeout(() => {
                    document.getElementById('fileSuccess').style.display = 'none';
                    document.getElementById('fileError').style.display = 'none';
                }, 5000);
            }
        });

        const fileUploadArea = document.getElementById('fileUploadArea');
        const fileInput = document.getElementById('fileInput');

        fileUploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });

        fileUploadArea.addEventListener('dragleave', () => {
            fileUploadArea.classList.remove('dragover');
        });

        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            fileInput.files = e.dataTransfer.files;
            if (fileInput.files.length > 0) {
                const fileNameDisplay = fileUploadArea.querySelector('p');
                fileNameDisplay.textContent = `Selected: ${fileInput.files[0].name}`;
            }
        });
    }
};
    """

    files_to_create = {
        os.path.join(base_dir, "index.html"): index_html_content,
        os.path.join(css_dir, "styles.css"): styles_css_content,
        os.path.join(js_dir, "app.js"): app_js_content,
        os.path.join(modules_dir, "main.js"): main_js_content, # New main.js to consolidate App object
        os.path.join(modules_dir, "config.js"): config_js_content,
        os.path.join(modules_dir, "utils.js"): utils_js_content,
        os.path.join(modules_dir, "ui.js"): ui_js_content,
        os.path.join(modules_dir, "validation.js"): validation_js_content,
        os.path.join(modules_dir, "api.js"): api_js_content,
        os.path.join(modules_dir, "state.js"): state_js_content,
        os.path.join(modules_dir, "data.js"): data_js_content,
        os.path.join(modules_dir, "handlers.js"): handlers_js_content,
        os.path.join(modules_dir, "events.js"): events_js_content, # New events.js
    }

    for file_path, content in files_to_create.items():
        with open(file_path, "w") as f:
            f.write(content.strip()) # .strip() to remove leading/trailing blank lines
        print(f"Created: {file_path}")

    print("\nFrontend files generated successfully in the 'frontend' directory!")
    print("To run, navigate to the 'frontend' directory and open 'index.html' in your browser.")
    print("Ensure your Spring Boot backend is running on http://localhost:8080.")

if __name__ == "__main__":
    create_frontend_files()
