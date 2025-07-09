// ticket.js
// Handles ticket listing, creation, and detail view.

const ticketListView = document.getElementById('ticket-list-view');
const ticketListContainer = document.getElementById('ticket-list-container');
const createTicketBtn = document.getElementById('create-ticket-btn');
const createTicketView = document.getElementById('create-ticket-view');
const ticketForm = document.getElementById('ticket-form');
const cancelCreateTicketBtn = document.getElementById('cancel-create-ticket');
const ticketPrioritySelect = document.getElementById('ticket-priority');
const ticketDetailView = document.getElementById('ticket-detail-view');

let currentTicketId = null; // To store the ID of the ticket currently being viewed

/**
 * Populates the priority dropdown in the ticket creation form.
 */
function populateTicketPriorityDropdown() {
    ticketPrioritySelect.innerHTML = ''; // Clear existing options
    for (const priority in TicketPriority) {
        const option = document.createElement('option');
        option.value = TicketPriority[priority];
        option.textContent = TicketPriority[priority];
        ticketPrioritySelect.appendChild(option);
    }
}

/**
 * Renders the list of tickets into the ticket list container.
 * @param {Array<Object>} tickets - An array of ticket objects.
 */
function renderTicketList(tickets) {
    if (tickets.length === 0) {
        ticketListContainer.innerHTML = '<p class="text-gray-600">No tickets found.</p>';
        return;
    }

    let tableHtml = `
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead class="bg-gray-100">
                <tr>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">ID</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Customer</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Issue</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Status</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Priority</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Assigned To</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Actions</th>
                </tr>
            </thead>
            <tbody>
    `;

    tickets.forEach(ticket => {
        tableHtml += `
            <tr class="hover:bg-gray-50 transition-colors duration-200">
                <td class="py-3 px-4 border-b text-gray-800">${ticket.id}</td>
                <td class="py-3 px-4 border-b text-gray-800">${ticket.customerName}</td>
                <td class="py-3 px-4 border-b text-gray-800">${ticket.issueDescription}</td>
                <td class="py-3 px-4 border-b text-gray-800">${ticket.ticketStatus}</td>
                <td class="py-3 px-4 border-b text-gray-800">${ticket.priority}</td>
                <td class="py-3 px-4 border-b text-gray-800">${ticket.assignedEngineer?.name || 'Unassigned'}</td>
                <td class="py-3 px-4 border-b">
                    <button data-id="${ticket.id}" class="view-ticket-detail px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-300 shadow-sm text-sm">
                        View Details
                    </button>
                </td>
            </tr>
        `;
    });

    tableHtml += `
            </tbody>
        </table>
    `;
    ticketListContainer.innerHTML = tableHtml;

    // Add event listeners for "View Details" buttons
    ticketListContainer.querySelectorAll('.view-ticket-detail').forEach(button => {
        button.addEventListener('click', (e) => {
            const ticketId = e.target.dataset.id;
            currentTicketId = ticketId; // Store the ID
            showView('ticket-detail-view');
            renderTicketDetail(ticketId); // Render the detail view
        });
    });
}

/**
 * Fetches tickets from the API and renders the list.
 */
async function fetchAndRenderTickets() {
    try {
        const tickets = await api.getAllTickets();
        renderTicketList(tickets);
    } catch (error) {
        // Error already handled by api.js
    }
}

/**
 * Renders the detail view for a specific ticket.
 * @param {number} ticketId - The ID of the ticket to display.
 */
