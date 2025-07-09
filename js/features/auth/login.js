import domUtils from '../../utils/domUtils.js';
import userService from '../../services/userService.js';

const login = {
    init() {
        this.renderLoginForm();
        this.attachEventListeners();
    },

    renderLoginForm() {
        const container = document.getElementById('main-content');
        domUtils.clearElement(container);

        const form = domUtils.createElement('form', { class: 'auth-form' }, [
            domUtils.createElement('h2', {}, ['Login']),
            domUtils.createElement('div', { class: 'form-group' }, [
                domUtils.createElement('label', { for: 'username' }, ['Username']),
                domUtils.createElement('input', { 
                    type: 'text', 
                    id: 'username', 
                    name: 'username',
                    required: 'true'
                })
            ]),
            domUtils.createElement('div', { class: 'form-group' }, [
                domUtils.createElement('label', { for: 'password' }, ['Password']),
                domUtils.createElement('input', { 
                    type: 'password', 
                    id: 'password', 
                    name: 'password',
                    required: 'true'
                })
            ]),
            domUtils.createElement('button', { 
                type: 'submit',
                class: 'btn btn-primary'
            }, ['Login']),
            domUtils.createElement('p', { class: 'auth-switch' }, [
                'Don\'t have an account? ',
                domUtils.createElement('a', { 
                    href: '#/register',
                    class: 'auth-link'
                }, ['Register here'])
            ])
        ]);

        container.appendChild(form);
    },

    attachEventListeners() {
        const form = document.querySelector('.auth-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            try {
                const spinner = domUtils.createSpinner();
                form.appendChild(spinner);
                form.querySelector('button').disabled = true;

                await userService.login(username, password);
                domUtils.showSuccess('Login successful!');
                window.location.hash = '#/dashboard';
            } catch (error) {
                domUtils.showError('Login failed. Please check your credentials.');
            } finally {
                const spinner = form.querySelector('.spinner');
                if (spinner) spinner.remove();
                form.querySelector('button').disabled = false;
            }
        });
    }
};

export default login;