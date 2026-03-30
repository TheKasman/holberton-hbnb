#!/usr/bin/python3
"""Generates uuid's for amenities. just run me to get them."""
import uuid

amenities = ["WiFi", "Swimming Pool", "Air Conditioning"]

for amenity in amenities:
    print(f"INSERT INTO Amenity (id, name) VALUES('{uuid.uuid4()}', '{amenity}');")
