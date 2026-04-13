# HBnB - Part 4: Simple Web Client
 
This part implements the Presentation layer as a dynamic web client using HTML5, CSS3, and JavaScript ES6, connecting to the back-end API built in previous parts.

---

## 📁 Contents

### ⚙️ Setup

1. Clone the repository

```bash
git clone https://github.com/TheKasman/holberton-hbnb.git
cd holberton-hbnb/part4
```

2. Install the required packages:

```bash
pip3 install -r requirements.txt
```

The `requirements.txt` file contains:

```
flask
flask-restx
flask-bcrypt
flask-jwt-extended
sqlalchemy
flask-sqlalchemy
```

3. Run the application:

```bash
python3 run.py
```

The application will be available at `http://127.0.0.1:5000/login`.

4. Seed the database with initial data:
```bash
python3 seed_users.py
python3 seed_admin.py
python3 seed_amenities.py
python3 seed_places.py
python3 seed_reviews.py
```

---

### 📄 Pages
 
| Page | File | Description |
|------|------|-------------|
| Login | `login.html` | Authentication form with JWT session management |
| List of Places | `index.html` | Main page displaying all places with price filtering |
| Place Details | `place.html` | Detailed view of a place including amenities and reviews |
| Add Review | `add_review.html` | Authenticated form to submit a review for a place |

---

### 🖥️ Pages & Features
 
**Login (`login.html`)**
 
- Submits email and password to the API login endpoint via `fetch` POST
- Stores the returned JWT token in a cookie on success
- Redirects to `index.html` after successful login
- Displays an error message on failure
 
**List of Places (`index.html`)**
 
- Fetches all places from the API on page load
- Dynamically renders each place as a card (`.place-card`) with name, price per night, and a "View Details" button
- Shows the login link only when the user is **not** authenticated
- Filters displayed places by maximum price client-side (options: 10, 50, 100, All) without page reload
 
**Place Details (`place.html`)**
 
- Extracts the place ID from the URL query string (`?id=<place_id>`)
- Fetches and displays full place information: host, price, description, amenities, and reviews
- Shows the add-review section only when the user is authenticated
 
**Add Review (`add_review.html`)**
 
- Redirects unauthenticated users to `index.html` immediately on load
- Submits review text and place ID to the API via authenticated `fetch` POST
- Displays a success message and clears the form on success
- Displays an error message on failure

---

### 🧪 Testing
 
**Verify seed data (optional)**
 
After seeding, you can confirm the database was populated correctly by running:
 
```bash
cd holberton-hbnb/part4
python3 test.py
```
 
This queries `development.db` directly and prints all users, places, amenities, and reviews. Example output:
 
```
Tables: [('users',), ('amenities',), ('places',), ('place_amenity',), ('reviews',)]
 
Users:
('John', 'Doe', 'john@example.com', ...)
 
Places:
('def-456', 'Beach House', 'Nice place', 100.0, 'abc-123')

Place Details (with owner):
('Cheap Studio', 'Cozy and affordable', 9.0, 48.8566, 2.3522, 'Admin User', 'admin@example.com')
 
Amenities:
('Wi-Fi', 'ghi-789', ...)
 
Reviews:
('jkl-012', 'Amazing stay!', 5, 'john@example.com', 'Beach House')
```
 
If any section prints `No X found`, re-run the corresponding seed file before proceeding.

---
 
Start the application before running any browser-based tests:
 
```bash
cd holberton-hbnb/part4
python3 run.py
```
 
**Login**
- Submit valid credentials → verify redirect to `index.html` and cookie set in browser DevTools
- Submit invalid credentials → verify error message is displayed
 
**List of Places**
- Log in and visit `index.html` → verify place cards are rendered
- Use the price filter dropdown → verify cards show/hide without a page reload
- To test as an unauthenticated user, delete the `token` cookie via browser DevTools (Application → Cookies) or by running the following in the browser console → verify the login link reappears
```javascript
document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
```

**Place Details**
- Click "View Details" on a place card → verify all details, amenities, and reviews are displayed
- While authenticated → verify the add-review section is visible
- While unauthenticated → verify the add-review section is hidden
 
**Add Review**
- While authenticated, submit a review → verify success message and form reset
- To test as an unauthenticated user, delete the `token` cookie via browser DevTools (Application → Cookies) or by running the following in the browser console, then visit `add_review.html` directly → verify redirect to `index.html`
```javascript
document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
```
 
---

## 🎯 Objectives
 
**Part 4** connects the full HBnB stack by building the client layer, applying the **Fetch API** and **cookie-based JWT sessions** to interact with the RESTful back-end from Parts 2 and 3:
 
- **HTML5 / CSS3** — Structure and styling across all pages
- **JavaScript ES6** — DOM manipulation, AJAX requests, client-side filtering
- **JWT cookies** — Authentication state management without page reloads
 
---

## 👥 Authors

* Andrew Kasapidis
* Matthew Wirski
* Yongshan Liang
* Patrick Macabulos
