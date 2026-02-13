/*
  Login functionality for Holberton HBNB project
  Handles authentication using Fetch API
  Stores JWT token in cookies
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission

            // Get form values
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            if (!email || !password) {
                alert('Please enter both email and password.');
                return;
            }

            try {
                await loginUser(email, password);
            } catch (error) {
                alert('An error occurred: ' + error.message);
            }
        });
    }
});

/*
  Function to send login request to API
*/
async function loginUser(email, password) {

    try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(errorText || 'Login failed');
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
        alert('Login failed: ' + error.message);
    }
}
