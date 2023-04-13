import sqlite3

# Connect to database (create if it doesn't exist)
conn = sqlite3.connect('tasks.db')

# Create table
conn.execute('''CREATE TABLE tasks
             (id INTEGER PRIMARY KEY,
             title TEXT,description TEXT,
             done BOOLEAN)''')

# Close connection
conn.close()

