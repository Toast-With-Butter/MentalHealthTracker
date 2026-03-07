from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import mysql.connector
from seed_mental_health_tracker import preview_entries, iter_entries

app = Flask(__name__)

DB_NAME = "mental_health_tracker"

@app.route('/dailyentries')
def get_daily_entries():
    conn = get_connection()
    init_db(conn, DB_NAME)

    cur = conn.cursor()
    cur.execute("SELECT entry_date, mood_level, stress_level, energy_level, hours_slept, notes FROM daily_entries")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []

    for entry_date, mood_level, stress_level, energy_level,hours_slept, notes in rows:
        result.append({
            "entry_date": entry_date,
            "mood_level": mood_level,
            "stress_level": stress_level,
            "energy_level": energy_level,
            "hours_slept": hours_slept,
            "notes": notes
        })

    return jsonify(result)

def enter_health_data():
    conn = get_connection()
    init_db(conn, DB_NAME)
    cur = conn.cursor()

    try:
        sleep = int(input("How many hours did you sleep?\n->"))
        mood = int(input("How is your mood level on a scale from 1-10?\n->"))
        stress = int(input("How is your stress level on a scale from 1-10?\n->"))
        energy = int(input("How is your energy level on a scale from 1-10?\n->"))
        notes = str(input("Any notes:\n->"))

        sql = "INSERT IGNORE INTO daily_entries (hours_slept, mood_level, stress_level, energy_level, notes)" \
        "VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql,(sleep, mood, stress, energy, notes))
        conn.commit()

        print("Data entered successfully!")

    except ValueError:
        print("You must enter a number.")

    finally:
        cur.close()
        conn.close()


@app.route('/')
def hello_world():  # put application's code here
    run_db()
    return 'Hello World!!'

def get_connection(db = None):
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=db,
    )

def main():
    load_dotenv()
    conn = run_db()
    is_running = True
    while is_running:
        Main_Menu()
        choice = input("--> ")
        is_running = handle_main_menu_input(choice)

    #preview_entries("habits.csv", 2)
    conn.close()

    # app.run()

def handle_main_menu_input(choice):
    if choice == "1":
        enter_health_data()
        return True
    elif choice == "2":
        return True
    elif choice == "3":
        return True
    elif choice == "4":
        return True
    elif choice == "5":
        return True
    elif choice == "6":
        return True
    elif choice == "7":
        Statistics_Menu()
        subchoice = input("--> ")
        handle_statistics_menu_input(subchoice)
        return True
    elif choice in "qQ":
        return False
    else:
        return True

def handle_statistics_menu_input(choice):
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice in "qQ":
        pass


def Main_Menu():
    print("Main Menu:\n",
          "1. Enter daily health data\n",
          "2. View all health data\n",
          "3. Create new habit\n",
          "4. List all habits\n",
          "5. Log daily habit\n",
          "6. View habits log\n",
          "7. View statistics\n",
          "Q. Quit\n")
    
def Statistics_Menu():
    print("Statistics:\n",
          "1. Your health summary\n",
          "2. Your average sleep /night\n",
          "3. Your sleep impact")
    print("Habits:\n",
          "4. Your high streaks")
    print("Q. Go Back!\n")


def init_db(conn, db_name: str) -> None:
    cur = conn.cursor()

    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cur.execute(f"USE `{db_name}`")
    init_schema(conn, db_name)
    cur.close()

def init_schema(conn, db_name: str) -> None:
    cur = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS habits (
        habit_id   INT AUTO_INCREMENT PRIMARY KEY,
        habit_name VARCHAR(100) NOT NULL,
        entry_date DATE         NOT NULL DEFAULT (CURDATE()),
        notes      VARCHAR(255)
    )
    """
    cur.execute(query)

    query = """
    CREATE TABLE IF NOT EXISTS habit_logs(
	habit_log_id INT AUTO_INCREMENT PRIMARY KEY, 
    habit_id INT NOT NULL,
    entry_date DATE NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (habit_id, entry_date),
    FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
    )
    """
    cur.execute(query)

    query = """
    CREATE TABLE IF NOT EXISTS daily_entries(
    entry_date DATE NOT NULL PRIMARY KEY DEFAULT (CURDATE()),
    hours_slept INT NOT NULL,
    mood_level INT NOT NULL,
    stress_level INT NOT NULL,
    energy_level INT NOT NULL,
    notes VARCHAR(255)
    )
    """
    cur.execute(query)

    query = """
    CREATE TABLE IF NOT EXISTS alerts(
    entry_date DATE DEFAULT (CURDATE()),
    alert_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    alert_type VARCHAR(100) NOT NULL,
    alert_message VARCHAR(255) NOT NULL
    )
    """
    cur.execute(query)

    cur.close()

def run_db():
    conn = get_connection()
    init_db(conn, DB_NAME)
    conn.close()
    return conn

def get_daily_entries():
    conn = get_connection(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT entry_date, mood_level, stress_level, energy_level, hours_slept, notes FROM daily_entries")
    rows = cur.fetchall()
    cur.close()
    print("Fetched rows:", len(rows))
    for entry_date, mood_level, stress_level, energy_level, hours_slept, notes in rows:
        print(f"Date: {entry_date}")
        print(f"Mood: {mood_level}")
        print(f"Stress: {stress_level}")
        print(f"Energy: {energy_level}")
        print(f"Hours Slept: {hours_slept}")
        print(f"Notes: {notes}")
        print("-" * 40)

if __name__ == '__main__':
    main()

