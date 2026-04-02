/* Login Interaction */
document.addEventListener('DOMContentLoaded', () => {
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
});

async function loginUser(email, password){
  try{
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
    const token     = getCookie('token');
    const loginLink = document.getElementById('login-link');
 
    if (!token) {
        loginLink.style.display = 'block';
        fetchPlaces(null);
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
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
    const name  = place.title ?? place.name ?? 'Unnamed Place';
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
        <p>Price per night: $${price.toFixed(2)}</p>
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
    const select  = document.getElementById('price-filter');
    const options = [
        { value: '10',  label: '$10'  },
        { value: '50',  label: '$50'  },
        { value: '100', label: '$100' },
        { value: 'all', label: 'All'  }
    ];
 
    select.innerHTML = '';
    options.forEach(({ value, label }) => {
        const opt       = document.createElement('option');
        opt.value       = value;
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
    const cards     = document.querySelectorAll('.place-card');
    const showAll   = maxPriceValue === 'all';
    const max       = showAll ? Infinity : parseFloat(maxPriceValue);
 
    cards.forEach(card => {
        const price        = parseFloat(card.dataset.price);
        card.style.display = (price <= max) ? '' : 'none';
    });
 
    /* Show a "no results" message when every card is hidden */
    const container  = document.getElementById('places-list');
    const anyVisible = [...cards].some(c => c.style.display !== 'none');
    let   msg        = container.querySelector('.no-results');
 
    if (!anyVisible && !msg) {
        msg = document.createElement('p');
        msg.classList.add('no-results');
        msg.textContent = 'No places match the selected price.';
        container.appendChild(msg);
    } else if (anyVisible && msg) {
        msg.remove();
    }
}
 
/* ── HELPERS ──────────────────────────────────────────────────── */
 

 /* Escapes HTML special chars before injecting into innerHTML. */
function escapeHtml(str) {
    if (str == null) return '';
    return String(str)
        .replace(/&/g,  '&amp;')
        .replace(/</g,  '&lt;')
        .replace(/>/g,  '&gt;')
        .replace(/"/g,  '&quot;')
        .replace(/'/g,  '&#39;');
}