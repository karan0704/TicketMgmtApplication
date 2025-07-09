// customer.js
// Handles customer listing and form submission.

const customerListView = document.getElementById('customer-list-view');
const customerListContainer = document.getElementById('customer-list-container');
const createCustomerBtn = document.getElementById('create-customer-btn');
const createCustomerView = document.getElementById('create-customer-view');
const customerForm = document.getElementById('customer-form');
const cancelCreateCustomerBtn = document.getElementById('cancel-create-customer');

/**
 * Renders the list of customers into the customer list container.
 * @param {Array<Object>} customers - An array of customer objects.
 */
function renderCustomerList(customers) {
    if (customers.length === 0) {
        customerListContainer.innerHTML = '<p class="text-gray-600">No customers found.</p>';
        return;
    }

    let tableHtml = `
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead class="bg-gray-100">
                <tr>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">ID</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Name</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Email</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Company</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Actions</th>
                </tr>
            </thead>
            <tbody>
    `;

    customers.forEach(customer => {
        tableHtml += `
            <tr class="hover:bg-gray-50 transition-colors duration-200">
                <td class="py-3 px-4 border-b text-gray-800">${customer.id}</td>
                <td class="py-3 px-4 border-b text-gray-800">${customer.name}</td>
                <td class="py-3 px-4 border-b text-gray-800">${customer.email}</td>
                <td class="py-3 px-4 border-b text-gray-800">${customer.companyName || 'N/A'}</td>
                <td class="py-3 px-4 border-b">
                    <button data-id="${customer.id}" class="view-customer-detail px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-300 shadow-sm text-sm">
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
    customerListContainer.innerHTML = tableHtml;

    // Add event listeners for "View Details" buttons
    customerListContainer.querySelectorAll('.view-customer-detail').forEach(button => {
        button.addEventListener('click', (e) => {
            const customerId = e.target.dataset.id;
            // In a more complex app, you'd fetch and display customer details here.
            // For now, we'll just show a message.
            showMessage(`Viewing details for customer ID: ${customerId}`, 'info');
            // If you had a customer detail view, you'd navigate to it here:
            // showView('customer-detail-view', customerId);
        });
    });
}

/**
 * Fetches customers from the API and renders the list.
 */
async function fetchAndRenderCustomers() {
    try {
        const customers = await api.getAllCustomers();
        renderCustomerList(customers);
    } catch (error) {
        // Error already handled by api.js
    }
}

// Event Listeners for Customer functionality
createCustomerBtn.addEventListener('click', () => {
    showView('create-customer-view');
    customerForm.reset(); // Clear form fields
});

cancelCreateCustomerBtn.addEventListener('click', () => {
    showView('customer-list-view');
    fetchAndRenderCustomers(); // Refresh list when returning
});

customerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const newCustomer = {
        name: document.getElementById('customer-name').value,
        email: document.getElementById('customer-email').value,
        phoneNumber: document.getElementById('customer-phone').value,
        companyName: document.getElementById('customer-company').value,
    };

    try {
        await api.createCustomer(newCustomer);
        showMessage('Customer created successfully!', 'success');
        showView('customer-list-view');
        fetchAndRenderCustomers(); // Refresh the list
    } catch (error) {
        // Error handled by api.js
    }
});
