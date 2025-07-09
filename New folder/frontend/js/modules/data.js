import { Api } from './api.js';
import { UI } from './ui.js';

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
            console.error('Error fetching customers:', error);
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
            console.error('Error fetching engineers:', error);
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
            console.error('Error fetching all tickets:', error);
        }
    },

    fetchDashboardStats: async () => {
        const statsContainer = document.getElementById('statsContainer');
        UI.showLoading(statsContainer);
        try {
            const [tickets, customers, engineers] = await Promise.all([
                Api.getAllTickets(),
                Api.getAllCustomers(),
                Api.getAllEngineers()
            ]);

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
            statsContainer.innerHTML = `<p class="error-message" style="display:block;">Failed to load statistics: ${error.message}</p>`;
            UI.showAlert('Failed to load dashboard statistics.', false);
            console.error('Error fetching dashboard statistics:', error);
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
            console.error('Error fetching recent activity:', error);
        }
    }
};