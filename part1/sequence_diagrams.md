# TASK 2 — Sequence Diagrams for API Calls

This section presents sequence diagrams illustrating the interaction flow between the **Presentation Layer**, **Business Logic Layer (HBnBFacade)**, and **Persistence Layer** for the main API use cases of the **HBnB Evolution** application.

The goal of these diagrams is to clearly demonstrate how API requests are processed step by step across the system layers, following the layered architecture defined in **TASK 1** and the domain model defined in **TASK 0**.

---

## 2.1 User Registration — POST /users

### Description
This API call handles the registration of a new user. The system validates the submitted data, checks for duplicate email addresses, hashes the password, and persists the user information.

### Flow Summary
- The client sends a registration request to the API.
- The API validates the input and forwards the request to the HBnBFacade.
- The facade enforces business rules and checks email uniqueness.
- The user is saved using the UserRepository.
- A success response is returned to the client.

### Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant API as Presentation Layer
    participant Facade as HBnBFacade
    participant UserRepo as UserRepository
    participant DB as Database

    Client->>API: POST /users
    API->>Facade: registerUser(userData)
    Facade->>UserRepo: findByEmail(email)
    UserRepo->>DB: SELECT user
    DB-->>UserRepo: not found
    Facade->>Facade: hashPassword()
    Facade->>UserRepo: save(user)
    UserRepo->>DB: INSERT user
    DB-->>UserRepo: OK
    Facade-->>API: user created
    API-->>Client: 201 Created
2.2 Place Creation — POST /places
Description
This API call allows a registered user to create a new place listing and optionally associate amenities with it.

Flow Summary
The client submits place data to the API.

The API forwards the request to the HBnBFacade.

The facade validates the owner and place attributes.

The place is stored and amenities are linked.

The created place is returned to the client.

Sequence Diagram
mermaid
Copy code
sequenceDiagram
    participant Client
    participant API as Presentation Layer
    participant Facade as HBnBFacade
    participant PlaceRepo as PlaceRepository
    participant AmenityRepo as AmenityRepository
    participant DB as Database

    Client->>API: POST /places
    API->>Facade: createPlace(placeData)
    Facade->>Facade: validateOwner()
    Facade->>PlaceRepo: save(place)
    PlaceRepo->>DB: INSERT place
    DB-->>PlaceRepo: OK
    Facade->>AmenityRepo: linkAmenities(place, amenities)
    AmenityRepo->>DB: INSERT relations
    DB-->>AmenityRepo: OK
    Facade-->>API: place created
    API-->>Client: 201 Created
2.3 Review Submission — POST /places/{id}/reviews
Description
This API call handles the submission of a review for a specific place by a registered user.

Flow Summary
The client submits a review request.

The API forwards the request to the HBnBFacade.

The facade validates the user, the place, and the rating.

The review is persisted.

A success response is returned to the client.

Sequence Diagram
mermaid
Copy code
sequenceDiagram
    participant Client
    participant API as Presentation Layer
    participant Facade as HBnBFacade
    participant ReviewRepo as ReviewRepository
    participant DB as Database

    Client->>API: POST /places/{id}/reviews
    API->>Facade: createReview(reviewData)
    Facade->>Facade: validateUser()
    Facade->>Facade: validatePlace()
    Facade->>Facade: validateRating()
    Facade->>ReviewRepo: save(review)
    ReviewRepo->>DB: INSERT review
    DB-->>ReviewRepo: OK
    Facade-->>API: review created
    API-->>Client: 201 Created
2.4 Fetching a List of Places — GET /places
Description
This API call retrieves a list of places based on optional filtering criteria such as price, location, or amenities.

Flow Summary
The client sends a request with query parameters.

The API parses and validates the filters.

The HBnBFacade queries the PlaceRepository.

Matching places are returned to the client.

Sequence Diagram
mermaid
Copy code
sequenceDiagram
    participant Client
    participant API as Presentation Layer
    participant Facade as HBnBFacade
    participant PlaceRepo as PlaceRepository
    participant DB as Database

    Client->>API: GET /places?filters
    API->>Facade: getPlaces(filters)
    Facade->>PlaceRepo: query(filters)
    PlaceRepo->>DB: SELECT places
    DB-->>PlaceRepo: results
    PlaceRepo-->>Facade: places list
    Facade-->>API: places
    API-->>Client: 200 OK
Summary
API Call	Purpose
POST /users	Register a new user
POST /places	Create a new place
POST /places/{id}/reviews	Submit a review
GET /places	Retrieve a list of places

These sequence diagrams demonstrate a clear separation of responsibilities:

The Presentation Layer handles HTTP requests and responses.

The Business Logic Layer (HBnBFacade) applies domain rules and coordinates operations.

The Persistence Layer manages data storage and retrieval.

yaml
Copy code
