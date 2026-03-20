-- Amenities table
DROP TABLE IF EXISTS Amenity;

CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE
);