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

```
part3/
├─ app/
│  ├─ __init__.py
│  ├─ extensions.py
│  ├─ business/
│  │  └─ facade.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ base_model.py
│  │  ├─ user.py
│  │  ├─ place.py
│  │  ├─ review.py
│  │  └─ amenity.py
│  └─ api/
│     └─ v1/
│        ├─ users.py
│        ├─ places.py
│        ├─ reviews.py
│        ├─ amenities.py
│        └─ auth.py
├─ config.py
├─ run.py
├─ requirements.txt
├─ seed.py
├─ schema.sql
├─ seed.sql
└─ instance/        # created at runtime (ignored by git)
```

---

## Setup Instructions (Flask API)

### 1) Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2) Create Database Tables (SQLAlchemy)

```bash
python3 -c "from app import create_app; from app.extensions import db; app=create_app(); app.app_context().push(); db.create_all(); print('DB TABLES CREATED')"
```

### 3) Seed Initial Data (Admin + Amenities)

```bash
python3 seed.py
```

Admin credentials:

```
admin@hbnb.io / admin1234
```

### 4) Run the Server

```bash
python3 run.py
```

Swagger Docs:

```
http://127.0.0.1:5000/api/v1/
```

---

## SQL Scripts (Raw SQL Task)

To test the database schema **without ORM**:

```bash
sqlite3 raw_test.db < schema.sql
sqlite3 raw_test.db < seed.sql
sqlite3 raw_test.db ".tables"
sqlite3 raw_test.db "SELECT email, is_admin FROM users;"
sqlite3 raw_test.db "SELECT name FROM amenities;"
```

Expected:

```
admin@hbnb.io | 1
WiFi
Swimming Pool
Air Conditioning
```

---

## Authentication

```bash
curl -s -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}'
```

---

## Important Note

The SQLite database file (`instance/development.db`) is **NOT committed to Git**.  
It is automatically created during setup.

---

## Authors

Abdullah Alasiri  
Ghalyah Alotaibi
