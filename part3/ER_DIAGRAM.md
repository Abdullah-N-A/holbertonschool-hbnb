```mermaid
erDiagram

    USER {
        CHAR(36) id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        BOOLEAN is_admin
    }

    PLACE {
        CHAR(36) id PK
        VARCHAR title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id FK
    }

    REVIEW {
        CHAR(36) id PK
        TEXT text
        INT rating
        CHAR(36) user_id FK
        CHAR(36) place_id FK
    }

    AMENITY {
        CHAR(36) id PK
        VARCHAR name
    }

    PLACE_AMENITY {
        CHAR(36) place_id FK
        CHAR(36) amenity_id FK
    }

    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : included_in
```
Relationships
One-to-Many Relationships
USER → PLACE: A user can own multiple places, but each place has one owner

Cardinality: ||--o{ (one to zero or many)
Foreign Key: PLACE.owner_id references USER.id
USER → REVIEW: A user can write multiple reviews, but each review is written by one user

Cardinality: ||--o{ (one to zero or many)
Foreign Key: REVIEW.user_id references USER.id
PLACE → REVIEW: A place can have multiple reviews, but each review belongs to one place

Cardinality: ||--o{ (one to zero or many)
Foreign Key: REVIEW.place_id references PLACE.id
Many-to-Many Relationship
PLACE ↔ AMENITY: A place can have many amenities, and an amenity can belong to many places
Cardinality: }o--o{ (many to many)
Junction Table: PLACE_AMENITY
Foreign Keys:
PLACE_AMENITY.place_id references PLACE.id
PLACE_AMENITY.amenity_id references AMENITY.id
Cardinality Symbols
Symbol	Meaning
||	Exactly one
o|	Zero or one
}|	One or more
}o	Zero or more
Viewing the Diagram
Online Editor: Mermaid Live Editor
GitHub: Automatically renders Mermaid diagrams in markdown files