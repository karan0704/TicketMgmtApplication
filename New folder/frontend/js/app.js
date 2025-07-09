import { App } from './modules/main.js'; // Import the main App object

document.addEventListener('DOMContentLoaded', () => {
    App.Events.init(); // Set up all event listeners
    App.Handlers.showTab('dashboard'); // Load dashboard data by default
});