/* ===== HBnB Part 4 - scripts.js (Flask RESTX + JWT) ===== */

const API_ROOT = "http://127.0.0.1:5000/api/v1";

/* ========= Token (COOKIE first, localStorage fallback) ========= */
const TOKEN_COOKIE = "token";

function getCookie(name) {
  const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return m ? decodeURIComponent(m[2]) : null;
}
function setCookie(name, value, days = 7) {
  const exp = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${exp}; path=/`;
}
function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/`;
}

function getToken() {
  return getCookie(TOKEN_COOKIE) || localStorage.getItem("token");
}
function setToken(t) {
  setCookie(TOKEN_COOKIE, t, 7);
  localStorage.setItem("token", t);
}
function clearToken() {
  deleteCookie(TOKEN_COOKIE);
  localStorage.removeItem("token");
}

/* ========= Helpers ========= */
function qs(id) { return document.getElementById(id); }

function getPlaceIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function stars(rating) {
  const r = Number(rating) || 0;
  const full = "★".repeat(Math.max(0, Math.min(5, r)));
  const empty = "☆".repeat(Math.max(0, 5 - Math.max(0, Math.min(5, r))));
  return full + empty;
}

/* ========= API ========= */
async function apiFetch(path, options = {}) {
  const p = path.startsWith("/") ? path : `/${path}`;
  const url = `${API_ROOT}${p}`;

  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");

  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const token = getToken();
  if (token && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const res = await fetch(url, { ...options, headers });
  return res;
}

async function apiGetJsonWithFallback(pathA, pathB = null) {
  let res = await apiFetch(pathA, { method: "GET" });
  if ((!res.ok || res.status === 404 || res.status === 405) && pathB) {
    res = await apiFetch(pathB, { method: "GET" });
  }
  if (!res.ok) return null;
  return res.json().catch(() => null);
}

async function apiPostJsonWithFallback(pathA, pathB, payload) {
  let res = await apiFetch(pathA, { method: "POST", body: JSON.stringify(payload) });
  if (res.status === 404 || res.status === 405) {
    res = await apiFetch(pathB, { method: "POST", body: JSON.stringify(payload) });
  }
  return res;
}

/* ========= Header login button (Login/Logout) ========= */
function updateLoginButton() {
  const btn = document.querySelector(".login-button");
  if (!btn) return;

  if (getToken()) {
    btn.textContent = "Logout";
    btn.href = "#";
    btn.onclick = (e) => {
      e.preventDefault();
      clearToken();
      window.location.href = "index.html";
    };
  } else {
    btn.textContent = "Login";
    btn.href = "login.html";
    btn.onclick = null;
  }
}

/* ========= Caches ========= */
const userCache = new Map();          // id -> displayName
let amenitiesMap = null;              // id -> name

function nameFromUserObj(u) {
  if (!u || typeof u !== "object") return "";
  const first = u.first_name ?? u.firstName ?? "";
  const last  = u.last_name ?? u.lastName ?? "";
  const full = `${first} ${last}`.trim();
  return full || u.username || u.user_name || u.name || u.email || "";
}

async function getUserNameById(userId) {
  if (!userId) return "";
  if (userCache.has(userId)) return userCache.get(userId);

  // try /users/<id> then /users/<id>/
  const u =
    await apiGetJsonWithFallback(`/users/${encodeURIComponent(userId)}`, `/users/${encodeURIComponent(userId)}/`);

  const display =
    nameFromUserObj(u) ||
    (typeof u === "string" ? u : "") ||
    userId;

  userCache.set(userId, display);
  return display;
}

async function loadAmenitiesMap() {
  if (amenitiesMap) return amenitiesMap;

  // try /amenities/ then /amenities
  const list =
    await apiGetJsonWithFallback("/amenities/", "/amenities");

  const arr = Array.isArray(list) ? list : (list && list.amenities) ? list.amenities : [];
  amenitiesMap = new Map();
  arr.forEach((a) => {
    if (!a) return;
    const id = a.id ?? a.amenity_id;
    const name = a.name ?? a.title;
    if (id && name) amenitiesMap.set(String(id), String(name));
  });

  return amenitiesMap;
}

async function resolveAmenityNames(rawAmenities) {
  if (!rawAmenities) return "";
  const map = await loadAmenitiesMap();

  const arr = Array.isArray(rawAmenities) ? rawAmenities : [rawAmenities];

  const names = arr.map((a) => {
    // object with name
    if (a && typeof a === "object") {
      return a.name ?? a.title ?? a.id ?? "";
    }
    // id string
    const key = String(a);
    return map.get(key) || key;
  }).filter(Boolean);

  return names.join(", ");
}

/* ========= AUTH ========= */
async function handleLoginSubmit(e) {
  e.preventDefault();

  const emailEl = qs("email");
  const passEl = qs("password");
  const errEl = qs("login-error");

  const email = emailEl ? emailEl.value.trim() : "";
  const password = passEl ? passEl.value : "";

  if (errEl) errEl.textContent = "";

  const res = await apiFetch("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });

  if (!res.ok) {
    if (errEl) errEl.textContent = "Login failed (email/password).";
    return;
  }

  const data = await res.json().catch(() => ({}));
  if (!data.access_token) {
    if (errEl) errEl.textContent = "Login failed (no token returned).";
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
    const id = p.id ?? p.place_id ?? p.placeId;

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
  const filtered = cachedPlaces.filter((p) => {
    const price = Number(p.price_per_night ?? p.price ?? p.pricePerNight ?? NaN);
    return Number.isFinite(price) && price <= limit;
  });
  renderPlaces(filtered);
}

async function loadPlaces() {
  const container = qs("places-list");
  if (!container) return;

  const data = await apiGetJsonWithFallback("/places/", "/places");
  if (!data) {
    container.innerHTML = `<div class="error">Failed to load places.</div>`;
    return;
  }

  cachedPlaces = Array.isArray(data) ? data : (data.places || []);
  renderPlaces(cachedPlaces);

  const select = qs("max-price");
  if (select) select.onchange = () => applyMaxPriceFilter(select.value);
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

  const p =
    await apiGetJsonWithFallback(`/places/${encodeURIComponent(placeId)}`, `/places/${encodeURIComponent(placeId)}/`);

  if (!p) {
    if (titleEl) titleEl.textContent = "Place not found";
    return;
  }

  const title = p.title ?? p.name ?? "Untitled";
  const price = p.price_per_night ?? p.price ?? p.pricePerNight ?? "N/A";
  const description = p.description ?? "";

  // host: try direct fields -> user object -> fetch by owner_id/user_id
  let host =
    p.host_name ??
    p.owner_name ??
    p.owner ??
    nameFromUserObj(p.user) ??
    nameFromUserObj(p.owner);

  if (!host) {
    const ownerId = p.owner_id ?? p.user_id ?? p.ownerId ?? p.userId;
    if (ownerId) host = await getUserNameById(String(ownerId));
  }
  if (!host) host = "N/A";

  // amenities: may come as ids -> map them to names
  const amenitiesRaw = p.amenities ?? p.amenity_ids ?? p.amenity_names ?? [];
  const amenitiesText = await resolveAmenityNames(amenitiesRaw);

  if (titleEl) titleEl.textContent = title;
  if (hostEl) hostEl.textContent = host;
  if (priceEl) priceEl.textContent = String(price);
  if (descEl) descEl.textContent = description;
  if (amenEl) amenEl.textContent = amenitiesText;

  await loadReviews(placeId);
  updateAddReviewLink(placeId);
}

/* ========= REVIEWS ========= */
async function loadReviews(placeId) {
  const wrap = qs("reviews-wrap");
  if (!wrap) return;

  const reviews =
    await apiGetJsonWithFallback(`/places/${encodeURIComponent(placeId)}/reviews`, `/places/${encodeURIComponent(placeId)}/reviews/`);

  if (!reviews) {
    wrap.innerHTML = `<div class="error">Failed to load reviews.</div>`;
    return;
  }

  const list = Array.isArray(reviews) ? reviews : (reviews.reviews || []);
  wrap.innerHTML = "";

  if (list.length === 0) {
    wrap.innerHTML = `<div class="review-card"><div class="name">No reviews yet.</div></div>`;
    return;
  }

  for (const r of list) {
    // user name: try fields -> user object -> fetch by user_id
    let user =
      r.user_name ??
      r.username ??
      r.userName ??
      r.name ??
      r.author_name ??
      nameFromUserObj(r.user) ??
      nameFromUserObj(r.author);

    if (!user) {
      const uid = r.user_id ?? r.userId;
      if (uid) user = await getUserNameById(String(uid));
    }
    if (!user) user = "Unknown";

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
  }
}

/* ========= Add Review link only (NO inline form) ========= */
function updateAddReviewLink(placeId) {
  const mustLoginMsg = qs("must-login-msg");
  const linkWrap = qs("add-review-link-wrap");
  const link = qs("add-review-link");

  const loggedIn = !!getToken();

  if (mustLoginMsg) mustLoginMsg.style.display = loggedIn ? "none" : "block";
  if (linkWrap) linkWrap.style.display = loggedIn ? "block" : "none";
  if (link) link.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
}

/* ========= Add Review Page Submit ========= */
async function handleAddReviewPageSubmit(e) {
  e.preventDefault();

  const placeId = getPlaceIdFromUrl();
  if (!placeId) return;

  if (!getToken()) {
    alert("Login first.");
    window.location.href = "login.html";
    return;
  }

  const textEl = qs("review-text");
  const ratingEl = qs("review-rating");

  const text = textEl ? textEl.value.trim() : "";
  const rating = ratingEl ? Number(ratingEl.value) : 1;

  if (!text) {
    alert("Review text is required.");
    return;
  }

  const res = await apiPostJsonWithFallback(
    `/places/${encodeURIComponent(placeId)}/reviews`,
    `/places/${encodeURIComponent(placeId)}/reviews/`,
    { text, rating }
  );

  if (!res.ok) {
    alert("Failed to submit review.");
    return;
  }

  window.location.href = `place.html?id=${encodeURIComponent(placeId)}`;
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
  if (qs("place-title")) loadPlaceDetails();

  // add_review.html
  const addForm = qs("add-review-form");
  if (addForm) addForm.addEventListener("submit", handleAddReviewPageSubmit);
});
