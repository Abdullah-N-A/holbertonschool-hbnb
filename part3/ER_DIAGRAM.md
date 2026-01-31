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
```
🔗 Relationships
One-to-Many
From	To	Meaning
USER → PLACE	A user can own many places	
USER → REVIEW	A user can write many reviews	
PLACE → REVIEW	A place can have many reviews	
Many-to-Many
Tables	Description
PLACE ↔ AMENITY	A place can have many amenities, and an amenity can belong to many places via PLACE_AMENITY
```
📘 Cardinality Symbols

| Symbol | Meaning      |             |             |
| ------ | ------------ | ----------- | ----------- |
| `      |              | `           | Exactly one |
| `o     | `            | Zero or one |             |
| `}     | `            | One or more |             |
| `}o`   | Zero or more |             |             |
