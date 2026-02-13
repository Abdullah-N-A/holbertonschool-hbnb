/*scripts.js
  Login functionality for Holberton HBNB project
  Handles authentication using Fetch API
  Stores JWT token in cookies
*/

/*
  Main scripts for Holberton HBNB frontend
  Handles place listing, filtering, and reviews
*/

const API_BASE_URL = 'http://localhost:5000/api/v1'; // Change to your API URL

let allPlaces = [];
let allStates = [];
let allCities = [];

document.addEventListener('DOMContentLoaded', async () => {
    // Check if user is logged in
    if (!getToken()) {
        window.location.href = 'login.html';
        return;
    }

    // Setup logout
    const logoutLink = document.getElementById('logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }

    // Load initial data
    await loadStates();
    await loadPlaces();
    setupFilters();
    setupReviewForm();
});

function getToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'token') return value;
    }
    return null;
}

function logout() {
    document.cookie = 'token=; path=/; max-age=0';
    window.location.href = 'login.html';
}

async function loadStates() {
    try {
        const response = await fetch(`${API_BASE_URL}/states`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (!response.ok) throw new Error('Failed to load states');

        allStates = await response.json();
        populateStateFilter();
    } catch (error) {
        console.error('Error loading states:', error);
    }
}

async function loadPlaces() {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (!response.ok) throw new Error('Failed to load places');

        allPlaces = await response.json();
        displayPlaces(allPlaces);
    } catch (error) {
        console.error('Error loading places:', error);
    }
}

function populateStateFilter() {
    const stateFilter = document.getElementById('state-filter');
    if (!stateFilter) return;

    allStates.forEach(state => {
        const option = document.createElement('option');
        option.value = state.id;
        option.textContent = state.name;
        stateFilter.appendChild(option);
    });
}

function setupFilters() {
    const stateFilter = document.getElementById('state-filter');
    const cityFilter = document.getElementById('city-filter');

    if (stateFilter) {
        stateFilter.addEventListener('change', async (e) => {
            const stateId = e.target.value;
            if (stateId) {
                await loadCities(stateId);
            } else {
                cityFilter.innerHTML = '<option value="">All Cities</option>';
                displayPlaces(allPlaces);
            }
        });
    }

    if (cityFilter) {
        cityFilter.addEventListener('change', (e) => {
            const cityId = e.target.value;
            const filteredPlaces = cityId
                ? allPlaces.filter(place => place.city_id === cityId)
                : allPlaces;
            displayPlaces(filteredPlaces);
        });
    }
}

async function loadCities(stateId) {
    try {
        const response = await fetch(`${API_BASE_URL}/states/${stateId}/cities`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (!response.ok) throw new Error('Failed to load cities');

        allCities = await response.json();
        populateCityFilter();
    } catch (error) {
        console.error('Error loading cities:', error);
    }
}

function populateCityFilter() {
    const cityFilter = document.getElementById('city-filter');
    if (!cityFilter) return;

    cityFilter.innerHTML = '<option value="">All Cities</option>';
    allCities.forEach(city => {
        const option = document.createElement('option');
        option.value = city.id;
        option.textContent = city.name;
        cityFilter.appendChild(option);
    });
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h3>${place.name}</h3>
            <p><strong>Price per night:</strong> $${place.price_by_night}</p>
            <p><strong>City:</strong> ${place.city ? place.city.name : 'N/A'}</p>
            <p>${place.description || 'No description available'}</p>
            <button class="view-details-btn" onclick="viewPlace('${place.id}')">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

function viewPlace(placeId) {
    window.location.href = `place.html?id=${placeId}`;
}

async function setupReviewForm() {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (!placeId) return;

    // Load place details
    await loadPlaceDetails(placeId);

    reviewForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;

        try {
            await submitReview(placeId, reviewText, rating);
            reviewForm.reset();
            await loadPlaceDetails(placeId); // Refresh reviews
        } catch (error) {
            alert('Error submitting review: ' + error.message);
        }
    });
}

async function loadPlaceDetails(placeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });

        if (!response.ok) throw new Error('Failed to load place details');

        const place = await response.json();
        displayPlaceDetails(place);
        displayReviews(place.reviews || []);
    } catch (error) {
        console.error('Error loading place details:', error);
    }
}

function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    if (!detailsSection) return;

    detailsSection.innerHTML = `
        <h2>${place.name}</h2>
        <p><strong>Price per night:</strong> $${place.price_by_night}</p>
        <p><strong>Max guest:</strong> ${place.max_guest}</p>
        <p><strong>Number of rooms:</strong> ${place.number_rooms}</p>
        <p><strong>Number of bathrooms:</strong> ${place.number_bathrooms}</p>
        <p><strong>City:</strong> ${place.city ? place.city.name : 'N/A'}</p>
        <p><strong>Description:</strong> ${place.description || 'No description'}</p>
    `;
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviews-list');
    if (!reviewsList) return;

    reviewsList.innerHTML = '';

    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach(review => {
        const reviewDiv = document.createElement('div');
        reviewDiv.className = 'review';
        reviewDiv.innerHTML = `
            <p><strong>${review.user ? review.user.first_name : 'Anonymous'}</strong> - Rating: ${review.rating}/5</p>
            <p>${review.text}</p>
        `;
        reviewsList.appendChild(reviewDiv);
    });
}

async function submitReview(placeId, text, rating) {
    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                text,
                rating: parseInt(rating)
            })
        });

        if (!response.ok) throw new Error('Failed to submit review');

        return await response.json();
    } catch (error) {
        throw error;
    }
}