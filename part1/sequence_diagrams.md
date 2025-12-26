TASK 2 — Sequence Diagrams for API Calls

This section describes the sequence diagrams that illustrate how requests flow through the Presentation Layer, Business Logic Layer (HBnBFacade), and Persistence Layer for the main API endpoints of the HBnB Evolution application.

These diagrams aim to show, step by step, how each API request is handled across the system layers, following the layered architecture defined in TASK 1 and the domain model introduced in TASK 0.

2.1 User Registration — POST /users

Description
A new user registers by submitting personal information. The system validates the input, checks for duplicate email addresses, hashes the password, and stores the user.

Flow Summary

The client sends a registration request to the API.

The API validates the input and forwards the request to the HBnBFacade.

The facade checks email uniqueness and applies business rules.

The user is saved using the UserRepository.

A success response is returned to the client.

(Sequence diagram stays exactly as you have it — ممتاز)

2.2 Place Creation — POST /places

Description
A registered user creates a new place listing and may associate amenities with it.

Flow Summary

The client submits place data to the API.

The API forwards the request to the HBnBFacade.

The facade validates the owner and place attributes.

The place is saved and amenities are linked.

The created place is returned.

2.3 Review Submission — POST /places/{id}/reviews

Description
A user submits a review for a specific place.

Flow Summary

The client sends a review request.

The API forwards the request to the HBnBFacade.

The facade validates the user, place, and rating.

The review is saved.

A success response is returned.

2.4 Fetching a List of Places — GET /places

Description
A user retrieves a list of places using optional filters such as price, location, or amenities.

Flow Summary

The client sends a request with query filters.

The API parses and validates the filters.

The HBnBFacade queries the PlaceRepository.

Matching places are returned to the client.

Summary
API Call	Purpose
POST /users	Register a new user
POST /places	Create a new place
POST /places/{id}/reviews	Submit a review
GET /places	Retrieve a list of places

These sequence diagrams highlight the separation of responsibilities between layers:

The Presentation Layer handles incoming requests and responses.

The Business Logic Layer (HBnBFacade) applies rules and coordinates operations.

The Persistence Layer manages data storage and retrieval.
