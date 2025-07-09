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