import domUtils from '../../utils/domUtils.js';
import userService from '../../services/userService.js';

const register = {
    init() {
        this.renderRegisterForm();
        this.attachEventListeners();
    },

    renderRegisterForm() {
        const container = document.getElementById('main-content');
        domUtils.clearElement(container);

        const form = domUtils.createElement('form', { class: 'auth-form' }, [
            domUtils.createElement('h2', {}, ['Register']),
            domUtils.createElement('div', { class: 'form-group' }, [
                domUtils.createElement('label', { for: 'username' }, ['Username']),
                domUtils.createElement('input', { 
                    type: 'text', 
                    id: 'username', 
                    name: 'username',
                    required: 'true',
                    minlength: '3',
                    maxlength: '20'
                })
            ]),
            domUtils.createElement('div', { class: 'form-group' }, [
                domUtils.createElement('label', { for: 'password' }, ['Password']),
                domUtils.createElement('input', { 
                    type: 'password', 
                    id: 'password', 
                    name: 'password',
                    required: 'true',
                    minlength: '6'
                })
            ]),
            domUtils.createElement('div', { class: 'form-group' }, [
                domUtils.createElement('label', { for: 'confirm-password' }, ['Confirm Password']),
                domUtils.createElement('input', { 
                    type: 'password', 
                    id: 'confirm-password', 
                    name: 'confirm-password',
                    required: 'true'
                })
            ]),
            domUtils.createElement('button', { 
                type: 'submit',
                class: 'btn btn-primary'
            }, ['Register']),
            domUtils.createElement('p', { class: 'auth-switch' }, [
                'Already have an account? ',
                domUtils.createElement('a', { 
                    href: '#/login',
                    class: 'auth-link'
                }, ['Login here'])
            ])
        ]);

        container.appendChild(form);
    },

    validateForm(username, password, confirmPassword) {
        if (password !== confirmPassword) {
            throw new Error('Passwords do not match');
        }
        if (username.length < 3) {
            throw new Error('Username must be at least 3 characters long');
        }
        if (password.length < 6) {
            throw new Error('Password must be at least 6 characters long');
        }
    },

    attachEventListeners() {
        const form = document.querySelector('.auth-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;

            try {
                this.validateForm(username, password, confirmPassword);

                const spinner = domUtils.createSpinner();
                form.appendChild(spinner);
                form.querySelector('button').disabled = true;

                await userService.register(username, password);
                domUtils.showSuccess('Registration successful! Please login.');
                window.location.hash = '#/login';
            } catch (error) {
                domUtils.showError(error.message || 'Registration failed. Please try again.');
            } finally {
                const spinner = form.querySelector('.spinner');
                if (spinner) spinner.remove();
                form.querySelector('button').disabled = false;
            }
        });
    }
};

export default register;