// Ticket Service for handling ticket-related operations
import { apiService } from './apiService.js';

class TicketService {
    async createTicket(ticketData) {
        try {
            return await apiService.createTicket(ticketData);
        } catch (error) {
            throw new Error('Failed to create ticket: ' + error.message);
        }
    }

    async getAllTickets() {
        try {
            return await apiService.getAllTickets();
        } catch (error) {
            throw new Error('Failed to fetch tickets: ' + error.message);
        }
    }

    async getTicketById(ticketId) {
        try {
            return await apiService.getTicketById(ticketId);
        } catch (error) {
            throw new Error('Failed to fetch ticket: ' + error.message);
        }
    }

    async updateTicket(ticketId, ticketData) {
        try {
            return await apiService.updateTicket(ticketId, ticketData);
        } catch (error) {
            throw new Error('Failed to update ticket: ' + error.message);
        }
    }

    async deleteTicket(ticketId) {
        try {
            return await apiService.deleteTicket(ticketId);
        } catch (error) {
            throw new Error('Failed to delete ticket: ' + error.message);
        }
    }

    async assignTicket(ticketId, engineerId) {
        try {
            return await apiService.assignTicket(ticketId, engineerId);
        } catch (error) {
            throw new Error('Failed to assign ticket: ' + error.message);
        }
    }

    async uploadFile(ticketId, file) {
        try {
            return await apiService.uploadFile(ticketId, file);
        } catch (error) {
            throw new Error('Failed to upload file: ' + error.message);
        }
    }

    async downloadFile(fileId) {
        try {
            return await apiService.downloadFile(fileId);
        } catch (error) {
            throw new Error('Failed to download file: ' + error.message);
        }
    }

    async getAllEngineers() {
        try {
            return await apiService.getAllEngineers();
        } catch (error) {
            throw new Error('Failed to fetch engineers: ' + error.message);
        }
    }
}

export const ticketService = new TicketService();