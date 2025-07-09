import { Utils } from './utils.js';

export const Validation = {
    validateCustomerForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.name)) {
            errors.name = 'Name is required';
        } else if (!Utils.validateMinLength(formData.name, 2)) {
            errors.name = 'Name must be at least 2 characters';
        }
        if (!Utils.validateRequired(formData.email)) {
            errors.email = 'Email is required';
        } else if (!Utils.validateEmail(formData.email)) {
            errors.email = 'Please enter a valid email address';
        }
        if (formData.phoneNumber && !Utils.validatePhone(formData.phoneNumber)) {
            errors.phoneNumber = 'Please enter a valid phone number';
        }
        if (!Utils.validateRequired(formData.companyName)) {
            errors.companyName = 'Company name is required';
        }
        return errors;
    },

    validateEngineerForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.name)) {
            errors.name = 'Name is required';
        } else if (!Utils.validateMinLength(formData.name, 2)) {
            errors.name = 'Name must be at least 2 characters';
        }
        if (!Utils.validateRequired(formData.email)) {
            errors.email = 'Email is required';
        } else if (!Utils.validateEmail(formData.email)) {
            errors.email = 'Please enter a valid email address';
        }
        if (!Utils.validateRequired(formData.designation)) {
            errors.designation = 'Designation is required';
        } else if (!Utils.validateMinLength(formData.designation, 2)) {
            errors.designation = 'Designation must be at least 2 characters';
        }
        return errors;
    },

    validateTicketForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.customerName)) {
            errors.customerName = 'Customer is required';
        }
        if (!Utils.validateRequired(formData.priority)) {
            errors.priority = 'Priority is required';
        }
        if (!Utils.validateRequired(formData.issue)) {
            errors.issue = 'Issue description is required';
        } else if (!Utils.validateMinLength(formData.issue, 10)) {
            errors.issue = 'Issue description must be at least 10 characters';
        }
        return errors;
    },

    validateFileUploadForm: (formData) => {
        const errors = {};
        if (!Utils.validateRequired(formData.ticketId)) {
            errors.ticketId = 'Ticket ID is required';
        } else if (isNaN(formData.ticketId) || parseInt(formData.ticketId) <= 0) {
            errors.ticketId = 'Ticket ID must be a positive number';
        }
        if (!formData.file) {
            errors.file = 'Please select a file to upload';
        }
        return errors;
    }
};