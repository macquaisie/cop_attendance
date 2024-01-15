import sqlite3

# Initialize SQLite database
conn = sqlite3.connect('attendance_database.db')
cursor = conn.cursor()

# Create a Members table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Members (
        id TEXT PRIMARY KEY,
        name TEXT,
        status TEXT,
        starting_year INTEGER,
        total_attendance INTEGER,
        last_attendance_time TEXT
    )
''')
conn.commit()

# Sample data
data = {
    "509432": {
        "name": "Mark Acquaisie",
        "status": "Member",
        "starting_year": 2017,
        "total_attendance": 7,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "374859": {
        "name": "Harry Potter",
        "status": "Member",
        "starting_year": 2021,
        "total_attendance": 12,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "930404": {
        "name": "Elon Musk",
        "status": "Member",
        "starting_year": 2020,
        "total_attendance": 7,
        "last_attendance_time": "2022-12-11 00:54:34"
    },
    "224422": {
        "name": "Maybel Akoto",
        "status": "Member",
        "starting_year": 2020,
        "total_attendance": 7,
        "last_attendance_time": "2022-12-11 00:54:34"
    }
}

# Insert data into the Members table
for key, value in data.items():
    cursor.execute('''
        INSERT INTO Members (id, name, status, starting_year, total_attendance, last_attendance_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (key, value["name"], value["status"], value["starting_year"], value["total_attendance"], value["last_attendance_time"]))

conn.commit()

# Close the connection
conn.close()
