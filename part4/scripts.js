// ===== API ROOT (يشتغل على localhost أو sandbox) =====
const API_ROOT = `${location.protocol}//${location.hostname}:5000/api/v1`;

// ==================== AUTH ====================
async function login(email, password) {
  const response = await fetch(`${API_ROOT}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "Login failed");

  localStorage.setItem("access_token", data.access_token);
  return true;
}

function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "login.html";
}

async function getCurrentUser() {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  try {
    const response = await fetch(`${API_ROOT}/auth/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!response.ok) throw new Error("Failed to get user");
    return await response.json();
  } catch (e) {
    localStorage.removeItem("access_token");
    return null;
  }
}

// ==================== NAV ====================
function updateNavBar(user) {
  const loginLink = document.getElementById("login-link");
  const userInfo = document.getElementById("user-info");
  const userEmail = document.getElementById("user-email");
  const logoutBtn = document.getElementById("logout-btn");

  if (!loginLink || !userInfo) return;

  if (user) {
    loginLink.style.display = "none";
    userInfo.style.display = "inline-flex";
    if (userEmail) userEmail.textContent = user.email || "";
    if (logoutBtn) logoutBtn.addEventListener("click", logout);
  } else {
    loginLink.style.display = "inline-block";
    userInfo.style.display = "none";
  }
}

// ==================== PAGE LOAD ====================
document.addEventListener("DOMContentLoaded", async () => {
  const user = await getCurrentUser();
  updateNavBar(user);

  // hide add review section if not logged in
  const addReviewSection = document.getElementById("add-review");
  if (addReviewSection) addReviewSection.style.display = user ? "block" : "none";

  // Login page
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();
      const errorDiv = document.getElementById("error-message");

      try {
        await login(email, password);
        window.location.href = "index.html";
      } catch (error) {
        if (errorDiv) {
          errorDiv.textContent = error.message;
          errorDiv.style.display = "block";
        }
      }
    });
  }

  // Home
  const placesList = document.getElementById("places-list");
  if (placesList) {
    loadPlaces();
    const priceFilter = document.getElementById("price-filter");
    if (priceFilter) priceFilter.addEventListener("change", loadPlaces);
  }

  // Place page
  const placeDetails = document.getElementById("place-details");
  if (placeDetails) {
    loadPlaceDetails();
    loadReviews();
  }

  const reviewForm = document.getElementById("review-form");
  if (reviewForm) reviewForm.addEventListener("submit", submitReview);
});

// ==================== LOAD PLACES ====================
async function loadPlaces() {
  const token = localStorage.getItem("access_token");
  const priceFilter = document.getElementById("price-filter")?.value || "";
  const placesList = document.getElementById("places-list");

  try {
    let url = `${API_ROOT}/places/`; // عندك Route "/"
    if (priceFilter) url += `?max_price=${encodeURIComponent(priceFilter)}`;

    const response = await fetch(url, {
      headers: token ? { "Authorization": `Bearer ${token}` } : {}
    });

    if (!response.ok) throw new Error("Failed to load places");
    const places = await response.json();

    if (!Array.isArray(places) || places.length === 0) {
      placesList.innerHTML = `<p class="loading">No places found.</p>`;
      return;
    }

    placesList.innerHTML = places.map(place => `
      <article class="place-card">
        <img src="${place.image_url || "placeholder.jpg"}" alt="${place.name}">
        <h3>${place.name}</h3>
        <p class="price">$${place.price_per_night}</p>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      </article>
    `).join("");

  } catch (error) {
    console.error(error);
    placesList.innerHTML = "<p>Error loading places</p>";
  }
}

// ==================== PLACE DETAILS ====================
async function loadPlaceDetails() {
  const placeId = new URLSearchParams(window.location.search).get("id");
  const token = localStorage.getItem("access_token");
  const placeDetails = document.getElementById("place-details");

  if (!placeId) {
    placeDetails.innerHTML = "<p>Missing place id</p>";
    return;
  }

  try {
    const response = await fetch(`${API_ROOT}/places/${placeId}`, {
      headers: token ? { "Authorization": `Bearer ${token}` } : {}
    });

    if (!response.ok) throw new Error("Place not found");
    const place = await response.json();

    const amenities = place.amenities || [];
    const ownerText = place.owner_id ? place.owner_id : "Unknown";

    placeDetails.innerHTML = `
      <h1>${place.name}</h1>

      <div class="place-info">
        <p><strong>Host:</strong> ${ownerText}</p>
        <p><strong>Price:</strong> $${place.price_per_night}</p>
        <p>${place.description || ""}</p>

        <h3>Amenities</h3>
        <ul>
          ${amenities.map(a => `<li>${a.name || a}</li>`).join("")}
        </ul>
      </div>
    `;

  } catch (error) {
    console.error(error);
    placeDetails.innerHTML = "<p>Error loading place</p>";
  }
}

// ==================== REVIEWS ====================
async function loadReviews() {
  const placeId = new URLSearchParams(window.location.search).get("id");
  const token = localStorage.getItem("access_token");
  const reviewsList = document.getElementById("reviews-list");

  if (!reviewsList || !placeId) return;

  try {
    const response = await fetch(`${API_ROOT}/places/${placeId}/reviews`, {
      headers: token ? { "Authorization": `Bearer ${token}` } : {}
    });

    if (!response.ok) throw new Error("Failed");

    const reviews = await response.json();

    if (!Array.isArray(reviews) || reviews.length === 0) {
      reviewsList.innerHTML = "<p>No reviews yet</p>";
      return;
    }

    reviewsList.innerHTML = reviews.map(r => `
      <article class="review-card">
        <p>${"⭐".repeat(Number(r.rating || 0))}</p>
        <p>${r.text || ""}</p>
        <small>User: ${r.user_id || "Unknown"}</small>
      </article>
    `).join("");

  } catch (error) {
    console.error(error);
    reviewsList.innerHTML = "<p>No reviews yet</p>";
  }
}

// ==================== SUBMIT REVIEW ====================
async function submitReview(e) {
  e.preventDefault();

  const placeId = new URLSearchParams(window.location.search).get("id");
  const token = localStorage.getItem("access_token");

  const text = document.getElementById("review-text").value.trim();
  const rating = document.getElementById("rating").value;

  if (!token) {
    alert("Please login to add a review");
    return;
  }

  try {
    const response = await fetch(`${API_ROOT}/places/${placeId}/reviews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ text, rating: Number(rating) })
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.error || "Submit failed");

    loadReviews();
    document.getElementById("review-form").reset();

  } catch (error) {
    console.error(error);
    alert("Error submitting review");
  }
}
