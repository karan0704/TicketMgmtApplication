// api.js
// This file centralizes all communication with your Spring Boot backend.
// Assumes your backend is running on http://localhost:8080
const BASE_URL = 'http://localhost:8080/api';

// Imports from utils.js (will be available globally when loaded in index.html)
// showMessage and setLoading are assumed to be globally available from utils.js

const api = (() => {
    /**
     * Generic request function to interact with the backend API.
     * @param {string} method - HTTP method (GET, POST, PUT, DELETE).
     * @param {string} path - API endpoint path (e.g., '/customers').
     * @param {Object|FormData|null} data - Request body data or FormData object.
     * @param {boolean} isFormData - True if data is FormData, false otherwise.
     * @returns {Promise<Object|null>} - JSON response from the API or null.
     */
    const request = async (method, path, data = null, isFormData = false) => {
        setLoading(true); // Show loading spinner
        try {
            const headers = {};
            let body = null;

            if (data && !isFormData) {
                headers['Content-Type'] = 'application/json';
                body = JSON.stringify(data);
            } else if (data && isFormData) {
                body = data; // FormData will set its own Content-Type header
            }

            const response = await fetch(`${BASE_URL}${path}`, {
                method,
                headers,
                body,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || `HTTP error! status: ${response.status}`);
            }

            // Handle cases where response might be empty (e.g., 204 No Content)
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                return null; // Or handle as text if needed
            }
        } catch (error) {
            console.error('API call failed:', error);
            showMessage(`Error: ${error.message}`, 'error');
            throw error; // Re-throw to allow component-specific error handling
        } finally {
            setLoading(false); // Hide loading spinner
        }
    };

    return {
        // Customer Endpoints
        createCustomer: (customer) => request('POST', '/customers', customer),
        getAllCustomers: () => request('GET', '/customers'),
        getCustomer: (id) => request('GET', `/customers/${id}`),

        // Engineer Endpoints
        getAllEngineers: () => request('GET', '/engineers'),
        createEngineer: (engineer) => request('POST', '/engineers', engineer),

        // File Upload Endpoints
        uploadFile: (file, ticketId) => {
            const formData = new FormData();
            formData.append('file', file);
            return request('POST', `/files/upload/${ticketId}`, formData, true);
        },
        getFilesByTicket: (ticketId) => request('GET', `/files/ticket/${ticketId}`),

        // Ticket Endpoints
        createTicket: (customerName, issue, priority) => {
            // Note: Your backend uses @RequestParam for createTicket, so we'll use URLSearchParams
            const params = new URLSearchParams({ customerName, issue, priority }).toString();
            return request('POST', `/tickets/create?${params}`);
        },
        getTicketById: (id) => request('GET', `/tickets/${id}`),
        assignTicket: (id, engineerId) => request('POST', `/tickets/${id}/assign/${engineerId}`),
        unassignTicket: (id) => request('POST', `/tickets/${id}/unassign`),
        getAllTickets: () => request('GET', '/tickets/all'),
    };
})();
