/* ===== HBnB Part 4 - scripts.js (Flask RESTX + JWT) ===== */

const API_ROOT = "http://127.0.0.1:5000/api/v1";

/* ========= Cookie (required by checklist) ========= */
function setCookie(name, value, days = 1) {
  const maxAge = days * 24 * 60 * 60;
  document.cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}; Path=/; Max-Age=${maxAge}; SameSite=Lax`;
}
function getCookie(name) {
  const key = `${encodeURIComponent(name)}=`;
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith(key))
    ?.slice(key.length) ?? null;
}
function deleteCookie(name) {
  document.cookie = `${encodeURIComponent(name)}=; Path=/; Max-Age=0; SameSite=Lax`;
}

/* ========= Token Storage (cookie first) ========= */
function getToken() {
  return getCookie("token");
}
function setToken(t) {
  setCookie("token", t, 1);
}
function clearToken() {
  deleteCookie("token");
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

/* ========= API Fetch ========= */
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

  let res;
  try {
    res = await fetch(url, { ...options, headers });
  } catch (err) {
    console.error("FETCH FAILED:", url, err);
    throw err;
  }

  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    console.error("API ERROR:", res.status, res.statusText, url, txt);
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

  // ✅ Checklist: store token in COOKIE
  setToken(data.access_token);

  window.location.href = "index.html";
}

/* ========= PLACES ========= */
let cachedPlaces = [];

function getCountryFromPlace(p) {
  // Try common field names (robust)
  return (
    p.country ??
    p.country_name ??
    p.countryName ??
    p.location?.country ??
    p.address?.country ??
    null
  );
}

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

function populateCountryFilter() {
  const select = qs("country-filter");
  if (!select) return;

  const countries = cachedPlaces
    .map(getCountryFromPlace)
    .filter(Boolean)
    .map((c) => String(c).trim())
    .filter((c) => c.length > 0);

  const unique = Array.from(new Set(countries)).sort((a, b) => a.localeCompare(b));

  // reset options
  select.innerHTML = `<option value="All">All</option>`;

  unique.forEach((c) => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    select.appendChild(opt);
  });

  // لو API ما فيه country نهائيًا، نخلي الفلتر موجود لكن ما يضيف شيء غير All
}

function applyCountryFilter(selected) {
  if (!selected || selected === "All") {
    renderPlaces(cachedPlaces);
    return;
  }
  const filtered = cachedPlaces.filter((p) => {
    const c = getCountryFromPlace(p);
    return c && String(c).trim() === selected;
  });
  renderPlaces(filtered);
}

async function loadPlaces() {
  const container = qs("places-list");
  if (!container) return;

  let res = await apiFetch("/places/", { method: "GET" });
  if (res.status === 404 || res.status === 405) {
    res = await apiFetch("/places", { method: "GET" });
  }

  if (!res.ok) {
    container.innerHTML = `<div class="error">Failed to load places.</div>`;
    return;
  }

  const data = await res.json().catch(() => []);
  cachedPlaces = Array.isArray(data) ? data : (data.places || []);

  renderPlaces(cachedPlaces);

  // ✅ Checklist: filtering by country
  populateCountryFilter();
  const select = qs("country-filter");
  if (select) select.onchange = () => applyCountryFilter(select.value);
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

  const p = await res.json().catch(() => ({}));

  const title = p.title ?? p.name ?? "Untitled";
  const price = p.price_per_night ?? p.price ?? p.pricePerNight ?? "N/A";
  const description = p.description ?? "";
  const amenities = p.amenities ?? p.amenity_names ?? [];

  let host = p.host_name ?? p.owner_name ?? p.owner;
  if (!host) {
    host = (
      (p.user && typeof p.user === "object"
        ? `${p.user.first_name ?? ""} ${p.user.last_name ?? ""}`.trim()
        : "") ||
      p.user_id ||
      "N/A"
    );
  }

  if (titleEl) titleEl.textContent = title;
  if (hostEl) hostEl.textContent = host;
  if (priceEl) priceEl.textContent = String(price);
  if (descEl) descEl.textContent = description;

  if (amenEl) {
    if (Array.isArray(amenities)) amenEl.textContent = amenities.map(a => a.name ?? a).join(", ");
    else amenEl.textContent = String(amenities);
  }

  await loadReviews(placeId);
  updateAddReviewLink(placeId);
}

/* ========= REVIEWS ========= */
async function loadReviews(placeId) {
  const wrap = qs("reviews-wrap");
  if (!wrap) return;

  let res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews`, { method: "GET" });
  if (res.status === 404 || res.status === 405) {
    res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews/`, { method: "GET" });
  }

  if (!res.ok) {
    wrap.innerHTML = `<div class="error">Failed to load reviews.</div>`;
    return;
  }

  const reviews = await res.json().catch(() => []);
  const list = Array.isArray(reviews) ? reviews : (reviews.reviews || []);

  wrap.innerHTML = "";

  if (list.length === 0) {
    wrap.innerHTML = `<div class="review-card"><div class="name">No reviews yet.</div></div>`;
    return;
  }

  list.forEach((r) => {
    const userObj =
      (r && typeof r.user === "object" && r.user) ? r.user :
      (r && typeof r.author === "object" && r.author) ? r.author :
      null;

    const fullNameFromObj = userObj
      ? `${userObj.first_name ?? userObj.firstName ?? ""} ${userObj.last_name ?? userObj.lastName ?? ""}`.trim()
      : "";

    let user =
      r.user_name ??
      r.username ??
      r.userName ??
      fullNameFromObj;

    if (!user) {
      user =
        (typeof r.user === "string" ? r.user : null) ||
        r.user_id ||
        r.userId ||
        "Unknown";
    }

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

/* ========= Add Review link only ========= */
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
async function postReview(placeId, payload) {
  let res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews`, {
    method: "POST",
    body: JSON.stringify(payload)
  });
  if (res.status === 404 || res.status === 405) {
    res = await apiFetch(`/places/${encodeURIComponent(placeId)}/reviews/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }
  return res;
}

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

  if (!text) return;

  const res = await postReview(placeId, { text, rating });

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
