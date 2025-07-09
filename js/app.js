import login from './features/auth/login.js';
import register from './features/auth/register.js';
import ticket from './features/tickets/ticket.js';
import userService from './services/userService.js';

const app = {
    init() {
        this.setupRouter();
        this.handleInitialRoute();
    },

    routes: {
        '#/login': login,
        '#/register': register,
        '#/tickets': ticket,
        '#/': () => {
            // Redirect to tickets if authenticated, otherwise to login
            if (userService.isAuthenticated()) {
                window.location.hash = '#/tickets';
            } else {
                window.location.hash = '#/login';
            }
        }
    },

    setupRouter() {
        window.addEventListener('hashchange', () => this.handleRoute());
    },

    handleInitialRoute() {
        if (!window.location.hash) {
            window.location.hash = '#/';
        } else {
            this.handleRoute();
        }
    },

    handleRoute() {
        const hash = window.location.hash;
        const route = this.routes[hash];

        if (route) {
            if (typeof route === 'function') {
                route();
            } else if (typeof route.init === 'function') {
                route.init();
            }
        } else {
            // Handle 404 or redirect to default route
            window.location.hash = '#/';
        }
    }
};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => app.init());

export default app;