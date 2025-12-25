classDiagram

class BaseModel {
    +UUID id
    +DateTime created_at
    +DateTime updated_at
    +save()
    +update()
    +delete()
}

class User {
    +String first_name
    +String last_name
    +String email
    +String password
    +create_place()
    +write_review()
}

class Place {
    +String name
    +String description
    +Float price_per_night
    +Float latitude
    +Float longitude
    +create_review()
    +add_amenity()
}

class Review {
    +String text
    +Integer rating
    +edit_review()
}

class Amenity {
    +String name
}

%% Inheritance
User --|> BaseModel
Place --|> BaseModel
Review --|> BaseModel
Amenity --|> BaseModel

%% Relationships
User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has
