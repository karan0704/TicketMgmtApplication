import { UI } from './ui.js';
import { Api } from './api.js';
import { Data } from './data.js';
import { Validation } from './validation.js';

export const Events = {
    init: () => {
        document.getElementById('customerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = {
                name: form.name.value,
                email: form.email.value,
                phoneNumber: form.phoneNumber.value,
                companyName: form.companyName.value
            };

            UI.clearFormErrors(form);
            const errors = Validation.validateCustomerForm(formData);
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                await Api.createCustomer(formData);
                UI.showAlert('Customer added successfully!', true);
                form.reset();
                Data.fetchCustomers();
            } catch (error) {
                UI.showAlert(`Failed to add customer: ${error.message}`, false);
            }
        });

        document.getElementById('engineerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = {
                name: form.name.value,
                email: form.email.value,
                designation: form.designation.value
            };

            UI.clearFormErrors(form);
            const errors = Validation.validateEngineerForm(formData);
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                await Api.createEngineer(formData);
                UI.showAlert('Engineer added successfully!', true);
                form.reset();
                Data.fetchEngineers();
            } catch (error) {
                UI.showAlert(`Failed to add engineer: ${error.message}`, false);
            }
        });

        document.getElementById('ticketForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = {
                customerName: form.customerName.value,
                priority: form.priority.value,
                issue: form.issue.value
            };

            UI.clearFormErrors(form);
            const errors = Validation.validateTicketForm(formData);
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                await Api.createTicket(formData);
                UI.showAlert('Ticket created successfully!', true);
                form.reset();
                Data.fetchAllTickets();
                Data.fetchDashboardStats();
                Data.fetchRecentActivity();
            } catch (error) {
                UI.showAlert(`Failed to create ticket: ${error.message}`, false);
            }
        });

        document.getElementById('fileUploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const ticketId = form.fileTicketId.value;
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];

            UI.clearFormErrors(form);
            const errors = Validation.validateFileUploadForm({ ticketId, file });
            if (Object.keys(errors).length > 0) {
                UI.displayFormErrors(errors, form);
                UI.showAlert('Please correct the errors in the form.', false);
                return;
            }

            try {
                const uploadMessage = document.getElementById('fileSuccess');
                uploadMessage.textContent = 'Uploading...';
                uploadMessage.style.display = 'block';

                const response = await Api.uploadFile(parseInt(ticketId), file);
                if (response.success) {
                    UI.showAlert(response.message, true);
                    uploadMessage.textContent = response.message;
                    form.reset();
                } else {
                    throw new Error(response.message || "Unknown file upload error.");
                }
            } catch (error) {
                const uploadError = document.getElementById('fileError');
                uploadError.textContent = `Failed to upload file: ${error.message}`;
                uploadError.style.display = 'block';
                UI.showAlert(`Failed to upload file: ${error.message}`, false);
            } finally {
                setTimeout(() => {
                    document.getElementById('fileSuccess').style.display = 'none';
                    document.getElementById('fileError').style.display = 'none';
                }, 5000);
            }
        });

        const fileUploadArea = document.getElementById('fileUploadArea');
        const fileInput = document.getElementById('fileInput');

        fileUploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploadArea.classList.add('dragover');
        });

        fileUploadArea.addEventListener('dragleave', () => {
            fileUploadArea.classList.remove('dragover');
        });

        fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploadArea.classList.remove('dragover');
            fileInput.files = e.dataTransfer.files;
            if (fileInput.files.length > 0) {
                const fileNameDisplay = fileUploadArea.querySelector('p');
                fileNameDisplay.textContent = `Selected: ${fileInput.files[0].name}`;
            }
        });
    }
};