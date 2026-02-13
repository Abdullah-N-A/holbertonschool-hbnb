/*scripts.js
  Login functionality for Holberton HBNB project
  Handles authentication using Fetch API
  Stores JWT token in cookies
*/
const API_URL = "http://localhost:5000/api/v1"; // Change to your API URL

// ==================== AUTH FUNCTIONS ====================
async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Login failed");

        localStorage.setItem("access_token", data.access_token);
        return true;
    } catch (error) {
        console.error("Login error:", error);
        throw error;
    }
}

async function logout() {
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
    } catch (error) {
        console.error("Error getting user:", error);
        localStorage.removeItem("access_token");
        return null;
    }
}

// ==================== UI FUNCTIONS ====================
function updateNavBar(user) {
    const loginLink = document.getElementById("login-link");
    const userInfo = document.getElementById("user-info");
    const userEmail = document.getElementById("user-email");
    const logoutBtn = document.getElementById("logout-btn");

    if (user) {
        loginLink.style.display = "none";
        userInfo.style.display = "inline-flex";
        userEmail.textContent = user.email;
        logoutBtn.addEventListener("click", logout);
    } else {
        loginLink.style.display = "inline-block";
        userInfo.style.display = "none";
    }
}

// ==================== LOGIN PAGE ====================
document.addEventListener("DOMContentLoaded", async () => {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;
            const errorDiv = document.getElementById("error-message");

            try {
                await login(email, password);
                window.location.href = "index.html";
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = "block";
            }
        });
    }

    // Update navbar on every page
    const user = await getCurrentUser();
    updateNavBar(user);

    // Load places on home page
    const placesList = document.getElementById("places-list");
    if (placesList) {
        loadPlaces();
    }

    // Handle price filter
    const priceFilter = document.getElementById("price-filter");
    if (priceFilter) {
        priceFilter.addEventListener("change", loadPlaces);
    }

    // Load place details on place page
    const placeDetails = document.getElementById("place-details");
    if (placeDetails) {
        loadPlaceDetails();
        loadReviews();
    }

    // Handle review form
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        reviewForm.addEventListener("submit", submitReview);
    }
});

async function loadPlaces() {
    const token = localStorage.getItem("access_token");
    const priceFilter = document.getElementById("price-filter").value;
    const placesList = document.getElementById("places-list");

    try {
        let url = `${API_URL}/places`;
        if (priceFilter) url += `?max_price=${priceFilter}`;

        const response = await fetch(url, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error("Failed to load places");
        const places = await response.json();

        placesList.innerHTML = places.map(place => `
            <div class="place-card">
                <img src="${place.image_url || 'placeholder.jpg'}" alt="${place.name}">
                <h3>${place.name}</h3>
                <p class="description">${place.description}</p>
                <p class="price">$${place.price}</p>
                <a href="place.html?id=${place.id}" class="btn-view">View Details</a>
            </div>
        `).join("");
    } catch (error) {
        console.error("Error loading places:", error);
        placesList.innerHTML = "<p>Error loading places</p>";
    }
}

async function loadPlaceDetails() {
    const placeId = new URLSearchParams(window.location.search).get("id");
    const token = localStorage.getItem("access_token");
    const placeDetails = document.getElementById("place-details");

    try {
        const response = await fetch(`${API_URL}/places/${placeId}`, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error("Place not found");
        const place = await response.json();

        placeDetails.innerHTML = `
            <img src="${place.image_url || 'placeholder.jpg'}" alt="${place.name}">
            <h1>${place.name}</h1>
            <p>${place.description}</p>
            <p class="price">$${place.price}</p>
        `;
    } catch (error) {
        console.error("Error loading place:", error);
        placeDetails.innerHTML = "<p>Error loading place details</p>";
    }
}

async function loadReviews() {
    const placeId = new URLSearchParams(window.location.search).get("id");
    const token = localStorage.getItem("access_token");
    const reviewsList = document.getElementById("reviews-list");

    try {
        const response = await fetch(`${API_URL}/places/${placeId}/reviews`, {
            headers: token ? { "Authorization": `Bearer ${token}` } : {}
        });

        if (!response.ok) throw new Error("Failed to load reviews");
        const reviews = await response.json();

        reviewsList.innerHTML = reviews.map(review => `
            <div class="review-item">
                <p class="rating">${"⭐".repeat(review.rating)}</p>
                <p class="text">${review.text}</p>
                <p class="author">- ${review.user.email}</p>
            </div>
        `).join("");
    } catch (error) {
        console.error("Error loading reviews:", error);
        reviewsList.innerHTML = "<p>No reviews yet</p>";
    }
}

async function submitReview(e) {
    e.preventDefault();
    const placeId = new URLSearchParams(window.location.search).get("id");
    const token = localStorage.getItem("access_token");
    const reviewText = document.getElementById("review-text").value;
    const rating = document.getElementById("rating").value;

    if (!token) {
        alert("Please login to add a review");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/places/${placeId}/reviews`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ text: reviewText, rating: parseInt(rating) })
        });

        if (!response.ok) throw new Error("Failed to submit review");
        document.getElementById("review-form").reset();
        loadReviews();
    } catch (error) {
        console.error("Error submitting review:", error);
        alert("Failed to submit review");
    }
}