-- Admin user creation, Generate a hash key using admin_hash.py
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$p0ywcwr9iXxD8sB0ZHcY.eYSH/cFw9PWiQtp3s.NLBCoVIssLRmBS',
    TRUE
);