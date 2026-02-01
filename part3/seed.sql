PRAGMA foreign_keys = ON;

-- =============================
-- Administrator User
-- password = admin1234 (bcrypt hashed)
-- =============================

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$KbQi9wK9F9Jv9wqH/1n2OeB6f7Wq9GQqz1W2fGz9f5y7u0rK8sT9e',
    TRUE
);

-- =============================
-- Initial Amenities
-- =============================

INSERT INTO amenities (id, name) VALUES
('a1b2c3d4-1111-2222-3333-444455556666', 'WiFi'),
('b2c3d4e5-2222-3333-4444-555566667777', 'Swimming Pool'),
('c3d4e5f6-3333-4444-5555-666677778888', 'Air Conditioning');
