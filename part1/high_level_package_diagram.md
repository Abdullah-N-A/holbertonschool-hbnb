classDiagram

%% Presentation Layer
class PresentationLayer {
    <<Facade>>
    +API
    +Services
}

%% Business Logic Layer
class BusinessLogicLayer {
    +User
    +Place
    +Review
    +Amenity
}

%% Persistence Layer
class PersistenceLayer {
    +Repositories
    +Database
}

%% Communication
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Data Access
