/* ===== HBnB Part 4 - scripts.js (API: Flask RESTX + JWT) ===== */

const API_ROOT = "http://127.0.0.1:5000/api/v1";

function getToken() {
  return localStorage.getItem("token");
}
function setToken(t) {
  localStorage.setItem("token", t);
}
function clearToken() {
  localStorage.removeItem("token");
}

function qs(id) {
  return document.getElementById(id);
}

function getPlaceIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function stars(rating) {
  const r = Number(rating) || 0;
  const full = "★".repeat(Math.max(0, Math.min(5, r)));
  const empty = "☆".repeat(Math.max(0, 5 - Math.max(0, Math.min(5, r))));
  return full + empty;
}

async function apiFetch(path, options = {}) {
  const url = `${API_ROOT}${path}`;
  const headers = options.headers ? { ...options.headers } : {};

  // JSON by default if body exists
  if (options.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  // Add JWT if exists
  const token = getToken();
  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(url, { ...options, headers });
  return res;
}

/* ========= Header login button (show Login/Logout) ========= */
function updateLoginButton() {
  const btn = document.querySelector(".login-button");
  if (!btn) return;

  if (getToken()) {
    btn.textContent = "Logout";
    btn.href = "#";
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      clearToken();
      window.location.href = "index.html";
    });
  } else {
    btn.textContent = "Login";
    btn.href = "login.html";
  }
}

/* ========= AUTH ========= */
async function handleLoginSubmit(e) {
  e.preventDefault();

  const email = qs("email").value.trim();
  const password = qs("password").value;

  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });

  if (!res.ok) {
    const err = qs("login-error");
    if (err) err.textContent = "Login failed (email/password).";
    return;
  }

  const data = await res.json();
  if (!data.access_token) {
    const err = qs("login-error");
    if (err) err.textContent = "Login failed (no token returned).";
    return;
  }

  setToken(data.access_token);
  window.location.href = "index.html";
}

/* ========= PLACES ========= */
let cachedPlaces = [];

function renderPlaces(list) {
  const container = qs("places-list");
  if (!container) return;

  container.innerHTML = "";

  list.forEach((p) => {
    const title = p.title ?? p.name ?? "Untitled";
    const price = p.price_per_night ?? p.price ?? p.pricePerNight ?? "N/A";
    const id = p.id ?? p.place_id;

    const card = document.createElement("div");
    card.className = "place-card";
    card.innerHTML = `
      <h3>${escapeHtml(title)}</h3>
      <p>Price per night: $${escapeHtml(String(price))}</p>
      <a class="details-button" href="place.html?id=${encodeURIComponent(id)}">View Details</a>
    `;
    container.appendChild(card);
  });
}

function applyMaxPriceFilter(maxPrice) {
  if (!maxPrice || maxPrice === "All") {
    renderPlaces(cachedPlaces);
    return;
  }
  const limit = Number(maxPrice);
  const filtered = cachedPlaces.filter(p => {
    const price = Number(p.price_per_night ?? p.price ?? p.pricePerNight ?? NaN);
    return Number.isFinite(price) && price <= limit;
  });
  renderPlaces(filtered);
}

async function loadPlaces() {
  const container = qs("places-list");
  if (!container) return;

  const res = await apiFetch("/places/", { method: "GET" });
  if (!res.ok) {
    container.innerHTML = `<div class="error">Failed to load places.</div>`;
    return;
  }

  const data = await res.json();
  cachedPlaces = Array.isArray(data) ? data : (data.places || []);

  renderPlaces(cachedPlaces);

  const select = qs("max-price");
  if (select) {
    select.addEventListener("change", () => applyMaxPriceFilter(select.value));
  }
}

/* ========= PLACE DETAILS ========= */
async function loadPlaceDetails() {
  const placeId = getPlaceIdFromUrl();
  if (!placeId) return;

  const titleEl = qs("place-title");
  const hostEl = qs("place-host");
  const priceEl = qs("place-price");
  const descEl = qs("place-description");
  const amenEl = qs("place-amenities");

  const res = await apiFetch(`/places/${encodeURIComponent(placeId)}`, { method: "GET" });
  if (!res.ok) {
    if (titleEl) titleEl.textContent = "Place not found";
    return;
  }

  const p = await res.json();

  const title = p.title ?? p.name ?? "Untitled";
  const price = p.price_per_night ?? p.price ?? p.pricePerNight ?? "N/A";
  const description = p.description ?? "";
  const amenities = p.amenities ?? p.amenity_names ?? [];
  const host =
    p.host_name ??
    p.owner_name ??
    p.owner ??
    (p.user ? `${p.user.first_name ?? ""} ${p.user.last_name ?? ""}`.trim() : "") ||
    "N/A";

  if (titleEl) titleEl.textContent = title;
  if (hostEl) hostEl.textContent = host;
  if (priceEl) priceEl.textContent = String(price);
  if (descEl) descEl.textContent = description;

  if (amenEl) {
    if (Array.isArray(amenities)) amenEl.textContent = amenities.map(a => a.name ?? a).join(", ");
    else amenEl.textContent = String(amenities);
  }

  await loadReviews(placeId);
  updateAddReviewVisibility(placeId);
}

