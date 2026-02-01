# HBnB (Part 3) — Flask REST API + SQLAlchemy + JWT

Backend API for the HBnB project (Part 3).  
Includes SQLAlchemy persistence, JWT authentication, and Swagger documentation via Flask-RESTX.

---

## Features

- **Flask Application Factory** with environment configs
- **SQLite** database (development) + in-memory DB (testing)
- **SQLAlchemy models**: User, Place, Review, Amenity + relationships
- **JWT Authentication** (`/api/v1/auth/login`) + protected endpoints
- **REST API** for Users / Places / Reviews / Amenities
- **Swagger UI** (Flask-RESTX)

---

## Tech Stack

- Python 3
- Flask
- Flask-RESTX
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Bcrypt
- SQLite (dev)

---
```
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
└─ instance/
└─ development.db
```

## Project Structure

---

## Setup

### 1) Install Dependencies

```bash
pip3 install -r requirements.txt
```
# 2) Create Database Tables
```
python3 -c "from app import create_app; from app.extensions import db; app=create_app();
from app.models import User, Place, Review, Amenity;
with app.app_context(): db.create_all(); print('DB TABLES CREATED')"
```
# 3) Run Server
```
flask --app app run --host=0.0.0.0 --port=5000
```
# Swagger (API Docs)
Swagger is available at:

http://127.0.0.1:5000/api/v1/

# Authentication
# Login (Get JWT)
```
curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}'
```
Export token:
```
TOKEN="PASTE_TOKEN_HERE"
```
# Example Protected Endpoint
```
curl -s http://127.0.0.1:5000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```
