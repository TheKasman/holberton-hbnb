/* Login Interaction */
document.addEventListener('DOMContentLoaded', () => {
    console.log("js loaded successfully")
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }

    /* Index page */
    if (document.getElementById('places-list')) {
        setupPriceFilter();
        checkAuthentication();
    }

    /* Place page */
    if (window.location.pathname.includes("place")) {
        initPlacePage();
    }

    /* Review page */
    if (window.location.pathname.includes("add_review")) {
        initAddReviewPage();
    }

});

async function loginUser(email, password) {
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();

            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = 'index.html'
        } else {
            alert('Login failed: ' + response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong');
    }
}


/* ── AUTHENTICATION ───────────────────────────────────────────── */

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        console.log("USER NOT authenticated");

        // Show login button (index page behavior)
        if (loginLink) {
            loginLink.style.display = 'block';
        }

        // Hide review section (place page behavior)
        if (addReviewSection) {
            addReviewSection.style.display = 'none'
        }

        // IMPORTANT: fetch places (index page)
        if (document.getElementById('places-list')) {
            fetchPlaces(null);
        }

    } else {
        console.log("User authenticated");

        // Hide login button
        if (loginLink) {
            loginLink.style.display = 'none';
        }

        // Show review section
        if (addReviewSection) {
            addReviewSection.style.display = 'block';
        }

        // IMPORTANT: fetch places with token
        if (document.getElementById('places-list')) {
            fetchPlaces(token);
        }
    }

    return token;
}


/* Returns the value of a cookie by name, or null if not found. */
function getCookie(name) {
    for (const cookie of document.cookie.split(';')) {
        const [key, ...rest] = cookie.trim().split('=');
        if (key === name) {
            return decodeURIComponent(rest.join('='));
        }
    }
    return null;
}

/* ── FETCH PLACES ─────────────────────────────────────────────── */

/**
 * GET /api/v1/places
 * Sends the JWT in the Authorization header when available.
 */
async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('/api/v1/places', {
            method: 'GET',
            headers
        });

        if (!response.ok) {
            throw new Error(`${response.status} ${response.statusText}`);
        }

        const places = await response.json();
        displayPlaces(places);

    } catch (error) {
        console.error('Failed to fetch places:', error);
        document.getElementById('places-list').innerHTML =
            '<p class="error-message">Unable to load places. Please try again later.</p>';
    }
}

/* ── DISPLAY PLACES ───────────────────────────────────────────── */

/** Cached list used by the price filter. */
let allPlaces = [];


/* Clears #places-list and renders a card for each place. */
function displayPlaces(places) {
    allPlaces = places;
    const container = document.getElementById('places-list');
    container.innerHTML = '';

    if (!places || places.length === 0) {
        container.innerHTML = '<p class="no-results">No places found.</p>';
        return;
    }

    places.forEach(place => container.appendChild(createPlaceCard(place)));
}


/* Builds a .place-card element matching the project's existing card style. */
function createPlaceCard(place) {
    const price = parseFloat(place.price ?? place.price_by_night ?? 0);
    const name = place.title ?? place.name ?? 'Unnamed Place';
    const image = place.image_url || '/static/images/default_image.png';

    const card = document.createElement('div');
    card.classList.add('place-card');
    card.dataset.price = price;

    card.innerHTML = `
        <img
            src="${image}"
            alt="${escapeHtml(name)}"
            class="place-image"
            onerror="this.src='/static/images/default_image.png'"
        />
        <h2>${escapeHtml(name)}</h2>
        <p class="card-price">Price per night: <span class="card-price-amount">$${price.toFixed(2)}</span></p>
        <button class="details-button"
                onclick="window.location.href='place.html?id=${encodeURIComponent(place.id)}'">
            View Details
        </button>
    `;

    return card;
}

/* ── PRICE FILTER ─────────────────────────────────────────────── */

/**
 * Populates the #price-filter <select> with the required options
 * and wires the change listener.
 */
function setupPriceFilter() {
    const select = document.getElementById('price-filter');
    const options = [
        { value: '10', label: '$10' },
        { value: '50', label: '$50' },
        { value: '100', label: '$100' },
        { value: 'all', label: 'All' }
    ];

    select.innerHTML = '';
    options.forEach(({ value, label }) => {
        const opt = document.createElement('option');
        opt.value = value;
        opt.textContent = label;
        select.appendChild(opt);
    });

    select.addEventListener('change', (event) => {
        filterPlacesByPrice(event.target.value);
    });
}

/**
 * Shows/hides .place-card elements based on the selected max price.
 * No page reload or extra fetch – purely DOM toggling.
 */
