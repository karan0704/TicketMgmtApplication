// API Service for handling all backend endpoints
const API_BASE_URL = 'http://localhost:8080/api';

class ApiService {
    constructor() {
        this.token = localStorage.getItem('token');
    }

    // Helper method for headers
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (includeAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // Auth endpoints
    async login(username, password) {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify({ username, password })
        });
        if (!response.ok) throw new Error('Login failed');
        const data = await response.json();
        this.token = data.token;
        localStorage.setItem('token', data.token);
        return data;
    }

    async register(username, password, role) {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: this.getHeaders(false),
            body: JSON.stringify({ username, password, role })
        });
        if (!response.ok) throw new Error('Registration failed');
        return response.json();
    }

    async logout() {
        localStorage.removeItem('token');
        this.token = null;
    }

    // User endpoints
    async getCurrentUser() {
        const response = await fetch(`${API_BASE_URL}/users/current`, {
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch current user');
        return response.json();
    }

    async updateUser(userId, userData) {
        const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify(userData)
        });
        if (!response.ok) throw new Error('Failed to update user');
        return response.json();
    }

    // Ticket endpoints
    async createTicket(ticketData) {
        const response = await fetch(`${API_BASE_URL}/tickets`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(ticketData)
        });
        if (!response.ok) throw new Error('Failed to create ticket');
        return response.json();
    }

    async getAllTickets() {
        const response = await fetch(`${API_BASE_URL}/tickets`, {
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch tickets');
        return response.json();
    }

    async getTicketById(ticketId) {
        const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}`, {
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch ticket');
        return response.json();
    }

    async updateTicket(ticketId, ticketData) {
        const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify(ticketData)
        });
        if (!response.ok) throw new Error('Failed to update ticket');
        return response.json();
    }

    async deleteTicket(ticketId) {
        const response = await fetch(`${API_BASE_URL}/tickets/${ticketId}`, {
            method: 'DELETE',
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error('Failed to delete ticket');
        return response.json();
    }

    // Engineer endpoints
    async getAllEngineers() {
        const response = await fetch(`${API_BASE_URL}/engineers`, {
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error('Failed to fetch engineers');
        return response.json();
    }

    async assignTicket(ticketId, engineerId) {
        const response = await fetch(`${API_BASE_URL}/engineers/assign/${ticketId}`, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify({ engineerId })
        });
        if (!response.ok) throw new Error('Failed to assign ticket');
        return response.json();
    }

    // File upload endpoints
    async uploadFile(ticketId, file) {
        const formData = new FormData();
        formData.append('file', file);

        const headers = {
            'Authorization': `Bearer ${this.token}`
        };

        const response = await fetch(`${API_BASE_URL}/files/upload/${ticketId}`, {
            method: 'POST',
            headers,
            body: formData
        });
        if (!response.ok) throw new Error('Failed to upload file');
        return response.json();
    }

    async downloadFile(fileId) {
        const response = await fetch(`${API_BASE_URL}/files/download/${fileId}`, {
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error('Failed to download file');
        return response.blob();
    }
}

export const apiService = new ApiService();