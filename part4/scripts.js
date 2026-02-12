/*
  Part 4 - Simple Web Client
  Task 2: Login
  Task 3: Index (Places list + Price filter + Login link visibility)
  Task 4: Place details (fetch place + reviews + Add Review link visibility)
  Task 5: Add review (submit review, auth required)
*/

// Use same sandbox host, different port (web-80 -> web-5000)
const API_BASE_URL = `${window.location.origin.replace('web-80-', 'web-5000-')}/api/v1`;

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
    if (trimmed.startsWith(target)) return decodeURIComponent(trimmed.slice(target.length));
  }
  return null;
}

// ---------- Common helpers ----------
function authHeaders(token) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

function getQueryParam(key) {
  const params = new URLSearchParams(window.location.search);
  return params.get(key);
}

function setLoginLinkVisibility() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (!loginLink) return;
  loginLink.style.display = token ? 'none' : 'inline-block';
}

// ---------- Task 2: Login ----------
async function loginUser(email, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: authHeaders(null),
    body: JSON.stringify({ email, password })
  });

  let data = null;
  try { data = await response.json(); } catch (_) { data = null; }

  if (!response.ok) {
    const msg = (data && (data.error || data.message)) ? (data.error || data.message) : 'Login failed';
    throw new Error(msg);
  }
  if (!data || !data.access_token) throw new Error('Login failed: no token returned');
  return data.access_token;
}

// ---------- Task 3: Index ----------
function loadPriceFilterOptions() {
  const select = document.getElementById('price-filter');
  if (!select) return;
  select.innerHTML = `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all">All</option>
  `;
  select.value = 'all';
}

async function fetchPlaces(token) {
  const response = await fetch(`${API_BASE_URL}/places/`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  });
  if (!response.ok) throw new Error(`Failed to fetch places: ${response.status} ${response.statusText}`);
  return await response.json();
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) return;
  list.innerHTML = '';

  places.forEach((place) => {
    const card = document.createElement('article');
    card.className = 'place-card';

    const price = Number(place.price_per_night || 0);
    card.dataset.price = String(price);

    card.innerHTML = `
      <h2>${place.name ?? 'Unnamed place'}</h2>
      <p>Price per night: <strong>$${price}</strong></p>
      <a class="details-button" href="place.html?id=${encodeURIComponent(place.id)}">View Details</a>
    `;
    list.appendChild(card);
  });
}

function applyPriceFilter(selectedValue) {
  const cards = document.querySelectorAll('.place-card');
  const maxPrice = selectedValue === 'all' ? null : Number(selectedValue);

  cards.forEach((card) => {
    const price = Number(card.dataset.price || 0);
    card.style.display = (maxPrice === null || price <= maxPrice) ? '' : 'none';
  });
}

// ---------- Task 4: Place details ----------
async function fetchPlace(placeId, token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await fetch(`${API_BASE_URL}/places/${encodeURIComponent(placeId)}`, { headers });
  if (!response.ok) throw new Error(`Failed to fetch place: ${response.status}`);
  return await response.json();
}

async function fetchPlaceReviews(placeId, token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const response = await fetch(`${API_BASE_URL}/places/${encodeURIComponent(placeId)}/reviews`, { headers });
  if (!response.ok) throw new Error(`Failed to fetch reviews: ${response.status}`);
  return await response.json();
}

function renderPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;

  const price = Number(place.price_per_night || 0);
  const amenities = Array.isArray(place.amenities) ? place.amenities : [];

  container.innerHTML = `
    <h2>${place.name ?? 'Place'}</h2>
    <p><strong>Host:</strong> ${place.owner_id ?? 'Unknown'}</p>
    <p><strong>Price per night:</strong> $${price}</p>
    <p><strong>Description:</strong> ${place.description ?? ''}</p>

    <h3>Amenities</h3>
    ${amenities.length ? `<ul>${amenities.map(a => `<li>${a}</li>`).join('')}</ul>` : `<p>No amenities listed.</p>`}
  `;
}

function renderReviews(reviews) {
  const container = document.getElementById('reviews');
  if (!container) return;

  // خلي العنوان موجود لو كان في HTML
  const cards = reviews.map((r) => `
    <article class="review-card">
      <p><strong>User:</strong> ${r.user_id ?? 'Unknown'}</p>
      <p><strong>Rating:</strong> ${r.rating ?? ''}</p>
      <p>${r.text ?? ''}</p>
    </article>
  `).join('');

  container.innerHTML = `
    <h2>Reviews</h2>
    ${reviews.length ? cards : `<p>No reviews yet.</p>`}
  `;
}

