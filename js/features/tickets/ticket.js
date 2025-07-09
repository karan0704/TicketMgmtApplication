import domUtils from '../../utils/domUtils.js';
import ticketService from '../../services/ticketService.js';

const ticket = {
    init() {
        this.renderTicketDashboard();
        this.attachEventListeners();
        this.loadTickets();
    },

    renderTicketDashboard() {
        const container = document.getElementById('main-content');
        domUtils.clearElement(container);

        const dashboard = domUtils.createElement('div', { class: 'ticket-dashboard' }, [
            // Create Ticket Form
            domUtils.createElement('div', { class: 'ticket-form-container' }, [
                domUtils.createElement('h2', {}, ['Create New Ticket']),
                domUtils.createElement('form', { class: 'ticket-form', id: 'createTicketForm' }, [
                    domUtils.createElement('div', { class: 'form-group' }, [
                        domUtils.createElement('label', { for: 'customerName' }, ['Customer Name']),
                        domUtils.createElement('input', { 
                            type: 'text', 
                            id: 'customerName', 
                            name: 'customerName',
                            required: 'true'
                        })
                    ]),
                    domUtils.createElement('div', { class: 'form-group' }, [
                        domUtils.createElement('label', { for: 'issue' }, ['Issue Description']),
                        domUtils.createElement('textarea', { 
                            id: 'issue', 
                            name: 'issue',
                            required: 'true',
                            rows: '4'
                        })
                    ]),
                    domUtils.createElement('div', { class: 'form-group' }, [
                        domUtils.createElement('label', { for: 'priority' }, ['Priority']),
                        domUtils.createElement('select', { id: 'priority', name: 'priority' }, [
                            domUtils.createElement('option', { value: 'LOW' }, ['Low']),
                            domUtils.createElement('option', { value: 'MEDIUM' }, ['Medium']),
                            domUtils.createElement('option', { value: 'HIGH' }, ['High']),
                            domUtils.createElement('option', { value: 'CRITICAL' }, ['Critical'])
                        ])
                    ]),
                    domUtils.createElement('button', { 
                        type: 'submit',
                        class: 'btn btn-primary'
                    }, ['Create Ticket'])
                ])
            ]),

            // Tickets List
            domUtils.createElement('div', { class: 'tickets-list-container' }, [
                domUtils.createElement('h2', {}, ['All Tickets']),
                domUtils.createElement('div', { id: 'ticketsList', class: 'tickets-list' })
            ])
        ]);

        container.appendChild(dashboard);
    },

    async loadTickets() {
        const ticketsList = document.getElementById('ticketsList');
        try {
            const spinner = domUtils.createSpinner();
            ticketsList.appendChild(spinner);

            const tickets = await ticketService.getAllTickets();
            domUtils.clearElement(ticketsList);

            if (tickets.length === 0) {
                ticketsList.appendChild(
                    domUtils.createElement('p', { class: 'no-tickets' }, ['No tickets found'])
                );
                return;
            }

            tickets.forEach(ticket => {
                const ticketElement = this.createTicketElement(ticket);
                ticketsList.appendChild(ticketElement);
            });
        } catch (error) {
            domUtils.showError('Failed to load tickets');
            domUtils.clearElement(ticketsList);
            ticketsList.appendChild(
                domUtils.createElement('p', { class: 'error' }, ['Error loading tickets'])
            );
        }
    },

    createTicketElement(ticket) {
        return domUtils.createElement('div', { class: 'ticket-card' }, [
            domUtils.createElement('div', { class: 'ticket-header' }, [
                domUtils.createElement('h3', {}, [`Ticket #${ticket.id}`]),
                domUtils.createElement('span', { 
                    class: `priority priority-${ticket.priority.toLowerCase()}`
                }, [ticket.priority])
            ]),
            domUtils.createElement('div', { class: 'ticket-body' }, [
                domUtils.createElement('p', { class: 'customer' }, [
                    'Customer: ',
                    domUtils.createElement('span', {}, [ticket.customerName])
                ]),
                domUtils.createElement('p', { class: 'issue' }, [ticket.issue]),
                ticket.assignedEngineer ? 
                    domUtils.createElement('p', { class: 'engineer' }, [
                        'Assigned to: ',
                        domUtils.createElement('span', {}, [ticket.assignedEngineer.name])
                    ]) : null
            ]),
            domUtils.createElement('div', { class: 'ticket-actions' }, [
                domUtils.createElement('button', {
                    class: 'btn btn-danger',
                    onclick: () => this.handleDeleteTicket(ticket.id)
                }, ['Delete'])
            ])
        ]);
    },

    attachEventListeners() {
        const form = document.getElementById('createTicketForm');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const customerName = document.getElementById('customerName').value;
            const issue = document.getElementById('issue').value;
            const priority = document.getElementById('priority').value;

            try {
                const spinner = domUtils.createSpinner();
                form.appendChild(spinner);
                form.querySelector('button').disabled = true;

                await ticketService.createTicket(customerName, issue, priority);
                domUtils.showSuccess('Ticket created successfully!');
                form.reset();
                this.loadTickets(); // Reload the tickets list
            } catch (error) {
                domUtils.showError('Failed to create ticket');
            } finally {
                const spinner = form.querySelector('.spinner');
                if (spinner) spinner.remove();
                form.querySelector('button').disabled = false;
            }
        });
    },

    async handleDeleteTicket(ticketId) {
        if (!confirm('Are you sure you want to delete this ticket?')) return;

        try {
            await ticketService.deleteTicket(ticketId);
            domUtils.showSuccess('Ticket deleted successfully!');
            this.loadTickets(); // Reload the tickets list
        } catch (error) {
            domUtils.showError('Failed to delete ticket');
        }
    }
};

export default ticket;