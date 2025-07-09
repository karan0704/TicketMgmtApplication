// DOM utility functions

const domUtils = {
    // Create an element with attributes and children
    createElement(tag, attributes = {}, children = []) {
        const element = document.createElement(tag);
        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });
        children.forEach(child => {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else {
                element.appendChild(child);
            }
        });
        return element;
    },

    // Show error message
    showError(message, duration = 3000) {
        const errorDiv = this.createElement('div', {
            class: 'error-message',
            style: 'position: fixed; top: 20px; right: 20px; background-color: #ff4444; color: white; padding: 10px; border-radius: 4px; z-index: 1000;'
        }, [message]);
        document.body.appendChild(errorDiv);
        setTimeout(() => errorDiv.remove(), duration);
    },

    // Show success message
    showSuccess(message, duration = 3000) {
        const successDiv = this.createElement('div', {
            class: 'success-message',
            style: 'position: fixed; top: 20px; right: 20px; background-color: #44ff44; color: white; padding: 10px; border-radius: 4px; z-index: 1000;'
        }, [message]);
        document.body.appendChild(successDiv);
        setTimeout(() => successDiv.remove(), duration);
    },

    // Clear all children of an element
    clearElement(element) {
        while (element.firstChild) {
            element.removeChild(element.firstChild);
        }
    },

    // Create a loading spinner
    createSpinner() {
        return this.createElement('div', {
            class: 'spinner',
            style: 'width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite;'
        });
    }
};

export default domUtils;