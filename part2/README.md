# HBnB – Part 2: RESTful API

## 📌 Project Overview

HBnB is a simplified Airbnb-like application developed as part of the Holberton School curriculum.  
This part of the project focuses on building a **RESTful API** using **Flask-RESTx**, applying a **layered architecture** and the **Facade pattern**.

The API allows managing:
- Users
- Places
- Amenities
- Reviews

With proper validation, documentation (Swagger), and testing.

---

## 🧱 Architecture

The project follows a **3-layer architecture**:

Presentation Layer (API)
↓
Business Logic Layer (Facade)
↓
Persistence Layer (In-memory storage)
`

### Layers Description

- **Presentation Layer**
  - Handles HTTP requests and responses
  - Input validation
  - Status codes
  - Swagger documentation

- **Business Logic Layer**
  - Contains application logic
  - Uses the Facade pattern to abstract complexity

- **Persistence Layer**
  - In-memory storage (dictionary-based)
  - Simulates database behavior

---

## 📁 Project Structure



part2/
│
├── app/
│ ├── init.py
│ │
│ ├── api/
│ │ └── v1/
│ │ ├── init.py
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── amenities.py
│ │ ├── reviews.py
│ │ └── health.py
│ │
│ ├── business/
│ │ ├── init.py
│ │ └── facade.py
│ │
│ ├── models/
│ │ ├── init.py
│ │ ├── base_model.py
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── amenity.py
│ │ └── review.py
│ │
│ └── persistence/
│ ├── init.py
│ └── repository.py
│
├── main.py
├── requirements.txt
└── README.md






## 🚀 Features Implemented

### Users
- Create user
- Retrieve all users
- Retrieve user by ID
- Update user

### Places
- Create place
- Retrieve all places
- Retrieve place by ID
- Update place
- Retrieve all reviews for a place

### Amenities
- Create amenity
- Retrieve all amenities
- Update amenity

### Reviews
- Create review
- Retrieve all reviews
- Retrieve review by ID
- Update review
- Delete review (only entity with DELETE)

---

## ✅ Validation Rules

- Required fields are enforced for all entities
- Review rating must be between **1 and 5**
- Reviews must be associated with:
  - An existing user
  - An existing place
- Places must have a valid owner
- Proper error responses (`400`, `404`) are returned

---

## 🧪 Testing

### Manual Testing
- Performed using **cURL**
- Tested both successful and failing scenarios
- Verified correct status codes and responses

### Automated Testing
- Basic unit tests implemented using `unittest`
- Ensures API availability and correctness

Run tests:
```bash
python3 -m unittest discover tests
📖 API Documentation (Swagger)

Swagger UI is automatically generated using Flask-RESTx.

Access it at:

http://127.0.0.1:5000/

⚙️ Installation & Usage
Install dependencies
pip install -r requirements.txt

Run the application
python3 -m app


