export const Utils = {
    validateEmail: (email) => {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    validatePhone: (phone) => {
        const re = /^[\+]?[\d\s\-\(]{10,}$/;
        return re.test(phone);
    },
    validateRequired: (value) => {
        return value && String(value).trim().length > 0;
    },
    validateMinLength: (value, min) => {
        return value && String(value).trim().length >= min;
    }
};