# HBnB Evolution – Technical Documentation

## Introduction

This document provides the technical documentation for the HBnB Evolution project.
It serves as a blueprint for the system architecture, business logic design, and API interaction flow.
The goal of this documentation is to guide the implementation phases of the project.

---

## High-Level Architecture

### Overview

The HBnB application follows a layered architecture composed of three main layers:

- Presentation Layer
- Business Logic Layer
- Persistence Layer

The communication between layers is handled through the Facade pattern.

### High-Level Package Diagram

![High-Level Package Diagram](./high_level_package_diagram.png)

### Description

- Presentation Layer handles user interaction through services and API endpoints.
- Business Logic Layer contains the core models and business rules.
- Persistence Layer manages data storage and retrieval.

---

## Business Logic Layer

### Overview

The Business Logic Layer contains the core entities of the HBnB application:

- User
- Place
- Review
- Amenity

Each entity has a unique identifier and includes creation and update timestamps.

### Class Diagram

![Business Logic Class Diagram](./business_logic_class_diagram.png)

### Entities Description

- User represents application users.
- Place represents properties listed by users.
- Review represents feedback left by users for places.
- Amenity represents features associated with places.

### Relationships

- A User can own multiple Places.
- A Place can have multiple Amenities.
- A Review belongs to one User and one Place.

---

## API Interaction Flow

### User Registration

![User Registration Sequence Diagram](./sequence_user_registration.png)

---

### Place Creation

![Place Creation Sequence Diagram](./sequence_place_creation.png)

---

### Review Submission

![Review Submission Sequence Diagram](./sequence_review_submission.png)

---

### Fetching a List of Places

![Fetch Places Sequence Diagram](./sequence_fetch_places.png)

---

## Conclusion

This document provides a structured overview of the HBnB Evolution application
and serves as a reference for the implementation phases.