async function renderTicketDetail(ticketId) {
    ticketDetailView.innerHTML = `
        <div class="p-6 bg-white rounded-lg shadow-xl text-center text-gray-600">
            Loading ticket details...
        </div>
    `; // Show loading message

    try {
        const ticket = await api.getTicketById(ticketId);
        const engineers = await api.getAllEngineers();
        const attachedFiles = await api.getFilesByTicket(ticketId);

        if (!ticket) {
            ticketDetailView.innerHTML = `
                <div class="p-6 bg-white rounded-lg shadow-xl text-center text-gray-600">
                    Ticket not found.
                    <button id="back-to-tickets-from-detail" class="mt-4 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors duration-300 shadow-md">
                        Back to Tickets
                    </button>
                </div>
            `;
            document.getElementById('back-to-tickets-from-detail').addEventListener('click', () => {
                showView('ticket-list-view');
                fetchAndRenderTickets();
            });
            return;
        }

        const auditLogsHtml = ticket.auditLogs && ticket.auditLogs.length > 0
            ? `<ul class="list-disc list-inside space-y-1 text-gray-700">
                ${ticket.auditLogs.map(log => `<li><span class="font-mono text-xs text-gray-500">${log.timestamp}</span>: ${log.message}</li>`).join('')}
               </ul>`
            : '<p class="text-gray-600">No audit logs available.</p>';

        const attachedFilesHtml = attachedFiles && attachedFiles.length > 0
            ? `<ul class="list-disc list-inside space-y-1 text-gray-700">
                ${attachedFiles.map(file => `<li>${file.fileName} (<a href="${file.filePath}" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">Download</a>)</li>`).join('')}
               </ul>`
            : '<p class="text-gray-600">No files attached.</p>';

        let engineerOptionsHtml = '<option value="">Select Engineer</option>';
        engineers.forEach(eng => {
            const selected = (ticket.assignedEngineer?.id === eng.id) ? 'selected' : '';
            engineerOptionsHtml += `<option value="${eng.id}" ${selected}>${eng.name} (${eng.designation})</option>`;
        });

        ticketDetailView.innerHTML = `
            <h2 class="text-3xl font-bold mb-6 text-gray-800">Ticket Details (ID: ${ticket.id})</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
                    <h3 class="text-xl font-semibold mb-3 text-gray-700">Basic Information</h3>
                    <p class="mb-2"><strong class="text-gray-700">Customer:</strong> ${ticket.customerName}</p>
                    <p class="mb-2"><strong class="text-gray-700">Issue:</strong> ${ticket.issueDescription}</p>
                    <p class="mb-2"><strong class="text-gray-700">Status:</strong> <span class="font-medium px-2 py-1 rounded-full text-sm ${
                        ticket.ticketStatus === TicketStatus.RESOLVED ? 'bg-green-100 text-green-800' :
                        ticket.ticketStatus === TicketStatus.CLOSED ? 'bg-red-100 text-red-800' :
                        'bg-blue-100 text-blue-800'
                    }">${ticket.ticketStatus}</span></p>
                    <p class="mb-2"><strong class="text-gray-700">Priority:</strong> <span class="font-medium px-2 py-1 rounded-full text-sm ${
                        ticket.priority === TicketPriority.CRITICAL ? 'bg-red-100 text-red-800' :
                        ticket.priority === TicketPriority.HIGH ? 'bg-orange-100 text-orange-800' :
                        'bg-gray-100 text-gray-800'
                    }">${ticket.priority}</span></p>
                    <p class="mb-2"><strong class="text-gray-700">Assigned Engineer:</strong> ${ticket.assignedEngineer?.name || 'Unassigned'}</p>
                    ${ticket.ticketResponse ? `<p class="mb-2"><strong class="text-gray-700">Response:</strong> ${ticket.ticketResponse}</p>` : ''}
                </div>

                <div class="bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
                    <h3 class="text-xl font-semibold mb-3 text-gray-700">Assign Engineer</h3>
                    <div class="flex flex-col space-y-3">
                        <select id="assign-engineer-select" class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                            ${engineerOptionsHtml}
                        </select>
                        <div class="flex space-x-2">
                            <button id="assign-ticket-btn" class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-300 shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                                Assign
                            </button>
                            <button id="unassign-ticket-btn" class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-300 shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                                Unassign
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mb-6 bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
                <h3 class="text-xl font-semibold mb-3 text-gray-700">Audit Logs</h3>
                ${auditLogsHtml}
            </div>

            <div class="mb-6 bg-gray-50 p-4 rounded-lg shadow-sm border border-gray-200">
                <h3 class="text-xl font-semibold mb-3 text-gray-700">Attached Files</h3>
                <div class="flex flex-col md:flex-row items-center space-y-3 md:space-y-0 md:space-x-4 mb-4">
                    <input type="file" id="file-upload-input" class="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                    <button id="upload-file-btn" class="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors duration-300 shadow-md disabled:opacity-50 disabled:cursor-not-allowed w-full md:w-auto">
                        Upload File
                    </button>
                </div>
                <div id="attached-files-list">
                    ${attachedFilesHtml}
                </div>
            </div>

            <button id="back-to-tickets-from-detail" class="mt-6 px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors duration-300 shadow-md">
                Back to Tickets List
            </button>
        `;

        // Add event listeners for the new elements in the detail view
        document.getElementById('assign-ticket-btn').addEventListener('click', async () => {
            const selectedEngineerId = document.getElementById('assign-engineer-select').value;
            if (!selectedEngineerId) {
                showMessage('Please select an engineer to assign.', 'error');
                return;
            }
            try {
                await api.assignTicket(ticket.id, parseInt(selectedEngineerId));
                showMessage('Ticket assigned successfully!', 'success');
                renderTicketDetail(ticket.id); // Re-render to show updated assignment
            } catch (error) {
                // Error handled by api.js
            }
        });

        document.getElementById('unassign-ticket-btn').addEventListener('click', async () => {
            try {
                await api.unassignTicket(ticket.id);
                showMessage('Ticket unassigned successfully!', 'success');
                renderTicketDetail(ticket.id); // Re-render to show updated assignment
            } catch (error) {
                // Error handled by api.js
            }
        });

        const fileUploadInput = document.getElementById('file-upload-input');
        const uploadFileBtn = document.getElementById('upload-file-btn');
        let fileToUpload = null;

        fileUploadInput.addEventListener('change', (e) => {
            fileToUpload = e.target.files[0];
            uploadFileBtn.disabled = !fileToUpload;
        });

        uploadFileBtn.addEventListener('click', async () => {
            if (!fileToUpload) {
                showMessage('Please select a file to upload.', 'error');
                return;
            }
            try {
                await api.uploadFile(fileToUpload, ticket.id);
                showMessage('File uploaded successfully!', 'success');
                fileToUpload = null;
                fileUploadInput.value = ''; // Clear the file input
                uploadFileBtn.disabled = true;
                // Re-fetch and render attached files
                const updatedFiles = await api.getFilesByTicket(ticket.id);
                document.getElementById('attached-files-list').innerHTML = updatedFiles && updatedFiles.length > 0
                    ? `<ul class="list-disc list-inside space-y-1 text-gray-700">
                        ${updatedFiles.map(file => `<li>${file.fileName} (<a href="${file.filePath}" target="_blank" rel="noopener noreferrer" class="text-blue-500 hover:underline">Download</a>)</li>`).join('')}
                       </ul>`
                    : '<p class="text-gray-600">No files attached.</p>';

            } catch (error) {
                // Error handled by api.js
            }
        });

        document.getElementById('back-to-tickets-from-detail').addEventListener('click', () => {
            showView('ticket-list-view');
            fetchAndRenderTickets();
        });

    } catch (error) {
        ticketDetailView.innerHTML = `
            <div class="p-6 bg-white rounded-lg shadow-xl text-center text-red-600">
                Error loading ticket details: ${error.message}
                <button id="back-to-tickets-from-detail-error" class="mt-4 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors duration-300 shadow-md">
                    Back to Tickets
                </button>
            </div>
        `;
        document.getElementById('back-to-tickets-from-detail-error').addEventListener('click', () => {
            showView('ticket-list-view');
            fetchAndRenderTickets();
        });
    }
}


// Event Listeners for Ticket functionality
createTicketBtn.addEventListener('click', () => {
    showView('create-ticket-view');
    ticketForm.reset(); // Clear form fields
    populateTicketPriorityDropdown(); // Ensure dropdown is populated
});

cancelCreateTicketBtn.addEventListener('click', () => {
    showView('ticket-list-view');
    fetchAndRenderTickets(); // Refresh list when returning
});

ticketForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const customerName = document.getElementById('ticket-customer-name').value;
    const issue = document.getElementById('ticket-issue').value;
    const priority = document.getElementById('ticket-priority').value;

    try {
        await api.createTicket(customerName, issue, priority);
        showMessage('Ticket created successfully!', 'success');
        showView('ticket-list-view');
        fetchAndRenderTickets(); // Refresh the list
    } catch (error) {
        // Error handled by api.js
    }
});