function setupAddReviewLink(placeId) {
  const token = getCookie('token');
  const addReviewLink = document.getElementById('add-review-link');
  if (!addReviewLink) return;

  if (!token) {
    // Not logged in: hide button
    addReviewLink.style.display = 'none';
    return;
  }

  addReviewLink.style.display = 'inline-block';
  addReviewLink.href = `add_review.html?place_id=${encodeURIComponent(placeId)}`;
}

// ---------- Task 5: Add review ----------
async function submitReview(token, placeId, text, rating) {
  const response = await fetch(`${API_BASE_URL}/reviews/`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify({ place_id: placeId, text, rating })
  });

  let data = null;
  try { data = await response.json(); } catch (_) { data = null; }

  if (!response.ok) {
    const msg = (data && (data.error || data.message)) ? (data.error || data.message) : 'Failed to submit review';
    throw new Error(msg);
  }
  return data;
}

function fillRatingOptions() {
  const select = document.getElementById('rating');
  if (!select) return;
  if (select.options.length > 1) return; // already filled in HTML
  select.innerHTML = `
    <option value="">Select rating</option>
    <option value="1">1</option>
    <option value="2">2</option>
    <option value="3">3</option>
    <option value="4">4</option>
    <option value="5">5</option>
  `;
}

document.addEventListener('DOMContentLoaded', async () => {
  // ---------- Login page ----------
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

  // ---------- Index page ----------
  const isIndexPage = document.getElementById('places-list') && document.getElementById('price-filter');
  if (isIndexPage) {
    setLoginLinkVisibility();
    loadPriceFilterOptions();

    const token = getCookie('token');
    try {
      const places = await fetchPlaces(token);
      displayPlaces(places);

      const priceFilter = document.getElementById('price-filter');
      priceFilter.addEventListener('change', (event) => applyPriceFilter(event.target.value));

      applyPriceFilter('all');
    } catch (err) {
      console.error(err);
      const list = document.getElementById('places-list');
      if (list) list.innerHTML = `<p>Could not load places.</p>`;
    }
  }

  // ---------- Place details page ----------
  const isPlacePage = document.getElementById('place-details') && document.getElementById('reviews');
  if (isPlacePage) {
    setLoginLinkVisibility();

    const placeId = getQueryParam('id');
    if (!placeId) {
      document.getElementById('place-details').innerHTML = `<p>Invalid place id.</p>`;
      return;
    }

    setupAddReviewLink(placeId);

    const token = getCookie('token');
    try {
      const place = await fetchPlace(placeId, token);
      renderPlaceDetails(place);

      const reviews = await fetchPlaceReviews(placeId, token);
      renderReviews(reviews);
    } catch (err) {
      console.error(err);
      document.getElementById('place-details').innerHTML = `<p>Could not load place details.</p>`;
    }
  }

  // ---------- Add review page ----------
  const reviewForm = document.getElementById('review-form');
  const ratingSelect = document.getElementById('rating');
  const reviewTextarea = document.getElementById('review');
  const placeHint = document.getElementById('place-hint');
  const reviewError = document.getElementById('review-error');

  const isAddReviewPage = reviewForm && ratingSelect && reviewTextarea;
  if (isAddReviewPage) {
    setLoginLinkVisibility();

    const token = getCookie('token');
    if (!token) {
      window.location.href = 'index.html';
      return;
    }

    fillRatingOptions();

    const placeId = getQueryParam('place_id');
    if (placeHint) placeHint.innerHTML = `Reviewing place: <strong>${placeId ?? 'UNKNOWN'}</strong>`;

    if (!placeId) {
      if (reviewError) reviewError.textContent = 'Missing place_id in URL';
      return;
    }

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (reviewError) reviewError.textContent = '';

      const text = reviewTextarea.value.trim();
      const rating = Number(ratingSelect.value);

      if (!text) {
        if (reviewError) reviewError.textContent = 'Review text is required';
        return;
      }
      if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
        if (reviewError) reviewError.textContent = 'Rating must be between 1 and 5';
        return;
      }

      try {
        await submitReview(token, placeId, text, rating);
        window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to submit review';
        if (reviewError) reviewError.textContent = message;
        else alert(message);
      }
    });
  }
});
