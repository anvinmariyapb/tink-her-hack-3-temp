import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('homefix.db')
cursor = conn.cursor()

# Create the service_providers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS service_providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    contact TEXT NOT NULL,
    service_type TEXT NOT NULL,
    location TEXT NOT NULL
);
''')

# Create the contacts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id INTEGER,
    contact_name TEXT NOT NULL,
    contact_phone TEXT NOT NULL,
    contact_email TEXT,
    FOREIGN KEY (provider_id) REFERENCES service_providers(id)
);
''')

# Insert sample data into service_providers
cursor.execute('''
INSERT INTO service_providers (name, job_title, contact, service_type, location)
VALUES ('Anil Kumar', 'Plumber', '9876543210', 'Plumbing', 'Kochi');
''')

# Insert sample data into contacts
cursor.execute('''
INSERT INTO contacts (provider_id, contact_name, contact_phone, contact_email)
VALUES (1, 'Anil Kumar', '9876543210', 'anil@plumber.com');
''')

# Commit and close connection
conn.commit()
conn.close()

print("Tables created and sample data inserted successfully!")
