// User Service for handling user-related operations
import { apiService } from './apiService.js';

class UserService {
    constructor() {
        this.currentUser = null;
    }

    async login(username, password) {
        try {
            const data = await apiService.login(username, password);
            this.currentUser = await this.getCurrentUser();
            return data;
        } catch (error) {
            throw new Error('Login failed: ' + error.message);
        }
    }

    async register(username, password, role) {
        try {
            return await apiService.register(username, password, role);
        } catch (error) {
            throw new Error('Registration failed: ' + error.message);
        }
    }

    async logout() {
        try {
            await apiService.logout();
            this.currentUser = null;
        } catch (error) {
            throw new Error('Logout failed: ' + error.message);
        }
    }

    async getCurrentUser() {
        try {
            if (!this.isAuthenticated()) {
                return null;
            }
            return await apiService.getCurrentUser();
        } catch (error) {
            throw new Error('Failed to fetch current user: ' + error.message);
        }
    }

    isAuthenticated() {
        return !!localStorage.getItem('token');
    }

    async updateProfile(userId, userData) {
        try {
            const updatedUser = await apiService.updateUser(userId, userData);
            if (this.currentUser && this.currentUser.id === userId) {
                this.currentUser = updatedUser;
            }
            return updatedUser;
        } catch (error) {
            throw new Error('Failed to update profile: ' + error.message);
        }
    }
}

export const userService = new UserService();