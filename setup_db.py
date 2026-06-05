import sqlite3

# This script creates a physical file named 'mock_enterprise.db' inside a 'data' folder
conn = sqlite3.connect('data/mock_enterprise.db')
cursor = conn.cursor()

# Create a mock table that matches your resume narrative
cursor.execute('''
    CREATE TABLE IF NOT EXISTS policy_transactions (
        policy_id TEXT PRIMARY KEY,
        annual_premium_usd REAL,
        status_code TEXT
    )
''')

# Insert a few rows of fake data for the AI to query
cursor.executemany('''
    INSERT OR IGNORE INTO policy_transactions VALUES (?, ?, ?)
''', [
    ('POL1001', 1200.00, 'A'),
    ('POL1002', 2400.50, 'A'),
    ('POL1003', 850.00, 'C')
])

conn.commit()
conn.close()
print("Database created successfully!")
