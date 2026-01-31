# HBnB — Database ER Diagram (Task 10)




## ER Diagram (Mermaid)
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

## Relationships
# One-to-Many

# USER → PLACE: one user can own zero or many places
# FK: PLACE.owner_id → USER.id

# USER → REVIEW: one user can write zero or many reviews
# FK: REVIEW.user_id → USER.id

# PLACE → REVIEW: one place can have zero or many reviews
# FK: REVIEW.place_id → PLACE.id

# Many-to-Many

# PLACE ↔ AMENITY via PLACE_AMENITY
# FKs:
# PLACE_AMENITY.place_id → PLACE.id
# PLACE_AMENITY.amenity_id → AMENITY.id

# Cardinality Symbols (Mermaid)
# Symbol	Meaning
`	
`o	`
}o	Zero or more
`}	`
