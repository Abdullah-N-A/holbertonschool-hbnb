// scripts.js

// ----------- Welcome message when the page loads -----------
window.addEventListener('load', function() {
    console.log("Welcome to Holberton HBNB!");
});

// ----------- Hover effect on the login button -----------
const loginBtn = document.querySelector('.login-button');
if (loginBtn) {
    loginBtn.addEventListener('mouseover', () => {
        loginBtn.style.backgroundColor = '#2980b9'; // Darker blue on hover
    });
    loginBtn.addEventListener('mouseout', () => {
        loginBtn.style.backgroundColor = '#3498db'; // Original color
    });
}

// ----------- Alert when clicking "View Details" buttons -----------
const detailsBtns = document.querySelectorAll('.details-button');
detailsBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        alert("Redirecting to place details...");
    });
});

// ----------- Form validation example for login form -----------
const loginForm = document.querySelector('form');
if (loginForm && loginForm.querySelector('input[name="email"]') && loginForm.querySelector('input[name="password"]')) {
    loginForm.addEventListener('submit', (e) => {
        const email = loginForm.querySelector('input[name="email"]').value;
        const password = loginForm.querySelector('input[name="password"]').value;

        // Prevent submission if email or password is empty
        if (email.trim() === '' || password.trim() === '') {
            e.preventDefault(); // Stop the form from submitting
            alert("Please fill in both email and password!");
        }
    });
}
