/*
  Part 4 - Simple Web Client
  Task 2: Login
  Task 3: Index (Places list + Price filter + Login link visibility)
*/

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'; // عدّل لو API عندك مختلف

// ---------- Cookies helpers ----------
function setCookie(name, value, days = 1) {
  const maxAge = days * 24 * 60 * 60;
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; path=/; max-age=${maxAge}`;
}

function getCookie(name) {
  const target = `${encodeURIComponent(name)}=`;
  const parts = document.cookie.split(';');
  for (const part of parts) {
    const trimmed = part.trim();
    if (trimmed.startsWith(target)) {
      return decodeURIComponent(trimmed.slice(target.length));
    }
  }
  return null;
}

// ---------- Task 2: Login ----------
async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  let data = null;
  try { data = await response.json(); } catch (_) { data = null; }

  if (!response.ok) {
    const msg = (data && (data.error || data.message)) ? (data.error || data.message) : 'Login failed';
    throw new Error(msg);
  }

  if (!data || !data.access_token) {
    throw new Error('Login failed: no token returned');
  }

  return data.access_token;
}

// ---------- Task 3: Index ----------
function setLoginLinkVisibility() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (!loginLink) return;

  // Show login link only if NOT authenticated
  loginLink.style.display = token ? 'none' : 'inline-block';
}

function loadPriceFilterOptions() {
  const select = document.getElementById('price-filter');
  if (!select) return;

  // Required options: 10, 50, 100, All
  select.innerHTML = `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all">All</option>
  `;

  // Default to All
  select.value = 'all';
}

async function fetchPlaces(token) {
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}/places/`, { headers });

  if (!response.ok) {
    throw new Error(`Failed to fetch places: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;

  list.innerHTML = '';

  places.forEach((place) => {
    const card = document.createElement('article');
    card.className = 'place-card';

    // نحتاج price للفلترة
    const price = Number(place.price_per_night || 0);
    card.dataset.price = String(price);

    card.innerHTML = `
      <h2>${place.name ?? 'Unnamed place'}</h2>
      <p>Price per night: <strong>$${price}</strong></p>
      <a class="details-button" href="place.html?id=${place.id}">View Details</a>
    `;

    list.appendChild(card);
  });
}

function applyPriceFilter(selectedValue) {
  const cards = document.querySelectorAll('.place-card');
  const maxPrice = selectedValue === 'all' ? null : Number(selectedValue);

  cards.forEach((card) => {
    const price = Number(card.dataset.price || 0);

    if (maxPrice === null) {
      card.style.display = '';
      return;
    }

    card.style.display = price <= maxPrice ? '' : 'none';
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  // --- Login page wiring ---
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    const errorEl = document.getElementById('login-error');

    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (errorEl) errorEl.textContent = '';

      const email = (document.getElementById('email')?.value || '').trim();
      const password = document.getElementById('password')?.value || '';

      try {
        const token = await loginUser(email, password);
        setCookie('token', token, 1);
        window.location.href = 'index.html';
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Login failed';
        if (errorEl) errorEl.textContent = message;
        else alert(message);
      }
    });
  }

  // --- Index page wiring ---
  const isIndexPage = document.getElementById('places-list') && document.getElementById('price-filter');

  if (isIndexPage) {
    setLoginLinkVisibility();
    loadPriceFilterOptions();

    const token = getCookie('token');

    try {
      const places = await fetchPlaces(token);
      displayPlaces(places);

      const priceFilter = document.getElementById('price-filter');
      priceFilter.addEventListener('change', (event) => {
        applyPriceFilter(event.target.value);
      });

      // Apply default filter (All)
      applyPriceFilter('all');
    } catch (err) {
      console.error(err);
      const list = document.getElementById('places-list');
      if (list) list.innerHTML = `<p>Could not load places.</p>`;
    }
  }
});
