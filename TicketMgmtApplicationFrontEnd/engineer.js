// engineer.js
// Handles engineer listing and form submission.

const engineerListView = document.getElementById('engineer-list-view');
const engineerListContainer = document.getElementById('engineer-list-container');
const createEngineerBtn = document.getElementById('create-engineer-btn');
const createEngineerView = document.getElementById('create-engineer-view');
const engineerForm = document.getElementById('engineer-form');
const cancelCreateEngineerBtn = document.getElementById('cancel-create-engineer');

/**
 * Renders the list of engineers into the engineer list container.
 * @param {Array<Object>} engineers - An array of engineer objects.
 */
function renderEngineerList(engineers) {
    if (engineers.length === 0) {
        engineerListContainer.innerHTML = '<p class="text-gray-600">No engineers found.</p>';
        return;
    }

    let tableHtml = `
        <table class="min-w-full bg-white border border-gray-200 rounded-lg">
            <thead class="bg-gray-100">
                <tr>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">ID</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Name</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Email</th>
                    <th class="py-3 px-4 text-left text-sm font-semibold text-gray-700 border-b">Designation</th>
                </tr>
            </thead>
            <tbody>
    `;

    engineers.forEach(engineer => {
        tableHtml += `
            <tr class="hover:bg-gray-50 transition-colors duration-200">
                <td class="py-3 px-4 border-b text-gray-800">${engineer.id}</td>
                <td class="py-3 px-4 border-b text-gray-800">${engineer.name}</td>
                <td class="py-3 px-4 border-b text-gray-800">${engineer.email}</td>
                <td class="py-3 px-4 border-b text-gray-800">${engineer.designation || 'N/A'}</td>
            </tr>
        `;
    });

    tableHtml += `
            </tbody>
        </table>
    `;
    engineerListContainer.innerHTML = tableHtml;
}

/**
 * Fetches engineers from the API and renders the list.
 */
async function fetchAndRenderEngineers() {
    try {
        const engineers = await api.getAllEngineers();
        renderEngineerList(engineers);
    } catch (error) {
        // Error already handled by api.js
    }
}

// Event Listeners for Engineer functionality
createEngineerBtn.addEventListener('click', () => {
    showView('create-engineer-view');
    engineerForm.reset(); // Clear form fields
});

cancelCreateEngineerBtn.addEventListener('click', () => {
    showView('engineer-list-view');
    fetchAndRenderEngineers(); // Refresh list when returning
});

engineerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const newEngineer = {
        name: document.getElementById('engineer-name').value,
        email: document.getElementById('engineer-email').value,
        designation: document.getElementById('engineer-designation').value,
    };

    try {
        await api.createEngineer(newEngineer);
        showMessage('Engineer created successfully!', 'success');
        showView('engineer-list-view');
        fetchAndRenderEngineers(); // Refresh the list
    } catch (error) {
        // Error handled by api.js
    }
});
