import { State } from './state.js';

export const UI = {
    displayFormErrors: (errors, formElement) => {
        formElement.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });

        for (const field in errors) {
            const specificErrorElement = formElement.querySelector(`#${formElement.id.replace('Form', '')}${field.charAt(0).toUpperCase() + field.slice(1)}Error`);
            if (specificErrorElement) {
                specificErrorElement.textContent = errors[field];
                specificErrorElement.style.display = 'block';
            }
        }
    },

    clearFormErrors: (formElement) => {
        formElement.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
            el.style.display = 'none';
        });
    },

    showAlert: (message, isSuccess) => {
        const successAlert = document.getElementById('successAlert');
        const errorAlert = document.getElementById('errorAlert');

        successAlert.style.display = 'none';
        errorAlert.style.display = 'none';

        if (isSuccess) {
            successAlert.textContent = message;
            successAlert.style.display = 'block';
        } else {
            errorAlert.textContent = message;
            errorAlert.style.display = 'block';
        }

        setTimeout(() => {
            successAlert.style.display = 'none';
            errorAlert.style.display = 'none';
        }, 5000);
    },

    showLoading: (container) => {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                Loading...
            </div>
        `;
    },

    hideLoading: (container) => {
        container.innerHTML = '';
    },

    openModal: (modalId, title, contentHtml) => {
        const modal = document.getElementById(modalId);
        const modalTitle = modal.querySelector('h2');
        const modalContent = modal.querySelector('div[id$="Content"]');

        modalTitle.textContent = title;
        modalContent.innerHTML = contentHtml;
        modal.classList.add('active');
    },

    closeModal: (modalId) => {
        document.getElementById(modalId).classList.remove('active');
        if (modalId === 'assignEngineerModal' || modalId === 'changeStatusModal') {
            State.currentTicketIdForModal = null;
        }
    }
};