/* ========= REVIEWS ========= */
async function loadReviews(placeId) {
  const wrap = qs("reviews-wrap");
  if (!wrap) return;

  const res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews`, { method: "GET" });
  if (!res.ok) {
    wrap.innerHTML = `<div class="error">Failed to load reviews.</div>`;
    return;
  }

  const reviews = await res.json();
  const list = Array.isArray(reviews) ? reviews : (reviews.reviews || []);

  wrap.innerHTML = "";

  if (list.length === 0) {
    wrap.innerHTML = `<div class="review-card"><div class="name">No reviews yet.</div></div>`;
    return;
  }

  list.forEach((r) => {
    const user =
      r.user_name ??
      r.username ??
      (r.user ? `${r.user.first_name ?? ""} ${r.user.last_name ?? ""}`.trim() : "") ||
      r.user_id ||
      "Unknown";

    const text = r.text ?? r.comment ?? "";
    const rating = r.rating ?? 0;

    const card = document.createElement("div");
    card.className = "review-card";
    card.innerHTML = `
      <div class="name">${escapeHtml(user)}:</div>
      <div>${escapeHtml(text)}</div>
      <div class="line">Rating: <span class="stars">${escapeHtml(stars(rating))}</span></div>
    `;
    wrap.appendChild(card);
  });
}

function updateAddReviewVisibility(placeId) {
  const addWrap = qs("add-review-wrap");
  const mustLoginMsg = qs("must-login-msg");
  const addLink = qs("add-review-link");

  const loggedIn = !!getToken();

  if (addWrap) addWrap.style.display = loggedIn ? "block" : "none";
  if (mustLoginMsg) mustLoginMsg.style.display = loggedIn ? "none" : "block";

  // if you want a separate page: add_review.html
  if (addLink) addLink.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
}

async function handleReviewSubmit(e) {
  e.preventDefault(); // ✅ يمنع 501 (form submit إلى السيرفر static)

  const placeId = getPlaceIdFromUrl();
  if (!placeId) return;

  const text = qs("review-text").value.trim();
  const rating = Number(qs("review-rating").value);

  if (!text) return;

  // حاول بدون slash أولاً (هذا اللي نبيه)
  let res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews`, {
    method: "POST",
    body: JSON.stringify({ text, rating })
  });

  // لو 405 بسبب routing عندك (trailing slash) جرّب fallback مرة وحدة
  if (res.status === 405) {
    res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews/`, {
      method: "POST",
      body: JSON.stringify({ text, rating })
    });
  }

  if (!res.ok) {
    alert("Failed to submit review.");
    return;
  }

  // reload reviews
  qs("review-text").value = "";
  qs("review-rating").value = "1";
  await loadReviews(placeId);
}

/* ========= Add Review Page ========= */
async function handleAddReviewPageSubmit(e) {
  e.preventDefault();

  const placeId = getPlaceIdFromUrl();
  if (!placeId) return;

  const text = qs("review-text").value.trim();
  const rating = Number(qs("review-rating").value);

  let res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews`, {
    method: "POST",
    body: JSON.stringify({ text, rating })
  });

  if (res.status === 405) {
    res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews/`, {
      method: "POST",
      body: JSON.stringify({ text, rating })
    });
  }

  if (!res.ok) {
    alert("Failed to submit review.");
    return;
  }

  window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
}

/* ========= Utils ========= */
function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

/* ========= Boot ========= */
document.addEventListener("DOMContentLoaded", () => {
  updateLoginButton();

  // index.html
  if (qs("places-list")) loadPlaces();

  // login.html
  const loginForm = qs("login-form");
  if (loginForm) loginForm.addEventListener("submit", handleLoginSubmit);

  // place.html
  if (qs("place-title")) {
    loadPlaceDetails();
    const reviewForm = qs("review-form");
    if (reviewForm) reviewForm.addEventListener("submit", handleReviewSubmit);
  }

  // add_review.html
  const addForm = qs("add-review-form");
  if (addForm) addForm.addEventListener("submit", handleAddReviewPageSubmit);
});
