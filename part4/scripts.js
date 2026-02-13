const API_URL = "http://localhost:5000/api/v1";

// ==================== AUTH ====================
async function login(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
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
    const response = await fetch(`${API_URL}/auth/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (!response.ok) throw new Error("Failed to get user");
    return await response.json();
  } catch (e) {
    localStorage.removeItem("access_token");
    return null;
  }
}

// ==================== NAV UI ====================
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

  // Show add-review section in place.html only when logged in
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

  // Home page: load places
  const placesList = document.getElementById("places-list");
  if (placesList) {
    loadPlaces();
    const priceFilter = document.getElementById("price-filter");
    if (priceFilter) priceFilter.addEventListener("change", loadPlaces);
  }

  // Place page: load details + reviews
  const placeDetails = document.getElementById("place-details");
  if (placeDetails) {
    loadPlaceDetails();
    loadReviews();
  }

  // Review form (inside place.html)
  const reviewForm = document.getElementById("review-form");
  if (reviewForm) {
    reviewForm.addEventListener("submit", submitReview);
  }

  // add_review.html form (UI only)
  const addReviewForm = document.getElementById("add-review-form");
  if (addReviewForm) {
    addReviewForm.addEventListener("submit", (e) => {
      e.preventDefault();
      alert("UI only: reviews are submitted from place.html in this setup.");
    });
  }
});

// ==================== DATA LOADERS ====================
async function loadPlaces() {
  const token = localStorage.getItem("access_token");
  const priceFilter = document.getElementById("price-filter")?.value || "";
  const placesList = document.getElementById("places-list");

  try {
    let url = `${API_URL}/places`;
    if (priceFilter) url += `?max_price=${encodeURIComponent(priceFilter)}`;

    const response = await fetch(url, {
      headers: token ? { "Authorization": `Bearer ${token}` } : {}
    });

    if (!response.ok) throw new Error("Failed to load places");
    const places = await response.json();

    if (!Array.isArray(places) || places.length === 0) {
      placesList.innerHTML = "<p>No places found.</p>";
      return;
    }

    placesList.innerHTML = places.map(place => `
      <article class="place-card">
        <img src="${place.image_url || "placeholder.jpg"}" alt="${escapeHtml(place.name || "Place")}">
        <h3>${escapeHtml(place.name || "Unnamed place")}</h3>
        <p class="price">$${Number(place.price ?? 0)}</p>
        <a href="place.html?id=${encodeURIComponent(place.id)}" class="details-button btn-view">View Details</a>
      </article>
    `).join("");
  } catch (error) {
    placesList.innerHTML = "<p>Error loading places</p>";
  }
}

async function loadPlaceDetails() {
  const placeId = new URLSearchParams(window.location.search).get("id");
  const token = localStorage.getItem("access_token");
  const placeDetails = document.getElementById("place-details");

  try {
    const response = await fetch(`${API_URL}/places/${encodeURIComponent(placeId)}`, {
      headers: token ? { "Authorization": `Bearer ${token}` } : {}
    });

    if (!response.ok) throw new Error("Place not found");
    const place = await response.json();

    const amenities = Array.isArray(place.amenities) ? place.amenities : [];
    const hostName = place.host?.email || place.host?.name || "Unknown";

    placeDetails.innerHTML = `
      <h1>${escapeHtml(place.name || "Place")}</h1>
      <div class="place-info">
        <p><strong>Host:</strong> ${escapeHtml(hostName)}</p>
        <p><strong>Price per night:</strong> $${Number(place.price ?? 0)}</p>
        <p><strong>Description:</strong> ${escapeHtml(place.description || "")}</p>
        <div>
          <strong>Amenities:</strong>
          <ul>
            ${amenities.map(a => `<li>${escapeHtml(a?.name ?? String(a))}</li>`).join("") || "<li>No amenities listed</li>"}
          </ul>
        </div>
      </div>
    `;
  } catch (error) {
    placeDetails.innerHTML = "<p>Error loading place details</p>";
  }
}

async function loadReviews() {
  const placeId = new URLSearchParams(window.location.search).get("id");
  const token = localStorage.getItem("access_token");
  const reviewsList = document.getElementById("reviews-list");

  try {
    const response = await fetch(`${API_URL}/places/${encodeURIComponent(placeId)}/reviews`, {
      headers: token ? { "Authorization": `Bearer ${token}` } : {}
    });

    if (!response.ok) throw new Error("Failed to load reviews");
    const reviews = await response.json();

    if (!Array.isArray(reviews) || reviews.length === 0) {
      reviewsList.innerHTML = "<p>No reviews yet</p>";
      return;
    }

    reviewsList.innerHTML = reviews.map(review => `
      <article class="review-card review-item">
        <p class="rating">${"⭐".repeat(Number(review.rating ?? 0))}</p>
        <p class="text">${escapeHtml(review.text || "")}</p>
        <p class="author">- ${escapeHtml(review.user?.email || review.user?.name || "Anonymous")}</p>
      </article>
    `).join("");
  } catch (error) {
    reviewsList.innerHTML = "<p>No reviews yet</p>";
  }
}

async function submitReview(e) {
  e.preventDefault();
  const placeId = new URLSearchParams(window.location.search).get("id");
  const token = localStorage.getItem("access_token");
  const reviewText = document.getElementById("review-text").value.trim();
  const rating = Number(document.getElementById("rating").value);

  if (!token) {
    alert("Please login to add a review");
    return;
  }

  try {
    const response = await fetch(`${API_URL}/places/${encodeURIComponent(placeId)}/reviews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ text: reviewText, rating })
    });

    if (!response.ok) throw new Error("Failed to submit review");

    document.getElementById("review-form").reset();
    loadReviews();
  } catch (error) {
    alert("Failed to submit review");
  }
}

// Small helper to avoid HTML injection
function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
