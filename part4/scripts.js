/*
  Task 2 - Login
  - Submit login form with Fetch
  - Store JWT in cookie
  - Redirect to index.html on success
*/

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'; // عدّل البورت/الدومين لو مختلف

function setCookie(name, value, days = 1) {
  const maxAge = days * 24 * 60 * 60;
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; path=/; max-age=${maxAge}`;
}

async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  // حتى لو فشل، نحاول نقرأ JSON عشان نجيب error message
  let data = null;
  try {
    data = await response.json();
  } catch (_) {
    data = null;
  }

  if (!response.ok) {
    const msg = (data && (data.error || data.message)) ? (data.error || data.message) : 'Login failed';
    throw new Error(msg);
  }

  if (!data || !data.access_token) {
    throw new Error('Login failed: no token returned');
  }

  return data.access_token;
}

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;

  const errorEl = document.getElementById('login-error');

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (errorEl) errorEl.textContent = '';

    const emailEl = document.getElementById('email');
    const passwordEl = document.getElementById('password');

    const email = emailEl ? emailEl.value.trim() : '';
    const password = passwordEl ? passwordEl.value : '';

    try {
      const token = await loginUser(email, password);

      // Store JWT in cookie for session management
      setCookie('token', token, 1);

      // Redirect to main page
      window.location.href = 'index.html';
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Login failed';
      if (errorEl) {
        errorEl.textContent = message;
      } else {
        alert(message);
      }
    }
  });
});
