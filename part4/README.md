# HBnB – Part 4: Simple Web Client

## Overview

This project represents **Part 4** of the HBnB Evolution full-stack application.
The goal of this phase is to build a modern and interactive **front-end web client** using **HTML5, CSS3, and JavaScript (ES6)** that communicates with the backend REST API developed in previous parts.

The client allows users to:

* Authenticate using JWT.
* Browse and filter places.
* View detailed information about each place.
* Submit reviews (only for authenticated non-admin users).
* Experience a dynamic UI without full page reloads.

This project follows modern web development practices and integrates securely with a Flask REST API.

---

## Objectives

* Develop a clean and user-friendly interface.
* Connect the UI with backend services using the Fetch API.
* Implement authentication and secure session handling.
* Apply responsive design and semantic HTML.
* Ensure good UX and maintainable code.

---

## Technologies Used

* **HTML5**
* **CSS3**
* **JavaScript ES6**
* **Flask RESTX API**
* **JWT Authentication**
* **LocalStorage for session management**

---

## Features Implemented

### 1. Authentication

* Login form with validation.
* JWT token stored in browser storage.
* Dynamic header:

  * Shows **Login** or **Logout** depending on authentication state.
* Error handling for invalid credentials.

### 2. Places Listing

* Fetches places from the API.
* Displays them as responsive cards.
* Includes:

  * Title
  * Price per night
  * View details button
* Filtering:

  * Max price filtering.
  * Country filter (if implemented).

### 3. Place Details

* Displays:

  * Host name
  * Description
  * Amenities
  * Location
  * Price
* Dynamic review loading.
* Secure access to add review.

### 4. Reviews

* Users can:

  * View all reviews.
  * Submit new reviews.
* Validation:

  * Rating must be between 1 and 5.
  * Text required.
* Security:

  * Admin users are not allowed to submit reviews.

### 5. UI / UX

* Clean layout and consistent design.
* Semantic HTML structure.
* Responsive layout.
* Accessible and readable interface.

---

## Project Structure

```
holbertonschool-hbnb/
│
├── part3/              # Backend Flask API
│   ├── app/
│   ├── instance/
│   ├── seed.py
│   ├── run.py
│
├── part4/              # Frontend (this part)
│   ├── index.html
│   ├── login.html
│   ├── place.html
│   ├── add_review.html
│   ├── styles.css
│   ├── scripts.js
│   ├── images/
│
└── README.md
```

---

## How to Run the Project

### Step 1: Backend Setup

Make sure Python and dependencies are installed.

```
cd part3
pip install -r requirements.txt
```

---

### Step 2: Initialize the Database

This step resets the database and fills it with realistic sample data.

```
python seed.py
```

---

### Step 3: Start the Backend Server

```
python run.py
```

The backend will run on:

```
http://127.0.0.1:5000
```

---

### Step 4: Run the Frontend

Open a new terminal and go to:

```
cd part4
```

Run a simple HTTP server:

For Python 3:

```
python -m http.server 8000
```

The frontend will be available at:

```
http://localhost:8000
```

---

### Step 5: Login Credentials

Use the following sample users:

Admin:

```
Email: admin@hbnb.io
Password: admin1234
```

Regular user:

```
Email: owner@hbnb.io
Password: owner1234
```

---

## Testing the Application

1. Start backend and frontend.
2. Open the application in the browser.
3. Login using the provided credentials.
4. Explore:

   * View places.
   * Filter places.
   * View place details.
   * Submit reviews.
5. Logout and verify session handling.

---

## Security and Best Practices

* JWT authentication implemented.
* Admin restrictions enforced.
* Input validation for all forms.
* Error handling for API requests.
* Clean separation between frontend and backend.

---

## Evaluation Criteria Alignment

This project satisfies:

* Functional UI and API interaction.
* Clean and structured code.
* Consistent design.
* Secure authentication.
* Proper documentation.

---

## Future Improvements

* Pagination and search.
* Image uploads for places.
* User profile management.
* Review editing and deletion.
* Favorites and booking system.

---

## Contributors

* Abdullah Alasiri
* Ghalyah Alotaibi

---

## License

This project is for educational purposes as part of the Holberton School curriculum.
