/*login.js
/*
  Login functionality for Holberton HBNB project
  Handles authentication using Fetch API
  Stores JWT token in cookies
*/
/*
  Login functionality for Holberton HBNB project
  Handles authentication using Fetch API
  Stores JWT token in cookies
*/

const API_BASE_URL = 'http://localhost:5000/api/v1'; // Change to your API URL

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            const errorMessage = document.getElementById('error-message');

            if (!email || !password) {
                errorMessage.textContent = 'Please enter both email and password.';
                return;
            }

            try {
                await loginUser(email, password);
            } catch (error) {
                errorMessage.textContent = 'Login failed: ' + error.message;
            }
        });
    }
});

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || `HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (!data.access_token) {
            throw new Error('No token received from server');
        }

        // Store JWT token in cookie (valid for 1 hour)
        document.cookie = `token=${data.access_token}; path=/; max-age=3600`;

        // Redirect to index page
        window.location.href = 'index.html';

    } catch (error) {
        throw error;
    }
}