import { UI } from './ui.js';
import { Api } from './api.js';
import { State } from './state.js';
import { Data } from './data.js';
// import { Validation } from './validation.js'; // Not directly used here, but good to keep if needed for other handlers

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
                        const fileName = filePath.split(/[\\/]/).pop();
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