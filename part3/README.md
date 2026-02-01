# HBnB (Part 3) — Flask REST API + SQLAlchemy + JWT

Backend API for the **HBnB Project (Part 3)**.  
Implements SQLAlchemy persistence, JWT authentication, and Swagger documentation using Flask-RESTX.

---

## Features

- Flask Application Factory
- SQLite database (development) + in-memory DB (testing)
- SQLAlchemy models: User, Place, Review, Amenity
- JWT Authentication (`/api/v1/auth/login`)
- Protected endpoints with role support
- Full REST API (CRUD)
- Swagger UI (Flask-RESTX)

---

## Tech Stack

- Python 3  
- Flask  
- Flask-RESTX  
- Flask-SQLAlchemy  
- Flask-JWT-Extended  
- Flask-Bcrypt  
- SQLite  

---

## Project Structure



part3/
├─ app/
│ ├─ init.py
│ ├─ extensions.py
│ ├─ business/
│ │ └─ facade.py
│ ├─ models/
│ │ ├─ init.py
│ │ ├─ base_model.py
│ │ ├─ user.py
│ │ ├─ place.py
│ │ ├─ review.py
│ │ └─ amenity.py
│ └─ api/
│ └─ v1/
│ ├─ users.py
│ ├─ places.py
│ ├─ reviews.py
│ ├─ amenities.py
│ └─ auth.py
├─ config.py
├─ run.py
├─ requirements.txt
├─ seed.py
└─ instance/ # created at runtime (ignored by git)


---

## Setup Instructions

### 1) Install Dependencies

```bash
pip3 install -r requirements.txt

2) Create Database Tables
python3 -c "from app import create_app; from app.extensions import db; app=create_app(); app.app_context().push(); db.create_all(); print('DB TABLES CREATED')"

3) Seed Initial Data (Admin + Amenities)
python3 seed.py


This creates:

Admin user → admin@hbnb.io / admin1234

Default amenities

4) Run the Server
python3 run.py


Server runs at:

http://127.0.0.1:5000

Swagger API Docs
http://127.0.0.1:5000/api/v1/

Authentication
Login and get JWT
curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}'


Copy the token and export:

TOKEN="PASTE_TOKEN_HERE"

Get current user (Protected)
curl -s http://127.0.0.1:5000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"

API Endpoints

Base URL: /api/v1

Users
Method	Endpoint	Description
GET	/users/	Get all users
POST	/users/	Create new user
GET	/users/<user_id>	Get user
PUT	/users/<user_id>	Update user
Places
Method	Endpoint	Description
GET	/places/	Get all places
POST	/places/	Create place
GET	/places/<place_id>	Get place
PUT	/places/<place_id>	Update place
GET	/places/<place_id>/reviews	Get reviews
Reviews
Method	Endpoint	Description
GET	/reviews/	Get all reviews
POST	/reviews/	Create review
GET	/reviews/<review_id>	Get review
PUT	/reviews/<review_id>	Update review
DELETE	/reviews/<review_id>	Delete review
Amenities
Method	Endpoint	Description
GET	/amenities/	Get amenities
POST	/amenities/	Create amenity
GET	/amenities/<amenity_id>	Get amenity
PUT	/amenities/<amenity_id>	Update amenity
Auth
Method	Endpoint	Description
POST	/auth/login	Get JWT
GET	/auth/me	Current user
Quick Smoke Test
curl -I http://127.0.0.1:5000/api/v1/
curl -s http://127.0.0.1:5000/api/v1/users/
curl -s http://127.0.0.1:5000/api/v1/amenities/

Test DB Persistence
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Place","city":"Riyadh","price_per_night":100,"owner_id":"36c9050e-ddd3-4c3b-9731-9f487208bbc1"}'

curl -s http://127.0.0.1:5000/api/v1/places/

Important Note

The SQLite database file (instance/development.db) is NOT committed to Git.
It is automatically created when running setup steps.

Authors

Abdullah Alasiri
Ghalyah Alotaibi
