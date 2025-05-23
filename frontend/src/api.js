export const API = {
    health: 'http://localhost:8000/health',
    csrf: 'http://localhost:8000/auth/csrf',
    whoami: 'http://localhost:8000/auth/whoami',
    register: 'http://localhost:8000/auth/register',
    login: 'http://localhost:8000/auth/login',
    logout: 'http://localhost:8000/auth/logout',
    update: 'http://localhost:8000/auth/update',
    update_password: 'http://localhost:8000/auth/update-password',
    send_password_reset_email: 'http://localhost:8000/auth/send-password-reset-email',
    reset_password: 'http://localhost:8000/auth/reset-password'
}