
import sqlite3
import os
import subprocess
import sys

DATABASE = "sprint_data.db"


# --------------------------------
# Display Main Menu
# --------------------------------

def display_menu():
    print("\n===== SPRINT TRAINING ANALYSER =====")
    print("1. View all training sessions")
    print("2. Average RPE by session type")
    print("3. Sleep vs RPE")
    print("4. Weather vs RPE")
    print("5. Felt rating vs RPE")
    print("6. View charts")
    print("0. Exit")


# --------------------------------
# Option 1: View All Sessions
# --------------------------------

def view_sessions():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, session_type, duration_min,
               intensity_rpe, sleep_hours, felt_rating, weather
        FROM training_sessions
        ORDER BY date ASC
    """)

    sessions = cursor.fetchall()

    print("\n===== ALL TRAINING SESSIONS =====")

    for session in sessions:
        print(session)

    print(f"\nTotal records: {len(sessions)}")

    conn.close()


# --------------------------------
# Option 2: Average RPE by Session
# --------------------------------

def average_rpe_by_session():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT session_type,
               ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
               COUNT(*) AS total_sessions
        FROM training_sessions
        WHERE intensity_rpe IS NOT NULL
        GROUP BY session_type
        ORDER BY avg_rpe DESC
    """)

    results = cursor.fetchall()

    print("\n===== AVERAGE RPE BY SESSION TYPE =====")

    for session_type, avg_rpe, total in results:
        print(
            f"{session_type}: "
            f"Average RPE = {avg_rpe}, "
            f"Sessions = {total}"
        )

    conn.close()


# --------------------------------
# Option 3: Sleep vs RPE
# --------------------------------

def sleep_vs_rpe():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sleep_hours,
               ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
               COUNT(*) AS total_sessions
        FROM training_sessions
        WHERE intensity_rpe IS NOT NULL
          AND sleep_hours IS NOT NULL
        GROUP BY sleep_hours
        ORDER BY sleep_hours ASC
    """)

    results = cursor.fetchall()

    print("\n===== SLEEP VS RPE =====")

    for sleep, avg_rpe, total in results:
        print(
            f"Sleep: {sleep} hours | "
            f"Average RPE: {avg_rpe} | "
            f"Sessions: {total}"
        )

    conn.close()


# --------------------------------
# Option 4: Weather vs RPE
# --------------------------------

def weather_vs_rpe():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT weather,
               ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
               COUNT(*) AS total_sessions
        FROM training_sessions
        WHERE intensity_rpe IS NOT NULL
          AND weather IS NOT NULL
        GROUP BY weather
        ORDER BY avg_rpe DESC
    """)

    results = cursor.fetchall()

    print("\n===== WEATHER VS RPE =====")

    for weather, avg_rpe, total in results:
        print(
            f"Weather: {weather} | "
            f"Average RPE: {avg_rpe} | "
            f"Sessions: {total}"
        )

    conn.close()


# --------------------------------
# Option 5: Felt Rating vs RPE
# --------------------------------

def felt_vs_rpe():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT felt_rating,
               ROUND(AVG(intensity_rpe), 2) AS avg_rpe,
               COUNT(*) AS total_sessions
        FROM training_sessions
        WHERE intensity_rpe IS NOT NULL
          AND felt_rating IS NOT NULL
        GROUP BY felt_rating
        ORDER BY felt_rating ASC
    """)

    results = cursor.fetchall()

    print("\n===== FELT RATING VS RPE =====")

    for felt, avg_rpe, total in results:
        print(
            f"Felt Rating: {felt}/5 | "
            f"Average RPE: {avg_rpe} | "
            f"Sessions: {total}"
        )

    conn.close()


# --------------------------------
# Option 6: Display Charts
# --------------------------------

def view_charts():
    print("\n===== GENERATING CHARTS =====")

    # Run the existing analysis.py script
    subprocess.run(
        [sys.executable, "analysis.py"],
        check=True
    )

    print("\nCharts generated and saved in charts/")


# --------------------------------
# Main Program
# --------------------------------

def main():

    if not os.path.exists(DATABASE):
        print("Database not found. Run database.py first.")
        return

    while True:
        display_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            print("Exiting Sprint Training Analyser...")
            break

        elif choice == "1":
            view_sessions()

        elif choice == "2":
            average_rpe_by_session()

        elif choice == "3":
            sleep_vs_rpe()

        elif choice == "4":
            weather_vs_rpe()

        elif choice == "5":
            felt_vs_rpe()

        elif choice == "6":
            view_charts()

        else:
            print("Invalid choice. Please enter a number from 0 to 6.")


if __name__ == "__main__":
    main()
