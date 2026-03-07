from flask import Flask, jsonify
import os
from dotenv import load_dotenv
import mysql.connector

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
    conn.close()
    # app.run()

def init_db(conn, db_name: str) -> None:
    cur = conn.cursor()

    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cur.execute(f"USE `{db_name}`")
    cur.close()


def run_db():
    conn = get_connection()
    init_db(conn, DB_NAME)
    conn.close()
    get_daily_entries()
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