function filterPlacesByPrice(maxPriceValue) {
    const cards = document.querySelectorAll('.place-card');
    const showAll = maxPriceValue === 'all';
    const max = showAll ? Infinity : parseFloat(maxPriceValue);

    cards.forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = (price <= max) ? '' : 'none';
    });

    /* Show a "no results" message when every card is hidden */
    const container = document.getElementById('places-list');
    const anyVisible = [...cards].some(c => c.style.display !== 'none');
    let msg = container.querySelector('.no-results');

    if (!anyVisible && !msg) {
        msg = document.createElement('p');
        msg.classList.add('no-results');
        msg.textContent = 'No places match the selected price.';
        container.appendChild(msg);
    } else if (anyVisible && msg) {
        msg.remove();
    }
}

/* ── FETCH PLACE DETAILS ───────────────────────────────────── */

/**
 * Extract the id from URL then use initPlacePage function
 * to get id after document is loaded
 */

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

function initPlacePage() {
    const placeId = getPlaceIdFromURL()
    console.log("PLACE ID:", placeId)

    const token = checkAuthentication()
    console.log("TOKEN", token);

    // Call API
    fetchPlaceDetails(token, placeId)
}

/**
 * Fetches details of a single place from the API.
 * Includes JWT token if available.
 */

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };

        // If user is logged in include Authorization header
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers
        });

        if (!response.ok) { throw new Error(`${response.status} ${response.statusText}`) }

        const place = await response.json()
        console.log("PLACE DATA:", place);
        displayPlaceDetails(place)
    } catch (error) {
        console.error("Failed to fetch place details", error)
    }
}

/**
 * Populates the place details section with API data.
 */

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');

    if (!section) return;

    // Normalize fields 
    const name = place.title ?? place.name ?? 'Unnamed Place';
    const image = place.image_url
    const price = place.price ?? place.price_by_night ?? 0;
    const description = place.description ?? 'No description available';
    const host = place.owner
        ? `${place.owner.first_name} ${place.owner.last_name}`
        : 'Unknown';
    const amenitiesList = place.amenities && place.amenities.length > 0
        ? place.amenities.map(a => `<li>${escapeHtml(a.name)}</li>`).join('')
        : '<li>No amenities available</li>';
    const reviews = place.reviews?.map(r => `<li>${escapeHtml(r.text)}</li>`).join('') || '<li>No reviews yet.</li>';

    // Replace ONLY inner content (keep styling classes intact)
    section.innerHTML = `
        
            <div class="place-layout">
                <!-- LEFT: IMAGE -->
                <div class="place-image-container">
                    <img src="${image}" alt="${escapeHtml(name)}"
                        class="place-detail-image">
                </div>
                <!-- RIGHT: INFO -->
                <div class="place-info">
                    <h1>${escapeHtml(name)}</h1>
                    <p><strong>Host:</strong> ${escapeHtml(host)}</p>
                    <p><strong>Price per night:</strong> $${price}</p>
                    <p><strong>Description:</strong> ${escapeHtml(description)}</p>

                    <p><strong>Amenities:</strong></p>
                    <ul class="amenities-list">
                       ${amenitiesList}
                    </ul>
                </div>
            </div>
    `;

    // Populate reviews into the separate #reviews-list section
    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList) {
        if (place.reviews && place.reviews.length > 0) {
            reviewsList.innerHTML = place.reviews.map(r => `
                <li class="review-card">
                    <p><strong>${escapeHtml(r.first_name)} ${escapeHtml(r.last_name)}</strong></p>
                    <p><strong>Rating:</strong> ${r.rating}/5</p>
                    <p>${escapeHtml(r.text)}</p>
                </li>
            `).join('');
        } else {
            reviewsList.innerHTML = '<li>No reviews yet.</li>';
        }
    }
}

/* ── ADD REVIEW PAGE ─────────────────────────────────────────── */


function initAddReviewPage() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const loginLink = document.getElementById('login-link');
    if (loginLink) loginLink.style.display = 'none';

    const placeId = getPlaceIdFromURL();
    if (!placeId) {
        alert("Invalid place ID");
        window.location.href = "index.html";
        return;
    }

    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) return;

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const reviewText = document.getElementById('review-text').value;
        const rating = document.getElementById('rating').value;
        const response = await submitReview(token, placeId, reviewText, rating);
        handleResponse(response, reviewForm);
    });
}


/* Make AJAX Request to Submit Review */
async function submitReview(token, placeId, reviewText, rating) {
    console.log("TOKEN BEING SENT:", token);  // add this
    console.log("PLACE ID:", placeId);
    console.log("RATING:", rating);
    try {
        const response = await fetch('/api/v1/reviews', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId
            })
        });

        return response;

    } catch (error) {
        console.error("Error submitting review:", error);
        return { ok: false };
    }
}

/* Handle API response */
async function handleResponse(response, form) {
    if (response.ok) {
        alert('Review submitted successfully!');
        form.reset();

        // Redirect back to place page
        const placeId = getPlaceIdFromURL();
        window.location.href = `place.html?id=${placeId}`;

    } else {
        const data = await response.json();
        alert(data.error || 'Failed to submit review');
    }
}

/* ── HELPERS ──────────────────────────────────────────────────── */


/* Escapes HTML special chars before injecting into innerHTML. */
function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}