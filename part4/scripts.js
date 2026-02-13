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
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

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

    const response = await fetch('https://your-api-url/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();

        // Store JWT token in cookie
        document.cookie = `token=${data.access_token}; path=/`;

        // Redirect to main page
        window.location.href = 'index.html';

    } else {
        const errorText = await response.text();
        alert('Login failed: ' + errorText);
    }
}
