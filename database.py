import sqlite3
import csv

conn = sqlite3.connect("sprint_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS training_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT,
    session_type TEXT NOT NULL,
    duration_min INTEGER,
    intensity_rpe INTEGER,
    sleep_hours REAL,
    felt_rating INTEGER,
    weather TEXT
)
""")
cursor.execute("DELETE FROM training_sessions")

with open("data/sprint_log.csv","r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute("""
            INSERT INTO training_sessions (
                date, time, session_type, duration_min,
                intensity_rpe, sleep_hours, felt_rating, weather
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["date"],
            row["time"],
            row["session_type"],
            int(row["duration_min"]) if row["duration_min"] else None,
            int(row["intensity_rpe"]) if row["intensity_rpe"] else None,
            float(row["sleep_hours"]) if row["sleep_hours"] else None,
            int(row["felt_rating"]) if row["felt_rating"] else None,
            row["weather"]
        ))


conn.commit()

cursor.execute("SELECT COUNT(*) FROM training_sessions")
total = cursor.fetchone()[0]

print(f"Total records in database: {total}")


cursor.execute("""
    SELECT date, intensity_rpe
    FROM training_sessions
    WHERE intensity_rpe < 1 OR intensity_rpe > 10
""")

invalid_rpe = cursor.fetchall()

print("Invalid RPE records:", invalid_rpe)

# Check sleep hours (0–24)
cursor.execute("""
    SELECT date, sleep_hours
    FROM training_sessions
    WHERE sleep_hours IS NULL
       OR sleep_hours < 0
       OR sleep_hours > 24
""")

invalid_sleep = cursor.fetchall()
print("Invalid sleep records:", invalid_sleep)


# Check felt rating (1–5)
cursor.execute("""
    SELECT date, felt_rating
    FROM training_sessions
    WHERE felt_rating IS NULL
       OR felt_rating < 1
       OR felt_rating > 5
""")

invalid_felt = cursor.fetchall()
print("Invalid felt ratings:", invalid_felt)

cursor.execute("""
    SELECT date, weather
    FROM training_sessions
    WHERE weather IS NULL
       OR weather NOT IN ('warm', 'cold', 'rain')
""")

invalid_weather = cursor.fetchall()
print("Invalid weather records:", invalid_weather)

cursor.execute("""
    SELECT date, session_type
    FROM training_sessions
    WHERE session_type NOT IN (
        'rest', 'gym', 'flys', 'hills',
        'sled pulls', 'up-backs', 'sled/blocks'
    )
""")

invalid_sessions = cursor.fetchall()
print("Invalid session types:", invalid_sessions)


cursor.execute("""
    SELECT session_type,
           ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
           COUNT(intensity_rpe) AS total_sessions
    FROM training_sessions
    WHERE intensity_rpe IS NOT NULL
    GROUP BY session_type
    ORDER BY avg_rpe DESC
""")

results = cursor.fetchall()

for row in results:
    print(row)

cursor.execute("""
    SELECT sleep_hours,
           ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
           COUNT(*) AS total_sessions
    FROM training_sessions
    WHERE intensity_rpe IS NOT NULL
    GROUP BY sleep_hours
    ORDER BY sleep_hours ASC
""")

results = cursor.fetchall()

print("\nAverage RPE by sleep hours:")

for row in results:
    print(row)

cursor.execute("""
    SELECT weather,
           ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
           COUNT(*) AS total_sessions
    FROM training_sessions
    WHERE intensity_rpe IS NOT NULL
    GROUP BY weather
    ORDER BY avg_rpe DESC
""")

results = cursor.fetchall()

print("\nAverage RPE by weather:")

for row in results:
    print(row)

cursor.execute("""
    SELECT felt_rating,
           ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
           COUNT(*) AS total_sessions
    FROM training_sessions
    WHERE intensity_rpe IS NOT NULL
    GROUP BY felt_rating
    ORDER BY felt_rating ASC
""")

results = cursor.fetchall()

print("\nAverage RPE by felt rating:")

for row in results:
    print(row)

conn.close()


